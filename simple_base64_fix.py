#!/usr/bin/env python3
"""
가장 간단한 해결책: Base64 Data URL 사용
브라우저 보안 제한을 우회하여 새 탭에서 HTML 열기
"""
import os
import shutil
from datetime import datetime

def simple_base64_fix():
    """Base64 인코딩으로 HTML을 Data URL로 변환"""
    
    source = "card_news_app.py"
    backup = f"card_news_app.py.backup_base64_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        shutil.copy2(source, backup)
        print(f"✅ 백업 생성: {backup}")
        
        # 파일 읽기
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # render_summary_tab 함수의 시작 부분에 base64 import 추가
        render_start = content.find("def render_summary_tab():")
        if render_start == -1:
            print("❌ render_summary_tab 함수를 찾을 수 없습니다.")
            return False
        
        # import 추가
        import_line = "\n    import base64\n"
        insert_pos = content.find("\n", render_start) + 1
        
        # 이미 import가 있는지 확인
        if "import base64" not in content[render_start:render_start+500]:
            content = content[:insert_pos] + import_line + content[insert_pos:]
        
        # 파일 경로 수정 부분 찾기
        old_section = """        # 파일 경로 수정 (상대 경로로)
        # 파일 경로 수정 (Streamlit static 경로 사용)
        actual_path = card["file_path"]
        file_name = os.path.basename(actual_path)
        # Streamlit에서 파일을 열기 위한 전체 경로
        import pathlib
        full_path = str(pathlib.Path(actual_path).resolve())
        file_path = full_path"""
        
        # Base64 인코딩 방식으로 변경
        new_section = """        # 파일 경로 수정 (Base64 Data URL 사용)
        actual_path = card["file_path"]
        try:
            # HTML 파일 읽어서 Base64로 인코딩
            with open(actual_path, 'r', encoding='utf-8') as f:
                html_content_card = f.read()
            encoded = base64.b64encode(html_content_card.encode()).decode()
            # Data URL 생성
            file_path = f"data:text/html;base64,{encoded}"
        except:
            file_path = "#" """
        
        # 내용 교체
        if old_section in content:
            content = content.replace(old_section, new_section)
            
            # 파일 저장
            with open(source, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Base64 인코딩 방식으로 수정 완료!")
            print("   - HTML 파일을 Base64로 인코딩")
            print("   - Data URL로 브라우저에서 직접 열기 가능")
            return True
        else:
            print("⚠️  예상한 코드를 찾을 수 없습니다.")
            print("   다른 버전의 코드가 있는 것 같습니다.")
            
            # 대체 패턴 시도
            if "file_path = full_path" in content:
                # 더 간단한 치환
                content = content.replace(
                    "file_path = full_path",
                    """try:
            with open(actual_path, 'r', encoding='utf-8') as f:
                html_content_card = f.read()
            import base64
            encoded = base64.b64encode(html_content_card.encode()).decode()
            file_path = f"data:text/html;base64,{encoded}"
        except:
            file_path = "#" """
                )
                
                with open(source, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ 대체 방법으로 수정 완료!")
                return True
            
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 가장 간단한 해결책: Base64 Data URL 적용...")
    if simple_base64_fix():
        print("\n✅ 작업 완료!")
        print("\n이제:")
        print("1. 현재 실행 중인 Streamlit 앱 중지 (Ctrl+C)")
        print("2. 다시 실행: streamlit run card_news_app.py")
        print("3. '요약 카드뉴스' 탭에서 카드 클릭")
        print("4. 새 탭에서 카드뉴스가 열립니다!")
    else:
        print("\n❌ 작업 실패!")
        print("수동 확인이 필요합니다.")
