#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import streamlit.components.v1 as components
import base64
"""
🎨 전력산업 카드뉴스 생성기 - Streamlit UI (비용 안전장치 포함)
- 관심 기사를 시각적인 HTML 카드뉴스로 변환
- Claude AI를 활용한 자동 생성
- 💰 비용 관리 및 안전장치 포함
"""

# 1. 표준 라이브러리
import os
import json
import re
import time
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Union, Tuple, Any

# 2. 서드파티 라이브러리
import streamlit as st
from anthropic import Anthropic  # 변경: import anthropic → from anthropic import Anthropic
from dotenv import load_dotenv
from card_news_paths import get_paths, get_path, get_path_str

# 3. 프로젝트 내부 모듈 - 타입 시스템
from card_news.types import Article, Section, ThemeData
# from card_news.validators import validate_sections, validate_article  # Temporarily disabled
from card_news.decorators import fully_validated

# 4. 프로젝트 내부 모듈 - 기능 모듈
from card_news.section_selector import SectionSelector
from card_news.section_config import SectionConfig
from card_news.test_mode_generator import TestModeGenerator
from watch_interested_articles import InterestMonitor
from card_news.analytics_integration import AnalyticsDashboard

# 5. 레거시 모듈 (점진적 마이그레이션)
from update_summary import add_to_summary, update_summary_date
from summary_ui import render_summary_tab

# 비용 상수 (2025년 6월 기준)
COST_PER_REQUEST = 0.555  # USD
COST_PER_REQUEST_KRW = 750  # KRW

# 파일 경로 상수
# 경로 관리자 초기화
paths = get_paths()

# 파일 경로 상수 (하위 호환성 유지)
COST_TRACKING_FILE = get_path_str('cost_tracking')
PENDING_CARDNEWS_FILE = get_path_str('pending_cardnews')
PROCESSED_ARTICLES_FILE = get_path_str('processed_articles')
GENERATED_HISTORY_FILE = get_path_str('generated_history')
SECTION_STYLES_PATH = 'card_news/section_styles.css'


