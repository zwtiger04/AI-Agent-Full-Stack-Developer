#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 전력산업 카드뉴스 생성기 - Streamlit UI (비용 안전장치 포함)
- 관심 기사를 시각적인 HTML 카드뉴스로 변환
- Claude AI를 활용한 자동 생성
- 💰 비용 관리 및 안전장치 포함
"""

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime, date
import anthropic
from typing import List, Dict, Optional
from update_summary import add_to_summary, update_summary_date
import re

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
    
    def get_today_cost(self) -> float:
        """오늘 사용 비용"""
        today = date.today().isoformat()
        return self.costs['daily'].get(today, 0)
    
    def get_month_cost(self) -> float:
        """이번 달 사용 비용"""
        month = date.today().isoformat()[:7]
        return self.costs['monthly'].get(month, 0)
    
    def check_limits(self, daily_limit: float, monthly_limit: float) -> Dict[str, bool]:
        """한도 확인"""
        return {
            'daily_ok': self.get_today_cost() < daily_limit,
            'monthly_ok': self.get_month_cost() < monthly_limit,
            'daily_remaining': daily_limit - self.get_today_cost(),
            'monthly_remaining': monthly_limit - self.get_month_cost()
        }


class CardNewsGenerator:
    """카드뉴스 생성 클래스"""
    
    def __init__(self):
        """초기화"""
        self.anthropic_client = None
        self.pending_file = 'pending_cardnews.json'
        self.processed_file = 'processed_articles.json'
        self.output_dir = Path("detailed")
        self.output_dir.mkdir(exist_ok=True)
        self.cost_manager = CostManager()
        
    def setup_api(self, api_key: str):
        """Claude API 설정"""
        try:
            self.anthropic_client = anthropic.Anthropic(api_key=api_key)
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
    
    def determine_color_theme(self, article: Dict) -> Dict[str, str]:
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
        
        # 강조 요소 프롬프트 생성
        emphasis_prompt = ""
        if emphasis:
            emphasis_prompt = f"\n\n특별히 강조할 요소:\n" + "\n".join([f"- {e}" for e in emphasis])
        
                prompt = f"""당신은 전력산업 전문 웹 디자이너입니다. Enhanced 스타일 가이드를 완벽히 준수하여 디폴트 양식과 동일한 품질의 HTML 카드뉴스를 생성하세요.

[기사 정보]
제목: {article['title']}
요약: {article['summary']}
핵심내용: {article['content']}
키워드: {', '.join(article.get('keywords', []))}
원문 URL: {article.get('url', '')}

[Enhanced 스타일 가이드 - 디폴트 양식 필수 준수사항]

## 1. 필수 기본 설정
```css
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
body {
    font-family: 'Pretendard', -apple-system, sans-serif;
    background: #0a0a0a;
    color: #ffffff;
    line-height: 1.8;
}
```

## 2. 색상 테마 (3색 그라데이션 필수)
현재 기사 테마:
- 주색상: {color_theme['primary']}
- 중간색: {color_theme.get('secondary', color_theme['primary'])}
- 끝색상: {color_theme.get('tertiary', color_theme['secondary'])}
- 그라데이션: {color_theme['gradient']}
- RGBA: rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 알파값)

## 3. 히어로 섹션 (복잡한 배경 효과 필수)
```css
.hero {
    background: {color_theme['gradient']};
    min-height: 500px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 80%, rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.2) 0%, transparent 50%);
    animation: float 15s ease-in-out infinite;
}
```

## 4. 홈 버튼 (우상단 고정)
```html
<a href="../improved_summary.html" class="home-button">🏠</a>
```
```css
.home-button {
    position: fixed;
    top: 30px;
    right: 30px;
    background: rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.2);
    border: 2px solid rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.5);
    backdrop-filter: blur(10px);
    z-index: 1000;
}
```

## 5. 필수 클래스명 (정확히 사용)
- container (NOT wrapper)
- section fade-in (NOT section만)
- insight-grid, insight-card, insight-icon, insight-title
- stats-grid, stat-card counter, stat-value, stat-label
- timeline, timeline-item, timeline-marker, timeline-content
- expert-quote

## 6. 카드 hover 효과
```css
.insight-card {
    background: rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.1);
    border: 1px solid rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.3);
    transition: all 0.3s;
}
.insight-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 10px 30px rgba({color_theme.get('rgba_primary', '99, 102, 241')}, 0.3);
}
```

## 7. 필수 섹션 (정확한 제목과 구조)
1. 🎯 핵심 인사이트 - insight-grid에 insight-card 3개
2. 📊 주요 성과 및 지표 - stats-grid에 stat-card 4개
3. 🌍 진행 경과 - timeline 구조
4. 💬 전문가 의견 - expert-quote
5. 🔮 시사점 및 전망 - 추가 insight-grid

## 8. 애니메이션 (자체 CSS)
```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(10deg); }
}
@keyframes countUp {
    from { opacity: 0; transform: scale(0.5); }
    to { opacity: 1; transform: scale(1); }
}
.fade-in {
    opacity: 0;
    animation: fadeInUp 0.8s ease forwards;
}
```

{emphasis_prompt}

