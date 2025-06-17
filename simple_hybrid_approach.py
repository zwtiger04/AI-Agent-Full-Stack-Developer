#!/usr/bin/env python3
"""
간단한 하이브리드 방식 - 외부 파일 직접 열기
"""
import streamlit as st
from pathlib import Path
import os
import platform

def render_simple_hybrid_tab():
    """간단한 하이브리드 요약 탭"""
    
    st.markdown("## 📰 전력산업 카드뉴스")
    
    # 안내 메시지
    with st.info("💡 사용 방법"):
        st.markdown("""
        1. **미리보기**: 카드의 요약 정보를 확인
        2. **파일 열기**: 파일 탐색기에서 직접 열기
        3. **경로 복사**: 경로를 복사해서 브라우저에 붙여넣기
        """)
    
    # 카드 목록 로드
    cards = load_generated_card_news()
    
    # 필터 UI
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 검색", placeholder="제목 또는 키워드...")
    with col2:
        view_mode = st.radio("보기 모드", ["카드", "리스트"], horizontal=True)
    
    # 필터링
    if search:
        cards = [c for c in cards if search.lower() in c['title'].lower()]
    
    # 표시 모드에 따라 렌더링
    if view_mode == "카드":
        render_card_grid(cards)
    else:
        render_list_view(cards)

def render_card_grid(cards):
    """카드 그리드 뷰"""
    cols = st.columns(2)  # 2열로 표시
    
    for idx, card in enumerate(cards):
        with cols[idx % 2]:
            with st.container():
                # 카드 헤더
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {card['title']}")
                with col2:
                    st.caption(card['category_name'])
                
                # 요약
                st.markdown(card['summary'][:150] + "...")
                
                # 액션 영역
                with st.container():
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # 파일 위치 표시
                        if st.button("📁 위치", key=f"loc_{idx}"):
                            show_file_location(card)
                    
                    with col2:
                        # 파일 열기 (OS 기본 프로그램)
                        if st.button("🖱️ 열기", key=f"open_{idx}"):
                            open_file_in_system(card)
                    
                    with col3:
                        # 복사 가능한 경로
                        if st.button("📋 복사", key=f"copy_{idx}"):
                            show_copyable_path(card)
                
                st.divider()

def render_list_view(cards):
    """리스트 뷰 - 더 많은 정보 표시"""
    for idx, card in enumerate(cards):
        with st.expander(f"📄 {card['title']}", expanded=False):
            # 상세 정보
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**요약:**")
                st.write(card['summary'])
                
                st.markdown("**키워드:**")
                keywords = " • ".join(card.get('keywords', []))
                st.caption(keywords)
            
            with col2:
                st.markdown("**정보:**")
                st.caption(f"📅 {card['date']}")
                st.caption(f"📰 {card['source']}")
                st.caption(f"🏷️ {card['category_name']}")
            
            # 파일 정보
            st.markdown("---")
            file_info = get_file_info(card['file_path'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("파일 크기", file_info['size'])
            with col2:
                st.metric("생성일", file_info['created'])
            with col3:
                if st.button("🔗 열기", key=f"list_open_{idx}"):
                    open_file_in_system(card)

def show_file_location(card):
    """파일 위치 표시"""
    abs_path = os.path.abspath(card['file_path'])
    
    # WSL 경로를 Windows 경로로 변환
    if platform.system() == "Linux" and "/mnt/c" not in abs_path:
        win_path = f"\\\\wsl$\\Ubuntu{abs_path}"
    else:
        win_path = abs_path
    
    st.info(f"📁 파일 위치:\n```\n{win_path}\n```")

def open_file_in_system(card):
    """시스템 기본 프로그램으로 파일 열기"""
    try:
        abs_path = os.path.abspath(card['file_path'])
        
        # OS별 명령어
        if platform.system() == "Darwin":  # macOS
            os.system(f"open '{abs_path}'")
        elif platform.system() == "Linux":  # Linux/WSL
            # WSL에서 Windows 브라우저로 열기
            win_path = abs_path.replace("/home", "\\\\wsl$\\Ubuntu\\home")
            os.system(f"cmd.exe /c start {win_path}")
        else:  # Windows
            os.startfile(abs_path)
        
        st.success("✅ 파일을 여는 중...")
        
    except Exception as e:
        st.error(f"❌ 파일을 열 수 없습니다: {str(e)}")
        # 대안 제시
        show_alternative_methods(card)

def show_copyable_path(card):
    """복사 가능한 경로 표시"""
    abs_path = os.path.abspath(card['file_path'])
    
    # 다양한 형식 제공
    paths = {
        "절대 경로": abs_path,
        "WSL Windows 경로": f"\\\\wsl$\\Ubuntu{abs_path}",
        "파일 URL": f"file:///{abs_path}",
        "브라우저용": f"file://wsl$/Ubuntu{abs_path}"
    }
    
    st.markdown("**📋 복사할 경로 선택:**")
    for name, path in paths.items():
        st.code(path, language=None)

def show_alternative_methods(card):
    """대안 방법 제시"""
    st.markdown("### 🔧 다른 방법으로 열기:")
    
    tabs = st.tabs(["방법 1: 파일 탐색기", "방법 2: 웹 서버", "방법 3: 다운로드"])
    
    with tabs[0]:
        st.markdown("""
        1. Windows 파일 탐색기 열기 (Win + E)
        2. 주소창에 다음 입력:
        ```
        \\\\wsl$\\Ubuntu\\home\\zwtiger\\AI-Agent-Full-Stack-Developer
        ```
        3. `output/card_news/html` 폴더로 이동
        4. 원하는 HTML 파일 더블클릭
        """)
    
    with tabs[1]:
        st.markdown("""
        터미널에서 실행:
        ```bash
        cd ~/AI-Agent-Full-Stack-Developer/output/card_news
        python3 -m http.server 8080
        ```
        
        브라우저에서 열기:
        ```
        http://localhost:8080/html/
        ```
        """)
    
    with tabs[2]:
        # 다운로드 버튼
        try:
            with open(card['file_path'], 'rb') as f:
                st.download_button(
                    "💾 HTML 파일 다운로드",
                    f.read(),
                    file_name=f"{card['title']}.html",
                    mime="text/html"
                )
        except Exception as e:
            st.error(f"다운로드 실패: {e}")

def get_file_info(file_path):
    """파일 정보 가져오기"""
    try:
        stat = os.stat(file_path)
        size = f"{stat.st_size / 1024:.1f} KB"
        created = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d")
        return {"size": size, "created": created}
    except:
        return {"size": "N/A", "created": "N/A"}

# 메인 함수에 추가할 개선된 CSS
def apply_hybrid_styles():
    """하이브리드 UI 스타일"""
    st.markdown("""
    <style>
    /* 카드 스타일 개선 */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* 버튼 그룹 스타일 */
    div[data-testid="column"] > div {
        display: flex;
        justify-content: center;
    }
    
    /* 코드 블록 개선 */
    .stCodeBlock {
        background-color: #f0f0f0 !important;
        border: 1px solid #ddd !important;
    }
    
    /* Expander 스타일 */
    .streamlit-expanderHeader {
        background-color: #e9ecef;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)