# 페이지 설정
st.set_page_config(
    page_title="⚡ 전력산업 카드뉴스 생성기",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 비용 상수 (2025년 6월 기준)
COST_PER_REQUEST = 0.555  # USD
COST_PER_REQUEST_KRW = 750  # KRW

# CSS 스타일
st.markdown("""
<style>
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    .article-card {
        background: #f3f4f6;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 4px solid #3b82f6;
    }
    .keyword-tag {
        background: #e0e7ff;
        color: #3730a3;
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        font-size: 0.875rem;
        margin-right: 0.5rem;
    }
    .cost-warning {
        background: #fef3c7;
        border: 2px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .cost-alert {
        background: #fee2e2;
        border: 2px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)



class CostManager:
    """비용 관리 클래스"""
    
    def __init__(self):
        self.cost_file = COST_TRACKING_FILE
        self.load_costs()
    
    def load_costs(self):
        """비용 기록 로드"""
        if os.path.exists(self.cost_file):
            with open(self.cost_file, 'r') as f:
                self.costs = json.load(f)
        else:
            self.costs = {
                'daily': {},
                'monthly': {},
                'total': 0
            }
    
    def save_costs(self):
        """비용 기록 저장"""
        with open(self.cost_file, 'w') as f:
            json.dump(self.costs, f, indent=2)
    
    def add_cost(self, amount_usd: float):
        """비용 추가"""
        today = date.today().isoformat()
        month = today[:7]
        
        # 일일 비용
        if today not in self.costs['daily']:
            self.costs['daily'][today] = 0
        self.costs['daily'][today] += amount_usd
        
        # 월간 비용
        if month not in self.costs['monthly']:
            self.costs['monthly'][month] = 0
        self.costs['monthly'][month] += amount_usd
        
        # 총 비용
        self.costs['total'] += amount_usd
        
        self.save_costs()
    
    def get_daily_cost(self) -> float:
        """오늘 사용 비용"""
        today = date.today().isoformat()
        return self.costs['daily'].get(today, 0)
    
    def get_monthly_cost(self) -> float:
        """이번 달 사용 비용"""
        month = date.today().isoformat()[:7]
        return self.costs['monthly'].get(month, 0)
    
    def can_generate(self, daily_limit: float = 10, monthly_limit: float = 50) -> tuple[bool, str]:
        """생성 가능 여부 확인"""
        daily_cost = self.get_daily_cost()
        monthly_cost = self.get_monthly_cost()
        
        if daily_cost >= daily_limit:
            return False, f"일일 한도 초과 (${daily_cost:.2f}/${daily_limit})"
        if monthly_cost >= monthly_limit:
            return False, f"월간 한도 초과 (${monthly_cost:.2f}/${monthly_limit})"
        
        return True, "생성 가능"


@fully_validated
class CardNewsGenerator:
    """카드뉴스 생성 클래스"""
    
    def __init__(self):
        """초기화"""
        self.anthropic_client = None
        self.pending_file = PENDING_CARDNEWS_FILE
        self.processed_file = PROCESSED_ARTICLES_FILE
        self.output_dir = get_path('output_html')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cost_manager = CostManager()
            
    def setup_api(self, api_key: str):
        """Claude API 설정"""
        try:
            self.anthropic_client = Anthropic(api_key=api_key)
            return True
        except Exception as e:
            st.error(f"API 설정 실패: {str(e)}")
            return False
    
    def load_pending_articles(self) -> List[Dict]:
        """대기 중인 기사 로드"""
        try:
            if os.path.exists(self.pending_file):
                with open(self.pending_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"기사 로드 실패: {str(e)}")
        return []
    
    def mark_as_processed(self, page_id: str):
        """처리 완료 표시"""
        # processed_articles.json 업데이트
        processed = []
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r') as f:
                processed = json.load(f)
        
        if page_id not in processed:
            processed.append(page_id)
            
        with open(self.processed_file, 'w') as f:
            json.dump(processed, f, ensure_ascii=False, indent=2)
        
        # pending_cardnews.json에서 제거
        pending = self.load_pending_articles()
        pending = [a for a in pending if a['page_id'] != page_id]
        
        with open(self.pending_file, 'w') as f:
            json.dump(pending, f, ensure_ascii=False, indent=2)
    
    def get_color_theme(self, article: Dict) -> Dict[str, str]:
        """기사 주제에 따른 색상 테마 자동 결정"""
        keywords = ' '.join(article.get('keywords', [])) + ' ' + article.get('title', '')
        
        if any(kw in keywords for kw in ['ESS', '배터리', '저장']):
            return {
                'primary': '#10b981',  # 초록
                'secondary': '#3b82f6',  # 파랑
                'gradient': 'linear-gradient(135deg, #10b981 0%, #3b82f6 100%)'
            }
        elif any(kw in keywords for kw in ['태양광', '태양', 'PV']):
            return {
                'primary': '#f59e0b',  # 노랑
                'secondary': '#f97316',  # 주황
                'gradient': 'linear-gradient(135deg, #f59e0b 0%, #ef4444 50%, #dc2626 100%)'
            }
        elif any(kw in keywords for kw in ['정책', '제도', '법안', '규제']):
            return {
                'primary': '#3b82f6',  # 파랑
                'secondary': '#8b5cf6',  # 보라
                'gradient': 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)'
            }
        elif any(kw in keywords for kw in ['문제', '위기', '도전', '해결']):
            return {
                'primary': '#ef4444',  # 빨강
                'secondary': '#f97316',  # 주황
                'gradient': 'linear-gradient(135deg, #ef4444 0%, #f97316 100%)'
            }
        else:  # 기본값
            return {
                'primary': '#6366f1',  # 인디고
                'secondary': '#8b5cf6',  # 보라
                'gradient': 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)'
            }
    
    def generate_card_news(self, article: Dict, color_theme: Dict, emphasis: List[str]) -> str:
        """Claude API를 통한 카드뉴스 생성"""
        
        # 타입 변환 (validators 활용)
        from card_news.validators import DataValidator
        validator = DataValidator()
        
        # article 정규화
        if isinstance(article, dict) and 'page_id' not in article and 'id' in article:
            article['page_id'] = article['id']
        
        # emphasis 정규화 (List[str] 보장)
        if emphasis:
            emphasis = validator.normalize_sections(emphasis)
        
        # 섹션 스타일 CSS 파일 읽기
        try:
            with open('card_news/section_styles.css', 'r', encoding='utf-8') as f:
                section_styles_css = f.read()
        except FileNotFoundError:
            section_styles_css = ""  # CSS 파일이 없으면 빈 문자열
            st.warning("섹션 스타일 CSS 파일을 찾을 수 없습니다.")

        
        # 섹션 선택기 초기화 및 섹션 선택
        section_selector = SectionSelector()
        
        # 기사 분석 및 섹션 추천
        recommended_sections = section_selector.recommend_sections(article, num_sections=3)
        
        # 선택된 섹션 정보 로깅
        section_names = []
        for section_id, score in recommended_sections:
            section_info = SectionConfig.get_section_by_id(section_id)
            section_names.append(section_info['title'])
        
        st.info(f"🎯 선택된 섹션: {', '.join(section_names)}")
        
        # 동적 프롬프트 생성을 위한 섹션 정보 준비
        dynamic_sections_prompt = section_selector.generate_dynamic_prompt(article, recommended_sections)
        
        # 선택된 섹션의 CSS 스타일 준비
        section_styles = []
        for section_id, _ in recommended_sections:
            style_info = SectionConfig.get_section_style(section_id)
            section_info = SectionConfig.get_section_by_id(section_id)
            
            # 각 섹션의 CSS 추가
            section_css = f"""
/* {section_info['title']} 섹션 스타일 */
.{style_info['class']} {{
    --section-color: {style_info['color']};
    background: linear-gradient(135deg, {style_info['color']} 0%, {style_info['color']}CC 100%);
    padding: 2rem;
    margin: 1.5rem 0;
    border-radius: 12px;
    border-left: 5px solid {style_info['color']};
}}

.{style_info['class']} .section-icon {{
    font-size: 2rem;
    margin-bottom: 1rem;
}}
"""
            section_styles.append(section_css)
        
        # CSS를 하나의 문자열로 결합
        dynamic_section_css = '\n'.join(section_styles)
        
        # 섹션 선택 분석 데이터 저장
        if article.get('id'):
            section_selector.save_selection_analytics(article['id'], recommended_sections)
        
        
        
        # 강조 요소 프롬프트 생성
        emphasis_prompt = ""
        if emphasis:
            emphasis_prompt = f"\n\n특별히 강조할 요소:\n" + "\n".join([f"- {e}" for e in emphasis])
        
                # color_theme에서 색상 추출
        primary_color = color_theme['primary']
        secondary_color = color_theme.get('secondary', color_theme['primary'])
        tertiary_color = secondary_color  # 간단하게 처리
        
        # RGBA 값 계산 (hex to rgba)
        def hex_to_rgba(hex_color):
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f"{r}, {g}, {b}"
        
        rgba_primary = hex_to_rgba(primary_color)
        color_theme['rgba_primary'] = rgba_primary
        
        prompt = f"""당신은 전력산업 전문 웹 디자이너입니다. 아래 지침을 반드시 준수하여 카드뉴스를 생성하세요.

[⚠️ 시사점 작성 필수 지침]
5번 섹션(핵심 시사점 및 향후 전망)을 작성할 때:
1. "기사 내용을 바탕으로..." 같은 템플릿 문구를 절대 사용하지 마세요
2. 실제 기사 내용을 분석하여 구체적인 시사점을 작성하세요
3. 다음 내용을 반드시 포함하세요:
   - 이 기사가 전력산업에 미치는 실질적 영향 (구체적 수치나 예상 효과 포함)
   - 관련 기업들이 실제로 취해야 할 행동 (구체적인 전략이나 준비사항)
   - 시장 변화 예측 (단기/중기/장기로 구분하여 구체적으로)
4. 일반적이고 뻔한 내용이 아닌, 이 기사 특유의 시사점을 도출하세요

[⚠️ 필수 준수사항]
1. ❌ 절대 외부 CSS/JS 파일 참조 금지 - <link href="styles.css">, <script src="animations.js"> 등 사용 금지!
2. ✅ 모든 스타일은 반드시 <style> 태그 내에 인라인으로 포함
3. ✅ 완전히 독립적인 단일 HTML 파일로 생성
4. ✅ 아래 Enhanced 스타일 가이드의 모든 CSS를 <style> 태그 안에 포함

[기사 정보]
제목: {article['title']}
요약: {article['summary']}
핵심내용: {article['content']}
키워드: {', '.join(article.get('keywords', []))}
원문 URL: {article.get('url', '')}

[Enhanced 스타일 가이드 - 디폴트 양식 필수 준수사항]

⚠️ 중요: 아래의 모든 CSS는 반드시 <style> 태그 안에 포함하세요!
절대로 외부 CSS 파일(styles.css 등)을 만들거나 참조하지 마세요!

## 1. 필수 기본 설정
/* CSS CODE START - 반드시 모든 스타일을 <style> 태그 안에 포함! */

/* ========== 동적으로 선택된 섹션 스타일 ========== */
{dynamic_section_css}

/* ========== 기본 스타일 계속 ========== */

/* ========== 섹션 공통 스타일 ========== */
{section_styles_css}
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

/* 기본 설정 */
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: 'Pretendard', -apple-system, sans-serif;
    background: #0a0a0a;
    color: #ffffff;
    line-height: 1.8;
    font-size: 1.1rem;  /* 디폴트 본문 크기 */
}}

