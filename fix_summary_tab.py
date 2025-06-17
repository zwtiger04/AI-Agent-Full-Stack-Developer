import streamlit.components.v1 as components
import base64
from pathlib import Path

def render_summary_tab():
    """요약 카드뉴스 탭 - 완벽한 HTML 임베딩"""
    
    # 옵션 선택
    render_option = st.radio(
        "렌더링 방식",
        ["컴포넌트 (추천)", "iframe", "직접 임베딩"],
        horizontal=True,
        key="render_option"
    )
    
    # 카드뉴스 데이터 로드
    card_news_list = load_generated_card_news()
    
    # 필터 UI
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        search_query = st.text_input("🔍 카드뉴스 검색", key="summary_search")
    with col2:
        category_filter = st.selectbox("📁 카테고리", ["전체", "ESS", "태양광", "정책", "시장", "기술", "VPP", "재생에너지"], key="summary_category")
    with col3:
        sort_order = st.selectbox("정렬", ["최신순", "오래된순"], key="summary_sort")
    
    # 필터링
    filtered_list = filter_card_news(card_news_list, search_query, category_filter)
    if sort_order == "오래된순":
        filtered_list.reverse()
    
    # HTML 생성
    html_content = generate_full_html(filtered_list)
    
    # 선택한 방식으로 렌더링
    if render_option == "컴포넌트 (추천)":
        components.html(html_content, height=1200, scrolling=True)
    
    elif render_option == "iframe":
        # Base64 인코딩
        b64 = base64.b64encode(html_content.encode()).decode()
        iframe_html = f'<iframe src="data:text/html;base64,{b64}" width="100%" height="1200" frameborder="0"></iframe>'
        st.markdown(iframe_html, unsafe_allow_html=True)
    
    else:  # 직접 임베딩
        # CSS 우선순위 강화
        enhanced_css = """
        <style>
            /* Streamlit 기본 스타일 오버라이드 */
            .stApp { background-color: #0f0f0f !important; }
            section[data-testid="stSidebar"] { background-color: #1a1a1a !important; }
            .main .block-container { padding: 0 !important; max-width: 100% !important; }
            
            /* 그리드 강제 적용 */
            .news-grid {
                display: grid !important;
                grid-template-columns: repeat(3, 1fr) !important;
                gap: 30px !important;
                width: 100% !important;
                max-width: 1200px !important;
                margin: 0 auto !important;
            }
            
            @media (max-width: 1200px) {
                .news-grid { grid-template-columns: repeat(2, 1fr) !important; }
            }
            
            @media (max-width: 768px) {
                .news-grid { grid-template-columns: 1fr !important; }
            }
        </style>
        """
        st.markdown(enhanced_css + html_content, unsafe_allow_html=True)


def generate_full_html(card_list):
    """완전한 HTML 문서 생성"""
    
    # CSS 파일 읽기
    css_path = Path('output/card_news/templates/summary_style.css')
    if css_path.exists():
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
    else:
        css_content = ""
    
    # HTML 템플릿
    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>전력산업 카드뉴스</title>
        <style>{css_content}</style>
    </head>
    <body>
        <div class="container">
            {create_summary_header(len(card_list))}
            {create_stats_section(card_list) if card_list else ""}
            {create_card_grid(card_list) if card_list else '<p style="text-align:center; color:#888;">검색 결과가 없습니다.</p>'}
        </div>
    </body>
    </html>
    """
    
    return html
