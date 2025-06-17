"""
요약 카드뉴스 Streamlit UI - HTML 임베드 버전
기존 improved_summary.html의 스타일을 그대로 유지
"""
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from summary_manager import SummaryManager
import re

def render_summary_tab():
    """요약 카드뉴스 탭 렌더링 - HTML 임베드 방식"""
    
    # HTML 파일 경로
    html_path = Path("output/card_news/summary/improved_summary.html")
    
    if not html_path.exists():
        st.error("요약 페이지를 찾을 수 없습니다.")
        return
    
    # HTML 읽기
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Streamlit에서 작동하도록 경로 수정
    # onclick 이벤트를 Streamlit 링크로 변경
    modified_html = html_content
    
    # 링크 클릭을 처리할 JavaScript 추가
    js_script = """
    <script>
    function openDetailPage(path) {
        // 새 탭에서 열기 위한 전체 경로 구성
        const basePath = window.location.origin;
        const fullPath = basePath + '/output/card_news/html/' + path;
        window.open(fullPath, '_blank');
    }
    </script>
    """
    
    # onclick 이벤트 수정
    modified_html = re.sub(
        r"onclick=\"window\.location\.href='../html/([^']+)'\"",
        r'onclick="openDetailPage(\'\1\')"',
        modified_html
    )
    
    # head 태그 끝에 스크립트 삽입
    modified_html = modified_html.replace('</head>', js_script + '</head>')
    
    # 전체 화면으로 표시
    st.markdown("""
    <style>
    .stApp > main > div {
        padding-top: 0;
        padding-left: 0;
        padding-right: 0;
    }
    .block-container {
        padding: 0;
        max-width: 100%;
    }
    iframe {
        width: 100%;
        min-height: 1200px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # HTML 임베드
    components.html(modified_html, height=1200, scrolling=True)
    
    # 또는 더 간단한 방법: iframe으로 직접 표시
    # st.markdown(f'<iframe src="file://{html_path.absolute()}" width="100%" height="1200"></iframe>', unsafe_allow_html=True)

def render_summary_tab_alternative():
    """대안: 기존 HTML을 Streamlit 스타일로 재현"""
    
    # CSS 스타일 적용
    st.markdown("""
    <style>
    /* 다크 테마 배경 */
    .stApp {
        background-color: #0f0f0f;
    }
    
    /* 헤더 스타일 */
    .summary-header {
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 30px;
        margin-bottom: 40px;
        color: white;
    }
    
    /* 카드 스타일 */
    .news-card-st {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        cursor: pointer;
        color: white;
    }
    
    .news-card-st:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    
    .category-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 15px;
    }
    
    .category-ess { background: rgba(102, 126, 234, 0.2); color: #667eea; }
    .category-solar { background: rgba(255, 193, 7, 0.2); color: #ffc107; }
    .category-policy { background: rgba(76, 175, 80, 0.2); color: #4caf50; }
    .category-market { background: rgba(244, 67, 54, 0.2); color: #f44336; }
    .category-tech { background: rgba(156, 39, 176, 0.2); color: #9c27b0; }
    </style>
    """, unsafe_allow_html=True)
    
    # 헤더
    st.markdown("""
    <div class="summary-header">
        <h1 style="font-size: 48px; margin-bottom: 20px;">전력산업 주요 뉴스</h1>
        <p style="font-size: 20px;">2025년 6월 11일 | 에너지 전환의 현장을 전합니다</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 카드 표시 로직...

# 기본 함수는 임베드 방식 사용
render_summary_tab = render_summary_tab