/* 필수 폰트 크기 - 디폴트 양식과 동일하게! */
h1 {{ font-size: 3rem; font-weight: 800; }}
h2 {{ font-size: 2.5rem; margin-bottom: 2rem; }}
.subtitle {{ font-size: 1.1rem; opacity: 0.9; }}
.insight-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
.stat-number {{ font-size: 3rem; font-weight: 700; }}
/* CODE END */

## 2. 색상 테마 (3색 그라데이션 필수)
현재 기사 테마:
- 주색상: {color_theme['primary']}
- 중간색: {color_theme.get('secondary', color_theme['primary'])}
- 끝색상: {color_theme.get('tertiary', color_theme['secondary'])}
- 그라데이션: {color_theme['gradient']}
- RGBA: rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 알파값)

## 3. 히어로 섹션 (복잡한 배경 효과 필수)
/* CSS CODE START */
.hero {{
    background: {color_theme['gradient']};
    min-height: 500px;
    position: relative;
    overflow: hidden;
}}
.hero::before {{
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 80%, rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.2) 0%, transparent 50%);
    animation: float 15s ease-in-out infinite;
}}
/* CODE END */

## 4. 홈 버튼 (우상단 고정)
<!-- 홈 버튼 제거됨 - Streamlit 탭으로 대체 -->
/* CODE END */
- section fade-in (NOT section만)
- insight-grid, insight-card, insight-icon, insight-title
- stats-grid, stat-card counter, stat-value, stat-label
- timeline, timeline-item, timeline-marker, timeline-content
- expert-quote

## 5-1. 전문가 인용문 스타일
/* CSS CODE START */
.expert-quote {{
    position: relative;
    background: rgba(255, 255, 255, 0.05);
    border-left: 4px solid {color_theme['primary']};
    padding: 30px 40px;
    margin: 30px 0;
    font-style: italic;
    font-size: 1.2rem;
    line-height: 1.8;
    border-radius: 0 15px 15px 0;
}}
.expert-quote::before {{
    content: '"';
    position: absolute;
    top: -10px;
    left: 20px;
    font-size: 4rem;
    color: {color_theme['primary']};
    opacity: 0.3;
    font-family: Georgia, serif;
}}
.expert-quote p {{
    margin-top: 20px;
    font-size: 0.9rem;
    opacity: 0.8;
    text-align: right;
    font-style: normal;
}}
/* CODE END */

## 6. 카드 hover 효과
/* CSS CODE START */
.insight-card {{
    background: rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.1);
    border: 1px solid rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.3);
    transition: all 0.3s;
}}
.insight-card:hover {{
    transform: translateY(-10px);
    box-shadow: 0 10px 30px rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.3);
}}
/* CODE END */

## 7. 필수 섹션 (정확한 제목과 구조)
1. 🎯 핵심 인사이트 - insight-grid에 insight-card 3개
2. 📊 주요 성과 및 지표 - stats-grid에 stat-card 4개
3. 🌍 진행 경과 - timeline 구조
4. 💬 전문가 의견 - expert-quote
5. 🔮 시사점 및 전망 - 추가 insight-grid

