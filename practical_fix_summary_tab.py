#!/usr/bin/env python3
"""
Streamlit 요약 탭에서 카드뉴스 클릭 시 직접 표시하도록 수정
가장 실용적이고 간단한 해결책
"""
import os
import shutil
from datetime import datetime

def practical_fix_summary_tab():
    """실용적인 해결책: 클릭 시 Streamlit 내에서 카드뉴스 표시"""
    
    source = "card_news_app.py"
    backup = f"card_news_app.py.backup_practical_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        shutil.copy2(source, backup)
        print(f"✅ 백업 생성: {backup}")
        
        # 파일 읽기
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # render_summary_tab 함수 찾아서 수정
        # 1. 먼저 함수 시작 부분 찾기
        func_start = content.find("def render_summary_tab():")
        if func_start == -1:
            print("❌ render_summary_tab 함수를 찾을 수 없습니다.")
            return False
            
        # 2. components.html 부분 찾기
        comp_start = content.find("components.html(html_content, height=1600, scrolling=True)", func_start)
        if comp_start == -1:
            print("❌ components.html을 찾을 수 없습니다.")
            return False
            
        # 3. 그 다음 줄에 새 코드 삽입
        insert_pos = content.find("\n", comp_start) + 1
        
        # 4. 삽입할 코드
        new_code = """
    # 카드뉴스 클릭 처리 - Session State 사용
    if 'selected_card' not in st.session_state:
        st.session_state.selected_card = None
    
    # 카드 선택 처리 (숨겨진 버튼들)
    for idx, card in enumerate(card_news_list):
        if st.button(f"card_{idx}", key=f"hidden_card_{idx}", 
                    label_visibility="hidden", type="secondary"):
            st.session_state.selected_card = idx
            st.rerun()
    
    # 선택된 카드뉴스 표시
    if st.session_state.selected_card is not None:
        selected = card_news_list[st.session_state.selected_card]
        
        # 뒤로가기 버튼
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("⬅️ 목록으로 돌아가기"):
                st.session_state.selected_card = None
                st.rerun()
        
        # 카드뉴스 내용 표시
        try:
            with open(selected["file_path"], 'r', encoding='utf-8') as f:
                card_html = f.read()
            components.html(card_html, height=800, scrolling=True)
        except Exception as e:
            st.error(f"파일을 열 수 없습니다: {e}")
"""
        
        # 5. 코드 삽입
        content = content[:insert_pos] + new_code + content[insert_pos:]
        
        # 6. HTML의 onclick 수정 - JavaScript로 Streamlit 버튼 클릭 트리거
        # 먼저 window.open 부분을 찾아서 수정
        old_onclick = """onclick=\"window.open('{file_path}', '_blank')\""""
        new_onclick = """onclick=\"document.querySelector('button[kind=secondary]:nth-of-type({i+1})').click()\""""
        
        # render_summary_tab 함수 내에서만 수정
        func_end = content.find("\ndef ", func_start + 1)
        if func_end == -1:
            func_end = len(content)
        
        func_content = content[func_start:func_end]
        func_content = func_content.replace(old_onclick, new_onclick)
        
        # href 부분도 수정
        old_href = """<a href=\"{file_path}\" class=\"read-more\" onclick=\"event.stopPropagation()\">자세히 보기 →</a>"""
        new_href = """<a href=\"#\" class=\"read-more\" onclick=\"event.stopPropagation(); document.querySelector('button[kind=secondary]:nth-of-type({i+1})').click(); return false;\">자세히 보기 →</a>"""
        func_content = func_content.replace(old_href, new_href)
        
        # 전체 내용 재구성
        content = content[:func_start] + func_content + content[func_end:]
        
        # 파일 저장
        with open(source, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 실용적인 수정 완료!")
        print("   - 클릭 시 Streamlit 내에서 카드뉴스 표시")
        print("   - 뒤로가기 버튼 제공")
        print("   - Session State 활용")
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Streamlit 요약 탭 실용적 해결책 적용...")
    if practical_fix_summary_tab():
        print("\n✅ 작업 완료!")
        print("\n이제:")
        print("1. Streamlit 앱을 재시작하세요 (Ctrl+C 후 다시 실행)")
        print("2. 요약 카드뉴스 탭에서 카드 클릭")
        print("3. 같은 탭 내에서 상세 카드뉴스가 표시됩니다")
        print("4. '목록으로 돌아가기' 버튼으로 복귀 가능")
    else:
        print("\n❌ 작업 실패!")
