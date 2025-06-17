"""
요약 카드뉴스 Streamlit UI - 수정된 버전
"""
import streamlit as st
from summary_manager import SummaryManager
from pathlib import Path
import webbrowser
import subprocess
import platform

def render_summary_tab():
    """요약 카드뉴스 탭 렌더링"""
    manager = SummaryManager()
    
    # 기존 improved_summary.html 스타일 적용
    st.markdown("""
    <style>
    /* 다크 테마 */
    .stApp {
        background-color: #0f0f0f !important;
    }
    
    /* 메인 컨테이너 */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
    }
    
    /* 헤더 스타일 */
    .main-header {
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 30px;
        margin: -2rem -1rem 2rem -1rem;
        color: white;
    }
    
    .main-header h1 {
        font-size: 48px;
        margin-bottom: 20px;
        color: white;
    }
    
    /* 통계 섹션 */
    .stats-section {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 40px;
        text-align: center;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 30px;
        margin-top: 30px;
    }
    
    .stat-item {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 15px;
        padding: 25px;
        transition: all 0.3s ease;
    }
    
    .stat-item:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: scale(1.05);
    }
    
    .stat-number {
        font-size: 36px;
        font-weight: 900;
        color: #667eea;
        margin-bottom: 10px;
    }
    
    /* 카드 스타일 */
    .news-card-container {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .news-card-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .news-card-container:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    
    .news-card-container:hover::before {
        transform: scaleX(1);
    }
    
    /* 카테고리 배지 */
    .category-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 15px;
        color: white;
    }
    
    .category-ess { background: rgba(255, 107, 107, 0.8); }
    .category-vpp { background: rgba(78, 205, 196, 0.8); }
    .category-태양광 { background: rgba(255, 165, 0, 0.8); }
    .category-풍력 { background: rgba(152, 216, 200, 0.8); }
    .category-정책 { background: rgba(126, 87, 194, 0.8); }
    .category-기술 { background: rgba(66, 165, 245, 0.8); }
    .category-시장 { background: rgba(38, 166, 154, 0.8); }
    
    /* 제목 및 텍스트 */
    .card-title {
        font-size: 22px;
        font-weight: 700;
        color: white;
        margin-bottom: 15px;
        line-height: 1.4;
    }
    
    .card-summary {
        font-size: 16px;
        color: #cccccc;
        line-height: 1.8;
        margin-bottom: 20px;
    }
    
    .card-meta {
        color: #888888;
        font-size: 14px;
        padding-top: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* 필터 섹션 */
    .filter-section {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 40px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 헤더
    st.markdown("""
    <div class="main-header">
        <h1>전력산업 주요 뉴스</h1>
        <p style="font-size: 20px; color: rgba(255, 255, 255, 0.9);">
            2025년 6월 11일 | 에너지 전환의 현장을 전합니다
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 카드 로드
    cards = manager.load_cards()
    
    # 통계 섹션
    st.markdown('<div class="stats-section">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #667eea; font-size: 28px; margin-bottom: 30px;">오늘의 주요 지표</h2>', unsafe_allow_html=True)
    
    # 통계 계산
    total_cards = len(cards)
    category_counts = {}
    for card in cards:
        cat = card.get('category', '기타')
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # 통계 그리드
    cols = st.columns(4)
    with cols[0]:
        st.markdown(f"""
        <div class="stat-item">
            <div class="stat-number">{total_cards}</div>
            <div style="color: #aaa;">전체 기사</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 상위 3개 카테고리
    top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    for i, (cat, count) in enumerate(top_categories):
        with cols[i+1]:
            st.markdown(f"""
            <div class="stat-item">
                <div class="stat-number">{count}</div>
                <div style="color: #aaa;">{cat} 관련</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 필터 섹션
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.subheader("🔍 필터 및 검색")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categories = ["전체"] + manager.get_categories()
        category_filter = st.selectbox("📁 카테고리", categories)
    
    with col2:
        date_option = st.selectbox("📅 기간", ["전체", "오늘", "최근 7일", "최근 30일"])
    
    with col3:
        search_term = st.text_input("🔎 검색", placeholder="제목, 요약, 키워드 검색...")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 필터링
    filter_category = None if category_filter == "전체" else category_filter
    filtered_cards = manager.filter_cards(category=filter_category, search=search_term)
    
    # 카드 표시
    st.markdown("---")
    st.subheader(f"📰 카드뉴스 ({len(filtered_cards)}개)")
    
    # 카드 그리드
    for card in filtered_cards:
        with st.container():
            st.markdown('<div class="news-card-container">', unsafe_allow_html=True)
            
            # 카테고리
            category = card.get('category', '기타')
            category_class = f"category-{category.lower().replace(' ', '-')}"
            st.markdown(f'<span class="category-badge {category_class}">{category}</span>', unsafe_allow_html=True)
            
            # 제목
            st.markdown(f'<h3 class="card-title">{card["title"]}</h3>', unsafe_allow_html=True)
            
            # 요약
            summary = card.get('summary', '')[:200]
            if len(card.get('summary', '')) > 200:
                summary += "..."
            st.markdown(f'<p class="card-summary">{summary}</p>', unsafe_allow_html=True)
            
            # 메타 정보
            date = card.get('date', '')
            keywords = card.get('keywords', [])
            
            meta_html = '<div class="card-meta">'
            if date:
                meta_html += f'<span>📅 {date}</span> | '
            if keywords:
                meta_html += f'<span>🏷️ {", ".join(keywords[:3])}</span>'
            meta_html += '</div>'
            
            st.markdown(meta_html, unsafe_allow_html=True)
            
            # 상세보기 버튼
            file_path = card.get('file_path', '')
            if file_path:
                full_path = Path("output/card_news/html") / file_path
                
                if st.button(f"📖 상세보기", key=f"btn_{card.get('id', '')}"):
                    # 파일 열기 시도
                    if full_path.exists():
                        # OS별로 파일 열기
                        try:
                            if platform.system() == "Windows":
                                os.startfile(str(full_path))
                            elif platform.system() == "Darwin":  # macOS
                                subprocess.run(["open", str(full_path)])
                            else:  # Linux
                                subprocess.run(["xdg-open", str(full_path)])
                            st.success(f"✅ 상세 페이지를 열었습니다: {file_path}")
                        except Exception as e:
                            # 대안: 파일 내용을 직접 표시
                            with open(full_path, 'r', encoding='utf-8') as f:
                                html_content = f.read()
                            st.markdown("---")
                            st.markdown("### 📄 상세 내용")
                            st.components.v1.html(html_content, height=800, scrolling=True)
                    else:
                        st.error(f"⚠️ 파일을 찾을 수 없습니다: {file_path}")
            
            st.markdown('</div>', unsafe_allow_html=True)
