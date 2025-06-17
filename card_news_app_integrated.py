#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 전력산업 카드뉴스 생성기 - Streamlit UI (분석 대시보드 통합)
- 관심 기사를 시각적인 HTML 카드뉴스로 변환
- Claude AI를 활용한 자동 생성
- 💰 비용 관리 및 안전장치 포함
- 📊 섹션 분석 및 자동 최적화
"""

from typing import Dict, List, Optional, Union, Tuple, Any
import streamlit as st
import os
from datetime import datetime, timedelta
import json
from anthropic import Anthropic
import time
from pathlib import Path
from card_news.test_mode_generator import TestModeGenerator
# from watch_interested_articles import load_interested_articles, save_generated_card_news
from card_news.section_selector import SectionSelector
from card_news.section_config import SectionConfig
from card_news.analytics_integration import AnalyticsDashboard

# 타입 시스템 import 추가
from card_news.types import (
    Article, Section, ThemeData, GenerationRequest,
    SectionList, MixedSectionData
)
from card_news.validators import (
    DataValidator, TypeGuard, ensure_string, 
    normalize_sections, sanitize_key
)
from card_news.decorators import (
    validate_inputs, fully_validated, safe_dict_access,
    ensure_string_params, normalize_section_output
)

from dotenv import load_dotenv

st.set_page_config(
    page_title="⚡ 전력산업 카드뉴스 생성기",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)
    
# 비용 상수 (2025년 6월 기준)
COST_PER_REQUEST = 0.555  # USD
COST_PER_REQUEST_KRW = 750  # KRW

# CSS 스타일 (기존 스타일 유지 + 추가)
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
    .analytics-insight {
        background: #e0f2fe;
        border: 1px solid #0284c7;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

class CostManager:
    """비용 관리 클래스"""
    
    def __init__(self):
        self.cost_file = 'cost_tracking.json'
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
    
    def add_cost(self, amount: float):
        """비용 추가"""
        today = date.today().isoformat()
        month = date.today().strftime('%Y-%m')
        
        # 일일 비용
        if today not in self.costs['daily']:
            self.costs['daily'][today] = 0
        self.costs['daily'][today] += amount
        
        # 월간 비용
        if month not in self.costs['monthly']:
            self.costs['monthly'][month] = 0
        self.costs['monthly'][month] += amount
        
        # 총 비용
        self.costs['total'] += amount
        
        self.save_costs()
    
    def get_daily_cost(self) -> float:
        """오늘 사용한 비용"""
        today = date.today().isoformat()
        return self.costs['daily'].get(today, 0)
    
    def get_monthly_cost(self) -> float:
        """이번 달 사용한 비용"""
        month = date.today().strftime('%Y-%m')
        return self.costs['monthly'].get(month, 0)
    
    def can_generate(self, daily_limit: float = 10, monthly_limit: float = 50) -> tuple:
        """생성 가능 여부 확인"""
        daily = self.get_daily_cost()
        monthly = self.get_monthly_cost()
        
        if daily + COST_PER_REQUEST > daily_limit:
            return False, f"일일 한도 초과: ${daily:.2f} / ${daily_limit}"
        
        if monthly + COST_PER_REQUEST > monthly_limit:
            return False, f"월간 한도 초과: ${monthly:.2f} / ${monthly_limit}"
        
        return True, "생성 가능"

class CardNewsGenerator:
    """카드뉴스 생성기"""
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.cost_manager = CostManager()
        self.analytics_dashboard = AnalyticsDashboard()  # 분석 대시보드 추가
        self.output_dir = Path("/mnt/c/Users/KJ/Desktop/EnhancedCardNews/detailed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @ensure_string_params('keyword')
    def get_color_theme(self, keyword: str) -> Dict[str, str]:
        """키워드에 따른 색상 테마 반환 (타입 안전)"""
        themes = {
            '재생에너지': {
                'primary': '#10b981',  # 초록
                'secondary': '#34d399',
                'gradient': 'linear-gradient(135deg, #10b981 0%, #34d399 100%)'
            },
            'ESS': {
                'primary': '#3b82f6',  # 파랑
                'secondary': '#60a5fa',
                'gradient': 'linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%)'
            },
            '전력시장': {
                'primary': '#8b5cf6',  # 보라
                'secondary': '#a78bfa',
                'gradient': 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)'
            },
            '태양광': {
                'primary': '#f59e0b',  # 노랑/주황
                'secondary': '#fbbf24',
                'gradient': 'linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%)'
            },
            '풍력': {
                'primary': '#06b6d4',  # 청록
                'secondary': '#22d3ee',
                'gradient': 'linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%)'
            },
            '정책': {
                'primary': '#ef4444',  # 빨강
                'secondary': '#f97316',  # 주황
                'gradient': 'linear-gradient(135deg, #ef4444 0%, #f97316 100%)'
            }
        }
        
        # 키워드에 매칭되는 테마 찾기
        for theme_key in themes:
            if theme_key in keyword:
                return themes[theme_key]
        
        # 기본 테마
        return {
            'primary': '#6366f1',  # 인디고
            'secondary': '#8b5cf6',  # 보라
            'gradient': 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)'
        }
    
    @fully_validated
    def generate_card_news(self, article: Union[Dict, Article], 
                          color_theme: Union[Dict, str], 
                          emphasis: Union[List[str], List[Section], MixedSectionData], 
                          optimized_sections: Optional[List[str]] = None) -> str:
        """Claude API를 통한 카드뉴스 생성 (타입 안전)"""
        
        # Article 객체로 변환
        if isinstance(article, dict):
            article = DataValidator.validate_article(article)
        
        # 섹션 정규화
        emphasis_sections = DataValidator.normalize_sections(emphasis)
        emphasis_ids = [s.id for s in emphasis_sections]
        
        # optimized_sections 정규화
        if optimized_sections:
            opt_sections = DataValidator.normalize_sections(optimized_sections)
            sections = [s.id for s in opt_sections]
        else:
            sections = emphasis_ids
        
        # 섹션 스타일 CSS 파일 읽기
        try:
            with open('card_news/section_styles.css', 'r', encoding='utf-8') as f:
                section_styles_css = f.read()
        except FileNotFoundError:
            section_styles_css = ""  # CSS 파일이 없으면 빈 문자열
            st.warning("섹션 스타일 CSS 파일을 찾을 수 없습니다.")

        # 최적화된 섹션 사용 (제공된 경우)
        sections = optimized_sections or emphasis
        
        prompt = f"""
