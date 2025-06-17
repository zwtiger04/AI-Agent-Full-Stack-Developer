# Option A 구현 시 예상되는 복잡한 코드 예시

def render_summary_tab():
    """복잡해진 요약 탭 - 문제점 시뮬레이션"""
    
    # 1. Session State 관리 (복잡도 증가)
    if 'selected_card' not in st.session_state:
        st.session_state.selected_card = None
    if 'view_history' not in st.session_state:
        st.session_state.view_history = []
    if 'scroll_position' not in st.session_state:
        st.session_state.scroll_position = 0
    
    # 2. 카드 선택 상태에 따른 분기
    if st.session_state.selected_card is None:
        # 목록 표시
        display_card_list()
    else:
        # 상세 보기
        display_card_detail()
    
def display_card_list():
    """카드 목록 표시 - 복잡한 이벤트 처리"""
    cards = load_generated_card_news()
    
    # HTML로 카드 그리드 생성
    html_content = generate_grid_html(cards)
    
    # 숨겨진 버튼들 (해킹적인 방법)
    for i, card in enumerate(cards):
        if st.button(f"hidden_{i}", key=f"card_btn_{i}", 
                    label_visibility="hidden"):
            st.session_state.selected_card = i
            st.session_state.view_history.append(i)
            st.rerun()
    
    # JavaScript로 버튼 트리거 (불안정)
    html_with_js = html_content + """
    <script>
    document.querySelectorAll('.news-card').forEach((card, i) => {
        card.onclick = () => {
            // Streamlit 버튼 찾아서 클릭 (취약함)
            const btn = document.querySelector(`button[kind="secondary"]:nth-child(${i+1})`);
            if (btn) btn.click();
        }
    });
    </script>
    """
    
    components.html(html_with_js, height=1600)

def display_card_detail():
    """카드 상세 표시 - 제한사항 많음"""
    selected = load_generated_card_news()[st.session_state.selected_card]
    
    # 상단 네비게이션
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("⬅️ 목록으로"):
            st.session_state.selected_card = None
            st.rerun()
    
    with col2:
        st.markdown(f"### {selected['title']}")
    
    with col3:
        # 이전/다음 버튼 (복잡한 로직)
        if st.session_state.view_history:
            if st.button("⬅️ 이전"):
                # 복잡한 히스토리 관리
                pass
    
    # HTML 렌더링
    try:
        with open(selected['file_path'], 'r', encoding='utf-8') as f:
            card_html = f.read()
        
        # CSS 격리 시도 (완벽하지 않음)
        isolated_html = f"""
        <div style="position: relative; width: 100%; overflow: hidden;">
            <style>
            /* Streamlit 스타일 오버라이드 시도 */
            .stApp {{ padding: 0 !important; }}
            </style>
            {card_html}
        </div>
        """
        
        # 높이 자동 조절 불가능
        components.html(isolated_html, height=800, scrolling=True)
        
    except Exception as e:
        st.error(f"카드뉴스를 표시할 수 없습니다: {e}")
    
    # 하단 네비게이션 (중복 UI)
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("목록으로 돌아가기", use_container_width=True):
            st.session_state.selected_card = None
            st.rerun()

# 추가 문제: 여러 곳에서 호출 시 상태 관리 복잡
# 추가 문제: 에러 처리 복잡
# 추가 문제: 성능 최적화 어려움