## 8. 애니메이션 (자체 CSS)
/* CSS CODE START */
/* 필수 애니메이션 - 디폴트 양식과 동일! */
@keyframes float {{
    0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
    33% {{ transform: translate(30px, -30px) rotate(120deg); }}
    66% {{ transform: translate(-20px, 20px) rotate(240deg); }}
}}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(30px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes countUp {{
    from {{ opacity: 0; transform: scale(0.5); }}
    to {{ opacity: 1; transform: scale(1); }}
}}
.fade-in {{
    opacity: 0;
    animation: fadeInUp 0.8s ease forwards;
}}
/* CODE END */

{emphasis_prompt}

[HTML 구조 템플릿]
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>제목 - 전력산업 뉴스</title>
    <style>
        /* 모든 CSS는 여기에! 외부 파일 참조 금지! */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        /* 위에서 제공한 Enhanced 스타일 가이드의 모든 CSS를 여기에 포함하세요 */
        /* body, container, home-button, hero, 모든 섹션 스타일 등 */
    </style>
</head>
<!-- 홈 버튼 제거됨 - Streamlit 탭으로 대체 -->
    <!-- 컨텐츠 -->
</body>
</html>

반드시 위 구조를 따르고, 절대 style.css나 animations.js 같은 외부 파일을 참조하지 마세요!
모든 스타일은 <style> 태그 안에 직접 작성하세요.

[컨텐츠 구성 가이드라인 - 필수!]
기사 내용을 분석하여 다음과 같이 동적으로 선택된 섹션들을 포함하여 구성하세요:

{dynamic_sections_prompt}

⚠️ 중요: 위에서 지정된 섹션 순서와 구조를 정확히 따라주세요!

[섹션별 스타일 가이드]
   <!-- 반드시 이 섹션을 포함하세요! AI가 분석한 내용을 작성합니다 -->
   <section class="fade-in">
       <h2>🔮 핵심 시사점 및 향후 전망</h2>
       <!-- expert-quote 대신 다른 스타일 사용 -->
       <div style="background: linear-gradient(135deg, rgba({rgba_primary}, 0.1), rgba({rgba_primary}, 0.05)); 
                   border: 2px solid rgba({rgba_primary}, 0.3); 
                   border-radius: 20px; 
                   padding: 40px;
                   position: relative;
                   overflow: hidden;">
           <!-- 배경 장식 -->
           <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; 
                       background: radial-gradient(circle, rgba({rgba_primary}, 0.1), transparent); 
                       border-radius: 50%;"></div>
           
           <h3 style="color: {primary_color}; margin-bottom: 30px; font-size: 1.5rem;">
               <span style="display: inline-block; margin-right: 10px;">🔍</span>
               산업 영향 분석
           </h3>
           <p style="line-height: 1.8; margin-bottom: 30px;">
               이 기사가 전력산업에 미치는 구체적인 영향을 분석하여 작성하세요.
               단기적 영향과 장기적 변화를 구분하여 설명하세요.
           </p>
           
           <h3 style="color: {primary_color}; margin-bottom: 20px; font-size: 1.5rem;">
               <span style="display: inline-block; margin-right: 10px;">🎯</span>
               기업 대응 전략
           </h3>
           <ul style="list-style: none; padding: 0; margin-bottom: 30px;">
               <li style="margin-bottom: 15px; padding-left: 30px; position: relative;">
                   <span style="position: absolute; left: 0; color: {primary_color};">▶</span>
                   관련 기업들이 준비해야 할 구체적인 대응 방안 1
               </li>
               <li style="margin-bottom: 15px; padding-left: 30px; position: relative;">
                   <span style="position: absolute; left: 0; color: {primary_color};">▶</span>
                   시장 변화에 대응하기 위한 전략적 준비사항 2
               </li>
               <li style="margin-bottom: 15px; padding-left: 30px; position: relative;">
                   <span style="position: absolute; left: 0; color: {primary_color};">▶</span>
                   새로운 기회 요인과 활용 방안 3
               </li>
           </ul>
           
           <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; margin-top: 30px;">
               <h4 style="color: {primary_color}; margin-bottom: 15px;">📅 향후 전망</h4>
               <p style="margin: 0;">
                   앞으로의 시장 전망과 예상되는 변화를 구체적으로 작성하세요.
                   시기별(단기/중기/장기) 전망을 포함하면 더 좋습니다.
               </p>
           </div>
       </div>
   </section>"""

        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=8000
            )
            
            # 비용 기록
            self.cost_manager.add_cost(COST_PER_REQUEST)
            
            # HTML 추출 (마크다운 코드블록 처리)
            raw_content = response.content[0].text
            
            # 마크다운 코드블록에서 HTML 추출
            html_match = re.search(r'```html\s*(.*?)```', raw_content, re.DOTALL)
            if html_match:
                content = html_match.group(1).strip()
            else:
                # 코드블록이 없으면 전체 내용 사용
                content = raw_content
            
            # HTML 태그가 없으면 기본 구조 추가
            if not content.strip().startswith('<!DOCTYPE') and not content.strip().startswith('<html'):
                content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
</head>
<body>
{content}
</body>
</html>"""
            
            return content
            
        except Exception as e:
            st.error(f"카드뉴스 생성 실패: {str(e)}")
            return None




def load_interested_articles() -> List[Dict]:
    """관심 표시된 기사 로드"""
    pending_file = PENDING_CARDNEWS_FILE  # 통일된 경로 사용
    if os.path.exists(pending_file):
        try:
            with open(pending_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"기사 로드 중 오류: {str(e)}")
    return []


def main():
    """메인 앱 실행"""
    st.title("⚡ 전력산업 카드뉴스 생성기")
    st.markdown("관심 기사를 아름다운 카드뉴스로 변환합니다 🎨")
    
    # 생성기 초기화
    generator = CardNewsGenerator()
    test_generator = TestModeGenerator()
    analytics_dashboard = AnalyticsDashboard()
    
    # 변수 초기화 (사이드바 밖에서도 접근 가능하도록)
    test_mode = False
    api_key = None
    
    # 사이드바 - API 설정 및 비용 관리
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # 테스트 모드
        test_mode = st.checkbox(
            "🧪 테스트 모드",
            help="API 호출 없이 테스트 (무료)"
        )
        
        if test_mode:
            st.info("ℹ️ 테스트 모드가 활성화되었습니다. 실제 API는 호출되지 않습니다.")
        
        
        # API 키 입력 (테스트 모드가 아닐 때만)
        if not test_mode:
            api_key = st.text_input(
                "Anthropic API Key",
                type="password",
                help="Claude API 키를 입력하세요"
            )
        
            if api_key:
                if generator.setup_api(api_key):
                    st.success("✅ API 연결 성공!")
                else:
                    st.error("❌ API 연결 실패")
            else:
                st.warning("⚠️ API 키를 입력해주세요")
        
        st.divider()
        
        # 💰 비용 관리
        st.header("💰 비용 관리")
        
        # 비용 한도 설정
        st.subheader("📊 한도 설정")
        daily_limit = st.number_input("일일 한도 ($)", min_value=1.0, value=10.0, step=1.0)
        monthly_limit = st.number_input("월간 한도 ($)", min_value=10.0, value=50.0, step=10.0)
        
        # 현재 사용량
        st.subheader("📈 현재 사용량")
        today_cost = generator.cost_manager.get_daily_cost()
        month_cost = generator.cost_manager.get_monthly_cost()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("오늘 사용", f"${today_cost:.2f}", f"≈ ₩{today_cost * 1370:.0f}")
        with col2:
            st.metric("이번 달", f"${month_cost:.2f}", f"≈ ₩{month_cost * 1370:.0f}")
        
        # 한도 체크
        can_gen, message = generator.cost_manager.can_generate(daily_limit, monthly_limit)
        
        if not can_gen:
            st.error(f"⚠️ {message}")
        else:
            daily_remaining = daily_limit - generator.cost_manager.get_daily_cost()
            monthly_remaining = monthly_limit - generator.cost_manager.get_monthly_cost()
            st.info(f"일일 잔여: ${daily_remaining:.2f}")
            st.info(f"월간 잔여: ${monthly_remaining:.2f}")
        
        st.divider()
        
        # 새로고침
        col_refresh1, col_refresh2 = st.columns([1, 2])
        with col_refresh1:
            if st.button("🔄 기사 목록 새로고침"):
                # 노션에서 최신 관심 기사 가져오기
                try:
                    with st.spinner("노션에서 관심 기사를 확인하는 중..."):
                        monitor = InterestMonitor()
                        new_articles = monitor.check_new_interests()
                        
                        if new_articles:
                            # 기존 기사 로드
                            existing_articles = []
                            if os.path.exists(PENDING_CARDNEWS_FILE):
                                with open(PENDING_CARDNEWS_FILE, 'r') as f:
                                    existing_articles = json.load(f)
                            
                            # 중복 제거 후 추가
                            existing_ids = {a.get('page_id') for a in existing_articles}
                            added_count = 0
                            for article in new_articles:
                                if article.get('page_id') not in existing_ids:
                                    existing_articles.append(article)
                                    added_count += 1
                            
                            # 저장
                            if added_count > 0:
                                monitor.save_pending_articles(existing_articles)
                                st.success(f"✅ 노션에서 {added_count}개의 새로운 관심 기사를 추가했습니다!")
                            else:
                                st.info("📌 모든 관심 기사가 이미 추가되어 있습니다.")
                        else:
                            st.info("📭 노션에 새로운 관심 기사가 없습니다.")
                except Exception as e:
                    st.warning(f"노션 연동 중 오류: {str(e)}")
                    st.info("로컬 파일만 새로고침합니다.")
                
                st.rerun()
        
        with col_refresh2:
            st.caption("💡 노션에서 '관심' 체크한 기사를 자동으로 가져옵니다.")
        
        # 통계
        st.header("📊 통계")
        pending = generator.load_pending_articles()
        st.metric("대기 중인 기사", f"{len(pending)}개")
        st.metric("총 누적 비용", f"${generator.cost_manager.costs['total']:.2f}")
    
    # 메인 컨텐츠
    # 테스트 모드가 아닐 때만 API 키 확인
    if not test_mode and not api_key:
        st.info("👈 사이드바에서 API 키를 입력해주세요")
        return
    
    # 대기 중인 기사 로드
    articles = load_interested_articles()
    
    if not articles:
        st.info("📭 카드뉴스로 만들 관심 기사가 없습니다.")
        st.markdown("노션에서 관심 있는 기사에 체크하면 여기에 표시됩니다.")
        return
    
    tabs = st.tabs(["📰 카드뉴스 생성", "📚 요약 카드뉴스", "📊 분석 대시보드", "📋 생성 기록", "💰 비용 관리", "ℹ️ 사용 안내"])
    tab1, tab2, tab3, tab4, tab5, tab6 = tabs
    with tab1:
        st.header("📰 관심 기사 목록")
        
        # 한도 확인
        can_gen, message = generator.cost_manager.can_generate(daily_limit, monthly_limit)
        if not can_gen:
            st.markdown("""
            <div class="cost-alert">
                <h3>⚠️ 비용 한도 초과</h3>
                <p>설정된 한도를 초과하여 새로운 카드뉴스를 생성할 수 없습니다.</p>
                <p>사이드바에서 한도를 조정하거나 다음 날/달을 기다려주세요.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 기사 표시
        for idx, article in enumerate(articles):
            with st.expander(f"**{article['title']}**", expanded=False):
                # 키워드 표시
                if article.get('keywords'):
                    keywords_html = ' '.join([
                        f'<span class="keyword-tag">{kw}</span>' 
                        for kw in article['keywords']
                    ])
                    st.markdown(keywords_html, unsafe_allow_html=True)
                
                # 요약
                st.markdown("**📝 요약:**")
                st.write(article['summary'])
                
                # 핵심 내용
                if article.get('content'):
                    st.markdown("**💡 핵심 내용:**")
                    st.text_area("", article['content'], height=150, disabled=True, key=f"content_{idx}")
                
                # 원문 링크
                if article.get('url'):
                    st.markdown(f"[🔗 원문 보기]({article['url']})")
                
                st.divider()
                
                # 생성 옵션
                col1, col2 = st.columns(2)
                
                with col1:
                    # 색상 테마 자동 결정
                    auto_theme = generator.get_color_theme(article)
                    st.markdown(f"**자동 선택된 색상:**")
                    st.color_picker("주 색상", auto_theme['primary'], key=f"color1_{idx}", disabled=True)
                    st.color_picker("보조 색상", auto_theme['secondary'], key=f"color2_{idx}", disabled=True)
                
                with col2:
                    emphasis = st.multiselect(
                        "강조할 요소",
                        ["📊 차트/그래프", "📅 타임라인", "📋 비교 테이블", 
                         "💬 인용구", "🔢 통계 카운터", "🎯 인포그래픽"],
                        key=f"emphasis_{idx}"
                    )
                
                # 비용 경고
                if test_mode:
                    st.markdown("""
                    <div class="cost-warning" style="background: #d1fae5; border-color: #10b981;">
                        <strong>🧪 테스트 모드 안내</strong><br>
                        테스트 모드에서는 <strong>비용이 발생하지 않습니다</strong>.<br>
                        실제 API를 호출하지 않고 템플릿 기반으로 카드뉴스를 생성합니다.<br>
                        생성된 파일은 별도의 테스트 폴더에 저장됩니다.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="cost-warning">
                        <strong>💰 비용 안내</strong><br>
                        이 카드뉴스를 생성하면 <strong>${COST_PER_REQUEST}</strong> (약 {COST_PER_REQUEST_KRW}원)의 비용이 발생합니다.<br>
                        오늘 사용: ${today_cost:.2f} / ${daily_limit:.2f}<br>
                        이번 달: ${month_cost:.2f} / ${monthly_limit:.2f}
                    </div>
                    """, unsafe_allow_html=True)
                
                # 생성 버튼 (한도 확인)
                if can_gen:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        confirm = st.checkbox(
                            f"{'테스트 생성을 진행합니다' if test_mode else f'비용 ${COST_PER_REQUEST} 발생을 확인했습니다'}", 
                            key=f"confirm_{idx}"
                        )
                    
                    with col2:
                        if st.button(
                            f"🎨 카드뉴스 생성", 
                            key=f"generate_{idx}", 
                            type="primary",
                            disabled=not confirm
                        ):
                            with st.spinner("🎨 카드뉴스 생성 중..." + (" (테스트 모드)" if test_mode else " (30초~1분 소요)")):
                                # 카드뉴스 생성
                                if test_mode:
                                    # 테스트 모드: 실제 API 호출 없음
                                    html_content = test_generator.generate_test_card_news(
                                        article, 
                                        theme=list(auto_theme.keys())[0] if isinstance(auto_theme, dict) else 'modern',
                                        sections=emphasis
                                    )
                                else:
                                    # 실제 API 호출
                                    html_content = generator.generate_card_news(
                                        article, auto_theme, emphasis
                                    )
                                
                                if html_content:
                                    st.success(f"✅ 카드뉴스 생성 완료! {'(테스트 모드 - 비용 없음)' if test_mode else f'(비용: ${COST_PER_REQUEST})'}")
                                    st.balloons()
                                    
                                    # 미리보기
                                    st.markdown("### 👁️ 미리보기")
                                    st.components.v1.html(html_content, height=800, scrolling=True)
                                    
                                    # 저장
                                    col1, col2, col3 = st.columns(3)
                                    
                                    with col1:
                                        # 파일명 생성
                                        safe_title = re.sub(r'[^\w\s-]', '', article['title'])[:50]
                                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                        filename = f"{'TEST_' if test_mode else ''}detail_{safe_title}_{timestamp}.html"
                                        filepath = (Path(get_path_str('output_test')) if test_mode else generator.output_dir) / filename
                                        
                                        if st.button("💾 저장", key=f"save_{idx}"):
                                            with open(filepath, 'w', encoding='utf-8') as f:
                                                f.write(html_content)
                                            
                                            st.success(f"✅ 저장 완료: {filename}")
                                            
                                            # 처리 완료 표시
                                            if not test_mode:
                                                generator.mark_as_processed(article['page_id'])
                                            st.rerun()
                                    
                                    # 파일을 detailed 폴더에 자동 저장
                                    detailed_dir = Path(get_path_str('output_test')) if test_mode else generator.output_dir
                                    detailed_dir.mkdir(exist_ok=True)
                                    
                                    file_path = detailed_dir / filename
                                    with open(file_path, 'w', encoding='utf-8') as f:
                                        f.write(html_content)
                                    
                                    st.info(f"📁 파일이 자동 저장되었습니다: {file_path}")
                                    
                                    # 요약 페이지에 추가
                                    if not test_mode:
                                        try:
                                            if add_to_summary(article, str(file_path), str(generator.output_dir)):
                                                st.success("📝 요약 페이지에 추가되었습니다!")
                                                update_summary_date()
                                        except Exception as e:
                                            st.warning(f"요약 페이지 업데이트 실패: {e}")
                                    else:
                                        st.info("🧪 테스트 모드: 요약 페이지에 추가되지 않습니다.")
                                    
                                    with col2:
                                        # 다운로드
                                        st.download_button(
                                            label="📥 다운로드",
                                            data=html_content,
                                            file_name=filename,
                                            mime="text/html",
                                            key=f"download_{idx}"
                                        )
                                    
                                    with col3:
                                        if st.button("🔄 다시 생성", key=f"regenerate_{idx}"):
                                            st.rerun()
                else:
                    st.error("❌ 비용 한도 초과로 생성할 수 없습니다")
    

    with tab2:
        render_summary_tab()

    with tab3:
        st.header("📊 섹션 분석 대시보드")
        
        # 분석 대시보드 렌더링
        analytics_dashboard.render_full_dashboard()
        
        # 섹션 최적화 도구
        st.subheader("🔧 섹션 최적화 도구")
        
        # 키워드 입력
        keywords_input = st.text_input(
            "키워드 입력 (쉼표로 구분)",
            placeholder="재생에너지, ESS, 태양광"
        )
        
        if keywords_input:
            keywords = [kw.strip() for kw in keywords_input.split(',')]
            
            # 신뢰도 점수 표시
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**섹션 신뢰도 점수**")
                reliability_scores = analytics_dashboard.render_mini_dashboard(keywords)
            
            with col2:
                st.write("**추천 섹션**")
                optimized_sections, reasons = analytics_dashboard.get_optimized_sections(keywords)
                
                for section, reason in zip(optimized_sections, reasons):
                    st.write(f"• {section}")
                    st.caption(f"  → {reason}")
    
    with tab4:
        st.header("📋 생성 기록")
        
        # 생성된 파일 목록
        if generator.output_dir.exists():
            files = sorted(generator.output_dir.glob("*.html"), key=lambda x: x.stat().st_mtime, reverse=True)
            
            if files:
                for file in files[:20]:  # 최근 20개만 표시
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(f"📄 {file.name}")
                    with col2:
                        if st.button("👁️ 보기", key=f"view_{file.name}"):
                            with open(file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            st.components.v1.html(content, height=800, scrolling=True)
            else:
                st.info("아직 생성된 카드뉴스가 없습니다.")
    
    with tab5:
        st.header("💰 비용 분석")
        
        # 일별 비용 차트
        st.subheader("📊 일별 사용 비용")
        daily_data = generator.cost_manager.costs['daily']
        if daily_data:
            import pandas as pd
            df = pd.DataFrame(list(daily_data.items()), columns=['날짜', '비용($)'])
            df['비용(원)'] = df['비용($)'] * 1370
            st.line_chart(df.set_index('날짜')['비용($)'])
            st.dataframe(df)
        
        # 월별 비용 차트
        st.subheader("📊 월별 사용 비용")
        monthly_data = generator.cost_manager.costs['monthly']
        if monthly_data:
            df = pd.DataFrame(list(monthly_data.items()), columns=['월', '비용($)'])
            df['비용(원)'] = df['비용($)'] * 1370
            st.bar_chart(df.set_index('월')['비용($)'])
            st.dataframe(df)
        
        # 비용 절감 팁
        st.subheader("💡 비용 절감 팁")
        st.markdown("""
        1. **템플릿 재사용**: 비슷한 주제의 기사는 기존 카드뉴스를 수정
        2. **일괄 처리**: 여러 기사를 모아서 한 번에 처리
        3. **미리보기 활용**: 생성 전 충분히 검토
        4. **재생성 최소화**: 첫 생성 시 신중하게 옵션 선택
        """)


        
        # 테스트 파일 관리
        st.subheader("🧪 테스트 파일 관리")
        
        test_dir = Path(get_path_str('output_test'))
        if test_dir.exists():
            test_files = list(test_dir.glob('TEST_*.html'))
            st.info(f"📁 테스트 파일 개수: {len(test_files)}개")
            
            if test_files:
                # 최근 테스트 파일 목록
                st.markdown("**최근 테스트 파일 (최대 5개):**")
                for file in sorted(test_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                    st.text(f"• {file.name}")
                
                # 일괄 삭제 버튼
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ 모든 테스트 파일 삭제", type="secondary"):
                        for file in test_files:
                            file.unlink()
                        st.success(f"✅ {len(test_files)}개의 테스트 파일을 삭제했습니다.")
                        st.rerun()
                
                with col2:
                    # 7일 이상 된 파일 삭제
                    if st.button("🧹 오래된 테스트 파일 정리 (7일 이상)"):
                        import time
                        current_time = time.time()
                        old_files = []
                        for file in test_files:
                            if current_time - file.stat().st_mtime > 7 * 24 * 3600:  # 7일
                                file.unlink()
                                old_files.append(file.name)
                        if old_files:
                            st.success(f"✅ {len(old_files)}개의 오래된 테스트 파일을 삭제했습니다.")
                            st.rerun()
                        else:
                            st.info("7일 이상 된 테스트 파일이 없습니다.")
            else:
                st.success("✨ 테스트 파일이 없습니다.")
        else:
            st.info("🔍 테스트 디렉토리가 아직 생성되지 않았습니다.")

    with tab6:
        st.header("ℹ️ 사용 안내")
        
        st.markdown("""
        ### 🚀 빠른 시작
        
        1. **API 키 설정** (테스트 모드가 아닌 경우)
           - 사이드바에서 Anthropic API 키 입력
           
        2. **기사 선택**
           - 관심 있는 기사 선택
           - 자동으로 테마와 섹션 추천
           
        3. **카드뉴스 생성**
           - 생성 버튼 클릭
           - 30초~1분 대기
           
        ### 🧪 테스트 모드
        - API 키 없이 사용 가능
        - 실제 Claude API 호출 없음
        - 무료로 UI와 기능 테스트
        
        ### 📊 분석 대시보드 활용
        - 섹션별 사용 통계 확인
        - 키워드별 최적 섹션 추천
        - 품질 피드백 데이터 분석
        
        ### 💰 비용 관리
        - 일일 한도: $10
        - 월간 한도: $50
        - 기사당 비용: 약 $0.555 (테스트 모드에서는 무료)
        
        ### 📌 팁
        - 재생에너지 기사 → eco 테마 자동 선택
        - ESS/배터리 기사 → tech 테마 자동 선택
        - 강조 섹션으로 중요 내용 부각
        """)


if __name__ == "__main__":
    main()


# 요약 카드뉴스 탭 렌더링 함수
# 요약 카드뉴스 탭 렌더링 함수
def render_summary_tab():
    """요약 카드뉴스 탭 렌더링 - HTML 임베딩 방식"""
    
    try:
        # CSS 스타일 로드
        css_path = Path('output/card_news/templates/summary_style.css')
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # CSS 적용
            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        else:
            st.warning("CSS 파일을 찾을 수 없습니다. 기본 스타일을 사용합니다.")
    except Exception as e:
        st.error(f"CSS 로드 중 오류 발생: {str(e)}")
    
    # 필터 UI (Streamlit 위젯)
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        search_query = st.text_input("🔍 카드뉴스 검색", placeholder="제목 또는 내용 검색", key="summary_search")
    
    with col2:
        category_filter = st.selectbox(
            "📁 카테고리",
            ["전체", "ESS", "태양광", "정책", "시장", "기술", "VPP", "재생에너지"],
            key="summary_category"
        )
    
    with col3:
        sort_order = st.selectbox(
            "정렬",
            ["최신순", "오래된순"],
            key="summary_sort"
        )
    
    # 카드뉴스 데이터 로드
    try:
        card_news_list = load_generated_card_news()
    except Exception as e:
        st.error(f"카드뉴스 로드 중 오류 발생: {str(e)}")
        return
    
    # 필터링
    filtered_list = filter_card_news(card_news_list, search_query, category_filter)
    
    # 정렬
    if sort_order == "오래된순":
        filtered_list.reverse()
    
    # 헤더 HTML 생성
    header_html = create_summary_header(len(filtered_list))
    st.markdown(header_html, unsafe_allow_html=True)
    
    # 통계 섹션
    if filtered_list:
        stats_html = create_stats_section(filtered_list)
        st.markdown(stats_html, unsafe_allow_html=True)
    
    # 카드 그리드 생성
    if filtered_list:
        grid_html = create_card_grid(filtered_list)
        st.markdown(f'<div class="summary-container">{grid_html}</div>', unsafe_allow_html=True)
    else:
        st.info("🔍 검색 조건에 맞는 카드뉴스가 없습니다.")
def load_generated_card_news():
    """생성된 카드뉴스 목록 로드"""
    card_news_list = []
    html_dir = Path("output/card_news/html")
    
    # HTML 파일들에서 정보 추출
    for html_file in html_dir.glob("detail_*.html"):
        # 파일명에서 정보 추출
        filename = html_file.stem
        parts = filename.replace("detail_", "").rsplit("_", 1)
        
        if len(parts) == 2:
            title = parts[0].replace("-", " ")
            date_str = parts[1]
            
            # 날짜 파싱
            try:
                if len(date_str) == 8:  # YYYYMMDD
                    date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                else:
                    date = "2025-06-10"  # 기본값
            except:
                date = "2025-06-10"
            
            # 카테고리 추측 (제목에서)
            category = "일반"
            category_name = "일반"
            
            if "ESS" in title or "에너지저장" in title:
                category = "ess"
                category_name = "ESS"
            elif "태양광" in title or "태양" in title:
                category = "solar"
                category_name = "태양광"
            elif "정책" in title or "정부" in title or "법" in title:
                category = "policy"
                category_name = "정책"
            elif "VPP" in title or "가상발전" in title:
                category = "vpp"
                category_name = "VPP"
            elif "재생에너지" in title or "신재생" in title:
                category = "renewable"
                category_name = "재생에너지"
            elif "기술" in title or "개발" in title:
                category = "tech"
                category_name = "기술"
            
            card_news_list.append({
                "title": title,
                "date": date,
                "category": category,
                "category_name": category_name,
                "file_path": f"output/card_news/html/{html_file.name}",
                "summary": f"{title}에 대한 상세한 카드뉴스입니다.",
                "source": "전기신문"
            })
    
    # 날짜순 정렬 (최신순)
    card_news_list.sort(key=lambda x: x['date'], reverse=True)
    
    return card_news_list


def filter_card_news(card_list, search_query, category_filter):
    """카드뉴스 필터링"""
    filtered = card_list
    
    # 검색어 필터
    if search_query:
        search_lower = search_query.lower()
        filtered = [
            card for card in filtered
            if search_lower in card['title'].lower() or 
               search_lower in card['summary'].lower()
        ]
    
    # 카테고리 필터
    if category_filter != "전체":
        filtered = [
            card for card in filtered
            if card['category_name'] == category_filter
        ]
    
    return filtered


def create_summary_header(count):
    """헤더 HTML 생성"""
    today = datetime.now().strftime("%Y년 %m월 %d일")
    
    return f'''
    <div class="header">
        <h1>전력산업 카드뉴스</h1>
        <p class="subtitle">{today} | 총 {count}개의 카드뉴스</p>
    </div>
    '''


def create_stats_section(card_list):
    """통계 섹션 HTML 생성"""
    # 카테고리별 집계
    category_counts = {}
    for card in card_list:
        cat = card['category_name']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # 상위 4개 카테고리
    top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:4]
    
    stats_html = '''
    <div class="stats-section">
        <h2 class="stats-title">카테고리별 현황</h2>
        <div class="stats-grid">
    '''
    
    for category, count in top_categories:
        stats_html += f'''
        <div class="stat-item">
            <div class="stat-number">{count}</div>
            <div class="stat-label">{category}</div>
        </div>
        '''
    
    stats_html += '''
        </div>
    </div>
    '''
    
    return stats_html


def create_card_grid(card_list):
    """카드 그리드 HTML 생성"""
    grid_html = '<div class="news-grid">'
    
    for i, card in enumerate(card_list):
        # 카드 HTML 생성
        card_html = f'''
        <div class="news-card" onclick="window.open('{card["file_path"]}', '_blank')">
            <span class="card-category category-{card["category"]}">{card["category_name"]}</span>
            <h3 class="card-title">{card["title"]}</h3>
            <p class="card-summary">{card["summary"]}</p>
            <div class="card-meta">
                <span>{card["source"]} | {card["date"]}</span>
                <a href="#" class="read-more" onclick="event.stopPropagation(); window.open('{card["file_path"]}', '_blank'); return false;">자세히 보기 →</a>
            </div>
        </div>
        '''
        grid_html += card_html
    
    grid_html += '</div>'
    
    # JavaScript 추가 (클릭 이벤트 처리)
    grid_html += '''
    <script>
        // 카드 애니메이션 지연 적용
        document.querySelectorAll('.news-card').forEach((card, index) => {
            card.style.animationDelay = `${0.1 * (index + 1)}s`;
        });
    </script>
    '''
    
    return grid_html