전력산업 뉴스를 시각적으로 매력적인 HTML 카드뉴스로 변환해주세요.

기사 정보:
- 제목: {article.title}
- 요약: {article.summary}
- 핵심 내용: {article.get('content', '내용 없음')}
- 키워드: {', '.join(article.get('keywords', []))}
- 출처: {article.get('source', '전기신문')}
- URL: {article['url']}

색상 테마:
- 주 색상: {color_theme['primary']}
- 보조 색상: {color_theme['secondary']}
- 그라디언트: {color_theme['gradient']}

포함할 섹션 (순서대로):
{chr(10).join([f"- {section}" for section in sections])}

요구사항:
1. 모바일/데스크톱 반응형 디자인
2. 시각적으로 매력적인 레이아웃
3. 각 섹션은 카드 형태로 구분
4. 아이콘과 그래픽 요소 활용
5. 읽기 쉬운 타이포그래피
6. 제공된 색상 테마 활용
7. 섹션 스타일 CSS 적용

HTML 코드만 출력하세요. 설명은 불필요합니다.
반드시 <style> 태그 안에 다음 CSS를 포함하세요:
{section_styles_css}
"""
        
        try:
            message = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # 비용 기록
            self.cost_manager.add_cost(COST_PER_REQUEST)
            
            return message.content[0].text
            
        except Exception as e:
            st.error(f"카드뉴스 생성 중 오류 발생: {str(e)}")
            return None

def load_interested_articles() -> List[Dict]:
    """관심 표시된 기사 로드"""
    pending_file = 'pending_cardnews.json'
    
    if not os.path.exists(pending_file):
        return []
    
    try:
        with open(pending_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
            return articles
    except Exception as e:
        st.error(f"기사 로드 중 오류: {str(e)}")
        return []

@ensure_string_params('article_id', 'file_path')
def save_generated_card_news(article_id: str, file_path: str):
    """생성된 카드뉴스 정보 저장 (타입 안전)"""
    history_file = 'generated_cardnews_history.json'
    
    # 기존 히스토리 로드
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []
    
    # 새 항목 추가
    history.append({
        'article_id': article_id,
        'file_path': file_path,
        'generated_at': datetime.now().isoformat()
    })
    
    # 저장
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def main():
    # .env 파일 로드
    load_dotenv()
    
    st.title("⚡ 전력산업 카드뉴스 생성기")
    st.markdown("---")
    
    # 사이드바 설정
    with st.sidebar:
        st.markdown("### ⚙️ 설정")
        test_mode = st.checkbox(
            "🧪 테스트 모드",
            help="테스트 모드를 활성화하면 실제 API를 호출하지 않고 더미 카드뉴스를 생성합니다. 비용이 발생하지 않습니다."
        )
        if test_mode:
            st.info("🧪 테스트 모드 활성화됨\n실제 API 호출 없이 테스트합니다.")
        st.markdown("---")
    
    # 분석 대시보드 인스턴스
    analytics_dashboard = AnalyticsDashboard()
    
    # 탭 구성
    tabs = st.tabs(["📰 카드뉴스 생성", "📊 분석 대시보드", "💰 비용 관리", "ℹ️ 사용 안내"])
    
    # 탭 1: 카드뉴스 생성
    with tabs[0]:
        # API 키 처리 - 사이드바에서 입력받기
        with st.sidebar:
            st.markdown("### 🔑 API 설정")
            
            # 환경변수에서 기본값 로드
            env_api_key = os.getenv('ANTHROPIC_API_KEY', '')
            
            # API 키 입력 필드
            api_key = st.text_input(
                "Claude API Key",
                value=env_api_key,
                type="password",
                help="Claude API 키를 입력하세요. 환경변수가 설정되어 있으면 자동으로 로드됩니다.",
                key="anthropic_api_key"
            )
            
            if api_key:
                st.success("✅ API 키가 설정되었습니다")
            else:
                st.warning("⚠️ API 키를 입력해주세요")
            
            st.markdown("---")
        
        # API 키가 없으면 안내 메시지 표시
        if not api_key:
            st.error("⚠️ API 키가 설정되지 않았습니다!")
            st.info("""
            **API 키 설정 방법:**
            1. 왼쪽 사이드바에서 'API 설정' 섹션 확인
            2. Claude API 키 입력
            3. 또는 `.env` 파일에 `ANTHROPIC_API_KEY` 설정
            
            API 키는 [Anthropic Console](https://console.anthropic.com/)에서 발급받을 수 있습니다.
            """)
            st.stop()
        
        # 생성기 초기화
        generator = CardNewsGenerator(api_key)
        test_generator = TestModeGenerator()
        section_selector = SectionSelector()
        
        # 비용 확인
        can_generate, message = generator.cost_manager.can_generate()
        
        # 비용 정보 사이드바
        with st.sidebar:
            st.markdown("### 💰 비용 현황")
            daily_cost = generator.cost_manager.get_daily_cost()
            monthly_cost = generator.cost_manager.get_monthly_cost()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("오늘 사용", f"${daily_cost:.2f}")
            with col2:
                st.metric("이번 달", f"${monthly_cost:.2f}")
            
            if not can_generate:
                st.error(f"❌ {message}")
            else:
                st.success("✅ 생성 가능")
            
            st.markdown("---")
            st.info(f"**기사당 비용**: ${COST_PER_REQUEST} (약 {COST_PER_REQUEST_KRW}원)")
        
        # 관심 기사 로드
        articles = load_interested_articles()
        
        if not articles:
            st.warning("📭 관심 표시된 기사가 없습니다.")
            st.info("노션에서 관심 있는 기사에 체크 표시를 하면 여기에 나타납니다.")
        else:
            st.success(f"📬 {len(articles)}개의 관심 기사를 발견했습니다!")
            
            # 기사별 카드뉴스 생성
            for idx, article in enumerate(articles):
                with st.expander(f"📄 {article.title[:50]}...", expanded=True):
                    # 기사 정보
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**📅 날짜:** {article.get('date', '날짜 정보 없음')}")
                        st.markdown(f"**🏢 출처:** {article.get('source', '전기신문')}")
                        
                        # 키워드
                        keywords_html = " ".join([
                            f'<span class="keyword-tag">{kw}</span>' 
                            for kw in article.get('keywords', [])
                        ])
                        st.markdown(f"**🏷️ 키워드:** {keywords_html}", unsafe_allow_html=True)
                        
                        # 요약
                        st.markdown("**📝 요약:**")
                        st.write(article.summary)
                        
                        # 핵심 내용
                        st.markdown("**🎯 핵심 내용:**")
                        for content in [article.get('content', '내용 없음')]:
                            st.write(f"• {content}")
                    
                    with col2:
                        st.markdown("**🔗 원문 링크:**")
                        st.markdown(f"[기사 보기]({article['url']})")
                    
                    st.markdown("---")
                    
                    # 섹션 분석 인사이트 (미니 대시보드)
                    reliability_scores = analytics_dashboard.render_mini_dashboard(article.get('keywords', []))
                    
                    # 카드뉴스 생성 옵션
                    st.markdown("### 🎨 카드뉴스 생성 옵션")
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        # 색상 테마 선택
                        color_option = st.radio(
                            "색상 테마",
                            ["자동 (키워드 기반)", "수동 선택"],
                            key=f"color_{idx}"
                        )
                        
                        if color_option == "자동 (키워드 기반)":
                            # 첫 번째 키워드 기반 자동 테마
                            auto_theme = generator.get_color_theme(article.get('keywords', [])[0] if article.get('keywords', []) else '')
                            keyword = article.get("keywords", [])[0] if article.get("keywords", []) else "전력산업"
                            st.info(f"🎨 '{keyword}' 테마가 적용됩니다")
                        else:
                            # 수동 선택
                            theme_names = {
                                '재생에너지': '🌱 초록 (재생에너지)',
                                'ESS': '🔋 파랑 (ESS/배터리)',
                                '전력시장': '💜 보라 (전력시장)',
                                '태양광': '☀️ 노랑 (태양광)',
                                '풍력': '💨 청록 (풍력)',
                                '정책': '📢 빨강 (정책/규제)'
                            }
                            selected_theme = st.selectbox(
                                "테마 선택",
                                list(theme_names.keys()),
                                format_func=lambda x: theme_names[x],
                                key=f"theme_{idx}"
                            )
                            auto_theme = generator.get_color_theme(ensure_string(selected_theme))
                    
                    with col2:
                        # 섹션 선택 옵션
                        optimization_option = st.radio(
                            "섹션 구성",
                            ["자동 추천 (AI 분석)", "수동 선택"],
                            key=f"optimization_{idx}"
                        )
                        
                        if optimization_option == "자동 추천 (AI 분석)":
                            # AI 추천 섹션 사용
                            recommended_sections = section_selector.recommend_sections(
                                article,
                                num_sections=5
                            )
                            
                            # 최적화된 섹션 가져오기
                            optimized_sections, reasons = analytics_dashboard.get_optimized_sections(
                                article.get('keywords', []),
                                recommended_sections
                            )
                            
                            st.info("🤖 AI가 최적화된 섹션을 추천합니다")
                            
                            # 최적화 이유 표시
                            if reasons:
                                st.write("📋 **섹션 최적화 내역**")
                                for section, reason in reasons.items():
                                    st.write(f"• **{section}**: {reason}")
                            
                            emphasis = optimized_sections
                        else:
                            # 수동 섹션 선택
                            section_names = {k: v.get("name", k) for k, v in section_selector.config.get_all_sections().items()}
                            emphasis = st.multiselect(
                                "포함할 섹션 선택 (3-5개 권장)",
                                options=list(section_names.keys()),
                                format_func=lambda x: section_names[x],
                                default=[s[0] for s in section_selector.recommend_sections(article, num_sections=3)][:3],
                                key=f"sections_{idx}"
                            )
                    
                    st.markdown("---")
                    
                    # 생성 전 확인
                    if emphasis:
                        selected_sections_str = ", ".join([
                            SectionConfig.ALL_SECTIONS[s].get('title', s) 
                            for s in emphasis
                        ])
                        st.info(f"**선택된 섹션**: {selected_sections_str}")
                        
                        # 비용 경고
                        st.markdown('<div class="cost-warning">', unsafe_allow_html=True)
                        st.markdown(f"⚠️ **비용 안내**: 카드뉴스 생성 시 ${COST_PER_REQUEST} (약 {COST_PER_REQUEST_KRW}원)이 청구됩니다.")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # 동의 체크박스
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            confirm = st.checkbox(
                                "비용을 확인했으며, 카드뉴스 생성에 동의합니다.",
                                key=f"confirm_{idx}"
                            )
                        
                        with col2:
                            if st.button(
                                f"🎨 카드뉴스 생성", 
                                key=f"generate_{idx}", 
                                type="primary",
                                disabled=not confirm or not can_generate
                            ):
                                with st.spinner("🎨 카드뉴스 생성 중..." + (" (테스트 모드)" if test_mode else " (30초~1분 소요)")):
                                    # 카드뉴스 생성
                                    if test_mode:
                                        # 테스트 모드: 더미 HTML 생성
                                        html_content = test_generator.generate_test_card_news(
                                            article, auto_theme, emphasis
                                        )
                                        # 비용 없음
                                        st.warning("🧪 테스트 모드로 생성되었습니다. 실제 API는 호출되지 않았습니다.")
                                    else:
                                        # 실제 모드: API 호출
                                        html_content = generator.generate_card_news(
                                            article, auto_theme, emphasis,
                                            optimized_sections=emphasis if optimization_option == "자동 추천 (AI 분석)" else None
                                        )
                                    
                                    if html_content:
                                        if test_mode:
                                            st.success("✅ 테스트 카드뉴스 생성 완료! (비용: $0.00)")
                                    else:
                                        if test_mode:
                                            st.success("✅ 테스트 카드뉴스 생성 완료! (비용: $0.00)")
                                        else:
                                            st.success(f"✅ 카드뉴스 생성 완료! (비용: ${COST_PER_REQUEST})")
                                        st.balloons()
                                        
                                        # 분석 데이터 저장
                                        section_selector.save_selection_analytics(ensure_string(article.get('page_id', article.get('id', ''))), emphasis)
                                        
                                        # 미리보기
                                        st.markdown("### 👁️ 미리보기")
                                        st.components.v1.html(html_content, height=800, scrolling=True)
                                        
                                        # 다운로드 버튼
                                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                        filename = f"card_news_{article.get('page_id', article.get('id', ''))}_{timestamp}.html"
                                        
                                        st.download_button(
                                            label="📥 HTML 파일 다운로드",
                                            data=html_content,
                                            file_name=filename,
                                            mime="text/html"
                                        )
                                        
                                        # 파일을 detailed 폴더에 자동 저장
                                        detailed_dir = generator.output_dir
                                        detailed_dir.mkdir(exist_ok=True)
                                        
                                        file_path = detailed_dir / filename
                                        with open(file_path, 'w', encoding='utf-8') as f:
                                            f.write(html_content)
                                        
                                        save_generated_card_news(article.get('page_id', article.get('id', '')), str(file_path))
                                        
                                        # 요약 페이지에 추가
                                        try:
                                            if add_to_summary(article, str(file_path), str(generator.output_dir)):
                                                st.success("📝 요약 페이지에 추가되었습니다!")
                                                update_summary_date()
                                        except Exception as e:
                                            st.warning(f"요약 페이지 업데이트 실패: {e}")
                                        
                                        # 품질 피드백 UI
                                        with st.expander("💬 카드뉴스 품질 평가", expanded=True):
                                            analytics_dashboard.render_quality_feedback(
                                                article.get('page_id', article.get('id', '')), 
                                                emphasis
                                            )
                    else:
                        st.warning("⚠️ 포함할 섹션을 선택해주세요.")
    
    # 탭 2: 분석 대시보드
    with tabs[1]:
        analytics_dashboard.render_full_dashboard()
    
    # 탭 3: 비용 관리
    with tabs[2]:
        st.header("💰 비용 관리")
        
        cost_manager = CostManager()
        
        # 현재 비용 현황
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "오늘 사용액",
                f"${cost_manager.get_daily_cost():.2f}",
                f"한도: $10"
            )
        
        with col2:
            st.metric(
                "이번 달 사용액",
                f"${cost_manager.get_monthly_cost():.2f}",
                f"한도: $50"
            )
        
        with col3:
            st.metric(
                "누적 사용액",
                f"${cost_manager.costs['total']:.2f}"
            )
        
        # 사용 내역
        st.markdown("### 📊 일별 사용 내역")
        if cost_manager.costs['daily']:
            daily_data = [
                {"날짜": date, "비용($)": cost, "비용(원)": int(cost * 1370)}
                for date, cost in sorted(cost_manager.costs['daily'].items(), reverse=True)[:10]
            ]
            st.dataframe(daily_data, hide_index=True, use_container_width=True)
        else:
            st.info("아직 사용 내역이 없습니다.")
        
        # 월별 통계
        st.markdown("### 📈 월별 통계")
        if cost_manager.costs['monthly']:
            import pandas as pd
            monthly_df = pd.DataFrame([
                {"월": month, "비용($)": cost, "비용(원)": int(cost * 1370)}
                for month, cost in sorted(cost_manager.costs['monthly'].items())
            ])
            st.bar_chart(monthly_df.set_index('월')['비용($)'])
    
    # 탭 4: 사용 안내
    with tabs[3]:
        st.header("ℹ️ 사용 안내")
        
        st.markdown("""
        ### 🚀 빠른 시작
        
        1. **노션에서 관심 기사 선택**
           - 전력 산업 뉴스 데이터베이스에서 관심 있는 기사에 체크
           
        2. **카드뉴스 생성**
           - '카드뉴스 생성' 탭에서 기사 확인
           - 색상 테마와 섹션 구성 선택
           - 생성 버튼 클릭
        
        3. **품질 평가**
           - 생성된 카드뉴스의 품질을 평가
           - AI가 학습하여 점점 더 나은 결과 제공
        
        ### 📊 분석 대시보드 활용
        
        - **섹션 신뢰도**: 각 섹션의 성능 확인
        - **키워드 매칭**: 키워드별 최적 섹션 확인
        - **사용 추이**: 시간별 섹션 사용 패턴 분석
        - **개선 제안**: AI 기반 개선 사항 확인
        
        ### 💰 비용 정보
        
        - **기사당 비용**: $0.555 (약 750원)
        - **일일 한도**: $10
        - **월간 한도**: $50
        
        ### 🎨 섹션 종류
        
        - **개요/배경**: 주제 소개 및 배경 설명
        - **기술 상세**: 기술적 세부사항
        - **통계/수치**: 데이터와 통계 정보
        - **정책/규제**: 관련 정책 및 규제
        - **시장 동향**: 시장 분석 및 트렌드
        - **사례 연구**: 실제 적용 사례
        - **미래 전망**: 향후 전망 및 예측
        
        ### ⚡ 팁
        
        - 키워드에 맞는 색상 테마를 선택하면 더 시각적으로 매력적인 결과
        - AI 추천 섹션을 활용하면 더 적합한 구성 가능
        - 정기적인 품질 평가로 AI 성능 향상
        """)

if __name__ == "__main__":
    main()
