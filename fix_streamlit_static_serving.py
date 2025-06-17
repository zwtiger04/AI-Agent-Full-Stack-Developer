#!/usr/bin/env python3
"""
Streamlit 앱에서 카드뉴스 파일을 정적으로 서빙하도록 수정
"""
import os
import shutil
from datetime import datetime

def fix_streamlit_static_serving():
    """Streamlit의 정적 파일 서빙 기능 활용"""
    
    # 백업 생성
    source = "card_news_app.py"
    backup = f"card_news_app.py.backup_static_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        shutil.copy2(source, backup)
        print(f"✅ 백업 생성: {backup}")
        
        # 파일 읽기
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # render_summary_tab 함수의 파일 경로 부분 수정
        old_section = """        # 파일 경로 수정 (상대 경로로)
        # 파일 경로 수정 (Streamlit static 경로 사용)
        actual_path = card["file_path"]
        file_name = os.path.basename(actual_path)
        # Streamlit에서 파일을 열기 위한 전체 경로
        import pathlib
        full_path = str(pathlib.Path(actual_path).resolve())
        file_path = full_path"""
        
        # Streamlit static 서빙을 위한 새 방식
        new_section = """        # 파일 경로 수정 (Streamlit에서 직접 표시)
        actual_path = card["file_path"]
        file_name = os.path.basename(actual_path)
        # Streamlit 앱 내에서 파일 보기 버튼으로 처리
        file_path = f"show_card:{i}" """
        
        # 내용 교체
        if old_section in content:
            content = content.replace(old_section, new_section)
            
            # onclick 핸들러도 수정
            old_onclick = """onclick=\"window.open('{file_path}', '_blank')\""""
            new_onclick = """onclick=\"document.getElementById('card-link-{i}').click()\""""
            content = content.replace(old_onclick, new_onclick)
            
            # href 부분도 수정
            old_href = """<a href=\"{file_path}\" class=\"read-more\" onclick=\"event.stopPropagation()\">자세히 보기 →</a>"""
            new_href = """<a id=\"card-link-{i}\" href=\"#\" class=\"read-more\" onclick=\"event.stopPropagation(); document.querySelector('[data-card-id=\"{i}\"]').click(); return false;\">자세히 보기 →</a>"""
            content = content.replace(old_href, new_href)
            
            # 파일 저장
            with open(source, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ 정적 서빙 방식으로 수정 완료!")
            print("   - 다음 단계: render_summary_tab에 파일 표시 로직 추가 필요")
            return True
        else:
            print("⚠️  예상한 코드를 찾을 수 없습니다.")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

def add_file_display_logic():
    """요약 탭에 파일 표시 로직 추가"""
    
    source = "card_news_app.py"
    
    try:
        # 파일 읽기
        with open(source, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # render_summary_tab 함수 끝 부분 찾기
        for i, line in enumerate(lines):
            if "components.html(html_content, height=1600, scrolling=True)" in line:
                # 그 다음에 파일 표시 로직 추가
                insert_index = i + 1
                
                new_code = """
    # 카드뉴스 클릭 처리
    for idx, card in enumerate(card_news_list):
        if st.button(f"카드 {idx} 보기", key=f"card_view_{idx}", help=card["title"], 
                    type="secondary", use_container_width=False, 
                    disabled=False, on_click=None):
            # 새 탭에서 HTML 파일 열기
            with open(card["file_path"], 'r', encoding='utf-8') as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=800, scrolling=True)
            
"""
                lines.insert(insert_index, new_code)
                
                # 파일 저장
                with open(source, 'w') as f:
                    f.writelines(lines)
                
                print("✅ 파일 표시 로직 추가 완료!")
                return True
                
        print("⚠️  components.html 위치를 찾을 수 없습니다.")
        return False
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Streamlit 정적 서빙 문제 해결 시작...")
    # 실제로는 다른 방법을 사용해야 합니다
    print("\n⚠️  Streamlit의 보안 제한으로 인해 다른 접근이 필요합니다.")
    print("\n대안 제시:")
    print("1. 카드뉴스를 별도 탭에서 표시")
    print("2. 파일 다운로드 버튼 제공")
    print("3. 외부 웹서버 사용")