디폴트 양식과 완전히 동일한 고품질 HTML을 생성하세요. 모든 스타일 가이드를 정확히 준수하고, 특히 클래스명과 애니메이션은 반드시 위의 코드를 사용하세요."""

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


def main():
    """메인 앱 실행"""
    st.title("⚡ 전력산업 카드뉴스 생성기")
    st.markdown("관심 기사를 아름다운 카드뉴스로 변환합니다 🎨")
    
    # 생성기 초기화
    generator = CardNewsGenerator()
    
    # 사이드바 - API 설정 및 비용 관리
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # API 키 입력
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
        today_cost = generator.cost_manager.get_today_cost()
        month_cost = generator.cost_manager.get_month_cost()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("오늘 사용", f"${today_cost:.2f}", f"≈ ₩{today_cost * 1370:.0f}")
        with col2:
            st.metric("이번 달", f"${month_cost:.2f}", f"≈ ₩{month_cost * 1370:.0f}")
        
        # 한도 체크
        limits = generator.cost_manager.check_limits(daily_limit, monthly_limit)
        
        if not limits['daily_ok']:
            st.error(f"⚠️ 일일 한도 초과!")
        else:
            st.info(f"일일 잔여: ${limits['daily_remaining']:.2f}")
            
        if not limits['monthly_ok']:
            st.error(f"⚠️ 월간 한도 초과!")
        else:
            st.info(f"월간 잔여: ${limits['monthly_remaining']:.2f}")
        
        st.divider()
        
        # 새로고침
        if st.button("🔄 기사 목록 새로고침"):
            st.rerun()
        
        # 통계
        st.header("📊 통계")
        pending = generator.load_pending_articles()
        st.metric("대기 중인 기사", f"{len(pending)}개")
        st.metric("총 누적 비용", f"${generator.cost_manager.costs['total']:.2f}")
    
    # 메인 컨텐츠
    if not api_key:
        st.info("👈 사이드바에서 API 키를 입력해주세요")
        return
    
    # 대기 중인 기사 로드
    articles = generator.load_pending_articles()
    
    if not articles:
        st.info("📭 카드뉴스로 만들 관심 기사가 없습니다.")
        st.markdown("노션에서 관심 있는 기사에 체크하면 여기에 표시됩니다.")
        return
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["📰 기사 목록", "📋 생성 기록", "💰 비용 분석"])
    
    with tab1:
        st.header("📰 관심 기사 목록")
        
        # 한도 확인
        limits = generator.cost_manager.check_limits(daily_limit, monthly_limit)
        if not limits['daily_ok'] or not limits['monthly_ok']:
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
                    auto_theme = generator.determine_color_theme(article)
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
                st.markdown(f"""
                <div class="cost-warning">
                    <strong>💰 비용 안내</strong><br>
                    이 카드뉴스를 생성하면 <strong>${COST_PER_REQUEST}</strong> (약 {COST_PER_REQUEST_KRW}원)의 비용이 발생합니다.<br>
                    오늘 사용: ${today_cost:.2f} / ${daily_limit:.2f}<br>
                    이번 달: ${month_cost:.2f} / ${monthly_limit:.2f}
                </div>
                """, unsafe_allow_html=True)
                
                # 생성 버튼 (한도 확인)
                if limits['daily_ok'] and limits['monthly_ok']:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        confirm = st.checkbox(f"비용 ${COST_PER_REQUEST} 발생을 확인했습니다", key=f"confirm_{idx}")
                    
                    with col2:
                        if st.button(
                            f"🎨 카드뉴스 생성", 
                            key=f"generate_{idx}", 
                            type="primary",
                            disabled=not confirm
                        ):
                            with st.spinner("🎨 카드뉴스 생성 중... (30초~1분 소요)"):
                                # 카드뉴스 생성
                                html_content = generator.generate_card_news(
                                    article, auto_theme, emphasis
                                )
                                
                                if html_content:
                                    st.success(f"✅ 카드뉴스 생성 완료! (비용: ${COST_PER_REQUEST})")
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
                                        filename = f"detail_{safe_title}_{timestamp}.html"
                                        filepath = generator.output_dir / filename
                                        
                                        if st.button("💾 저장", key=f"save_{idx}"):
                                            with open(filepath, 'w', encoding='utf-8') as f:
                                                f.write(html_content)
                                            
                                            st.success(f"✅ 저장 완료: {filename}")
                                            
                                            # 처리 완료 표시
                                            generator.mark_as_processed(article['page_id'])
                                            st.rerun()
                                    
                                    # 파일을 detailed 폴더에 자동 저장
                                    detailed_dir = Path("detailed")
                                    detailed_dir.mkdir(exist_ok=True)
                                    
                                    file_path = detailed_dir / filename
                                    with open(file_path, 'w', encoding='utf-8') as f:
                                        f.write(html_content)
                                    
                                    st.info(f"📁 파일이 자동 저장되었습니다: {file_path}")
                                    
                                    # 요약 페이지에 추가
                                    try:
                                        if add_to_summary(article, str(file_path)):
                                            st.success("📝 요약 페이지에 추가되었습니다!")
                                            update_summary_date()
                                    except Exception as e:
                                        st.warning(f"요약 페이지 업데이트 실패: {e}")
                                    
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
    
    with tab3:
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


if __name__ == "__main__":
    main()
