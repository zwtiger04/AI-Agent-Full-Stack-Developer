"""
요약 카드뉴스 Streamlit UI 컴포넌트
"""
import streamlit as st
from datetime import datetime, timedelta
from summary_manager import SummaryManager
from pathlib import Path

def render_summary_tab():
    """요약 카드뉴스 탭 렌더링"""
    manager = SummaryManager()
    
    # 헤더
    st.header("📚 전력산업 카드뉴스 모음")
    st.markdown("생성된 모든 카드뉴스를 한눈에 보고 관리할 수 있습니다.")
    
    # 필터 섹션
    st.subheader("🔍 필터 및 검색")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categories = ["전체"] + manager.get_categories()
        category_filter = st.selectbox("📁 카테고리", categories)
    
    with col2:
        date_option = st.selectbox("📅 기간", 
                                  ["전체", "오늘", "최근 7일", "최근 30일", "사용자 지정"])
        
        # 사용자 지정 날짜 범위
        date_range = None
        if date_option == "사용자 지정":
            date_range = st.date_input("날짜 범위", 
                                       value=(datetime.now() - timedelta(days=30), 
                                             datetime.now()),
                                       key="date_range")
    
    with col3:
        search_term = st.text_input("🔎 검색", placeholder="제목, 요약, 키워드 검색...")
    
    # 카테고리 필터 적용
    filter_category = None if category_filter == "전체" else category_filter
    
    # 카드 로드 및 필터링
    cards = manager.filter_cards(category=filter_category, 
                                date_range=date_range,
                                search=search_term)
    
    # 결과 표시
    st.markdown("---")
    st.subheader(f"📰 카드뉴스 ({len(cards)}개)")
    
    if not cards:
        st.info("조건에 맞는 카드뉴스가 없습니다.")
        return
    
    # 카드 그리드 표시
    display_card_grid(cards)

def display_card_grid(cards):
    """카드를 그리드 형태로 표시"""
    # 3열 그리드
    cols_per_row = 3
    
    for i in range(0, len(cards), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, col in enumerate(cols):
            if i + j < len(cards):
                card = cards[i + j]
                
                with col:
                    # 카드 컨테이너
                    with st.container():
                        # 카테고리 배지
                        category = card.get('category', '기타')
                        category_color = get_category_color(category)
                        st.markdown(f"""
                        <span style="background-color: {category_color}; 
                                    color: white; 
                                    padding: 2px 8px; 
                                    border-radius: 4px; 
                                    font-size: 12px;">
                            {category}
                        </span>
                        """, unsafe_allow_html=True)
                        
                        # 제목
                        st.markdown(f"**{card['title']}**")
                        
                        # 요약 (최대 100자)
                        summary = card.get('summary', '')[:100]
                        if len(card.get('summary', '')) > 100:
                            summary += "..."
                        st.caption(summary)
                        
                        # 키워드
                        keywords = card.get('keywords', [])
                        if keywords:
                            keyword_text = " · ".join(f"#{kw}" for kw in keywords[:3])
                            st.caption(f"🏷️ {keyword_text}")
                        
                        # 날짜
                        date = card.get('date', '')
                        if date:
                            st.caption(f"📅 {date}")
                        
                        # 상세보기 버튼
                        file_path = card.get('file_path', '')
                        if file_path:
                            # 파일 경로 구성
                            full_path = Path("output/card_news/html") / file_path
                            
                            if full_path.exists():
                                # 파일을 새 탭에서 열기 위한 JavaScript
                                st.markdown(f"""
                                <a href="/{full_path}" target="_blank" 
                                   style="text-decoration: none;">
                                    <button style="background-color: #4CAF50; 
                                                  color: white; 
                                                  border: none; 
                                                  padding: 8px 16px; 
                                                  border-radius: 4px; 
                                                  cursor: pointer;">
                                        📖 상세보기
                                    </button>
                                </a>
                                """, unsafe_allow_html=True)
                            else:
                                st.caption("⚠️ 파일을 찾을 수 없음")
                        
                        st.markdown("---")

def get_category_color(category):
    """카테고리별 색상 반환"""
    colors = {
        "ESS": "#FF6B6B",
        "VPP": "#4ECDC4", 
        "재생에너지": "#45B7D1",
        "태양광": "#FFA500",
        "풍력": "#98D8C8",
        "전력시장": "#F06292",
        "정책": "#7E57C2",
        "투자": "#5C6BC0",
        "기술": "#42A5F5",
        "시장": "#26A69A"
    }
    return colors.get(category, "#78909C")  # 기본 색상

# 테스트
if __name__ == "__main__":
    st.set_page_config(page_title="카드뉴스 요약", layout="wide")
    render_summary_tab()
