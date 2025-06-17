#!/usr/bin/env python3
"""
하이브리드 방식 구현 예시
Streamlit + 로컬 웹서버 조합
"""
import streamlit as st
import subprocess
import socket
import time
from pathlib import Path
import webbrowser
import threading

class HybridCardNewsSystem:
    """하이브리드 카드뉴스 시스템"""
    
    def __init__(self):
        self.server_port = self.find_free_port()
        self.server_process = None
        self.base_url = f"http://localhost:{self.server_port}"
        
    def find_free_port(self):
        """사용 가능한 포트 찾기"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    def start_local_server(self):
        """백그라운드에서 로컬 웹서버 시작"""
        if self.server_process is None:
            # Python 내장 웹서버 사용
            cmd = [
                "python3", "-m", "http.server", 
                str(self.server_port),
                "--directory", "output/card_news"
            ]
            self.server_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            time.sleep(1)  # 서버 시작 대기
            return True
        return False
    
    def stop_server(self):
        """서버 종료"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None

def render_hybrid_summary_tab():
    """하이브리드 요약 탭 - 미리보기 + 외부 링크"""
    
    # 서버 관리
    if 'card_server' not in st.session_state:
        st.session_state.card_server = HybridCardNewsSystem()
        st.session_state.card_server.start_local_server()
    
    server = st.session_state.card_server
    
    # 헤더
    st.markdown("## 📰 전력산업 카드뉴스")
    
    # 서버 상태 표시
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"🌐 로컬 서버: {server.base_url}")
    with col2:
        if st.button("🔄 서버 재시작"):
            server.stop_server()
            server.start_local_server()
            st.rerun()
    
    # 카드 목록 로드
    cards = load_generated_card_news()
    
    # 검색/필터 UI
    search_term = st.text_input("🔍 검색", placeholder="제목, 키워드로 검색...")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox(
            "카테고리",
            ["전체"] + list(set(card['category_name'] for card in cards))
        )
    
    # 필터링
    filtered_cards = filter_cards(cards, search_term, category_filter)
    
    # 카드 그리드 표시
    st.markdown(f"### 총 {len(filtered_cards)}개의 카드뉴스")
    
    # 3열 그리드
    cols = st.columns(3)
    for idx, card in enumerate(filtered_cards):
        with cols[idx % 3]:
            render_card_preview(card, server.base_url)

def render_card_preview(card, base_url):
    """개별 카드 미리보기 렌더링"""
    
    # 카드 컨테이너
    with st.container():
        # 카테고리 배지
        category_colors = {
            '태양광': '🟡',
            'ESS': '🔋',
            '정책': '📋',
            'VPP': '🔌',
            '재생에너지': '🌱'
        }
        emoji = category_colors.get(card['category_name'], '📰')
        st.markdown(f"{emoji} **{card['category_name']}**")
        
        # 제목
        st.markdown(f"### {card['title']}")
        
        # 요약 (접을 수 있게)
        with st.expander("📝 요약 보기", expanded=False):
            st.write(card['summary'])
        
        # 메타 정보
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"📅 {card['date']}")
        with col2:
            st.caption(f"📰 {card['source']}")
        
        # 액션 버튼들
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 미리보기 (Streamlit 내부)
            if st.button("👁️ 미리보기", key=f"preview_{card['title'][:10]}"):
                show_preview_modal(card)
        
        with col2:
            # 새 탭에서 열기
            file_path = card['file_path'].replace('output/card_news/', '')
            full_url = f"{base_url}/{file_path}"
            st.markdown(f"[🔗 새 탭]({full_url})", unsafe_allow_html=True)
        
        with col3:
            # 다운로드
            if st.button("💾", key=f"download_{card['title'][:10]}", 
                        help="다운로드"):
                provide_download(card)
        
        st.divider()

def show_preview_modal(card):
    """미리보기 모달 (간단한 버전)"""
    with st.expander(f"미리보기: {card['title']}", expanded=True):
        # 썸네일 이미지가 있다면 표시
        thumbnail_path = card['file_path'].replace('.html', '_thumb.png')
        if Path(thumbnail_path).exists():
            st.image(thumbnail_path)
        
        # 주요 내용 요약
        st.markdown("#### 주요 내용")
        st.write(card['summary'])
        
        # 키워드
        if card.get('keywords'):
            st.markdown("#### 키워드")
            keyword_html = " ".join([
                f'<span style="background:#e3f2fd; padding:5px 10px; '
                f'border-radius:15px; margin:3px;">{kw}</span>'
                for kw in card['keywords']
            ])
            st.markdown(keyword_html, unsafe_allow_html=True)
        
        # 전체 보기 링크
        file_path = card['file_path'].replace('output/card_news/', '')
        full_url = f"{st.session_state.card_server.base_url}/{file_path}"
        st.markdown(f"[📖 전체 내용 보기]({full_url})")

def provide_download(card):
    """다운로드 기능"""
    try:
        with open(card['file_path'], 'rb') as f:
            content = f.read()
        
        st.download_button(
            label="💾 다운로드 시작",
            data=content,
            file_name=f"{card['title']}.html",
            mime="text/html",
            key=f"dl_actual_{card['title'][:10]}"
        )
    except Exception as e:
        st.error(f"다운로드 실패: {str(e)}")

def filter_cards(cards, search_term, category):
    """카드 필터링"""
    filtered = cards
    
    # 검색어 필터
    if search_term:
        search_lower = search_term.lower()
        filtered = [
            card for card in filtered
            if search_lower in card['title'].lower() or
               search_lower in card['summary'].lower() or
               any(search_lower in kw.lower() for kw in card.get('keywords', []))
        ]
    
    # 카테고리 필터
    if category != "전체":
        filtered = [
            card for card in filtered
            if card['category_name'] == category
        ]
    
    return filtered

# CSS 스타일 (Streamlit 내부용)
def inject_custom_css():
    """Streamlit UI 개선을 위한 CSS"""
    st.markdown("""
    <style>
    /* 카드 스타일 */
    .stContainer > div {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .stContainer > div:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* 버튼 스타일 개선 */
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        font-size: 14px;
    }
    
    /* 링크 스타일 */
    a {
        text-decoration: none;
        color: #1976d2;
        font-weight: 600;
    }
    
    a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

# 사용 예시
if __name__ == "__main__":
    st.set_page_config(
        page_title="전력산업 카드뉴스",
        page_icon="⚡",
        layout="wide"
    )
    
    inject_custom_css()
    render_hybrid_summary_tab()
