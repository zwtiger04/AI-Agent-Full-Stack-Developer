#!/usr/bin/env python3
"""
import 위치 수정 및 원래 방식으로 복원
"""
import os
import shutil
from datetime import datetime

def fix_import_and_restore():
    """import 위치 수정 및 간단한 방식으로 복원"""
    
    source = "card_news_app.py"
    backup = f"card_news_app.py.backup_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        shutil.copy2(source, backup)
        print(f"✅ 백업 생성: {backup}")
        
        # 파일 읽기
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 잘못된 import 위치 수정
        wrong_import = """def render_summary_tab():

    import base64
    \"\"\"요약 카드뉴스 탭 - 원본과 100% 동일한 스타일\"\"\" """
        
        correct_import = """def render_summary_tab():
    \"\"\"요약 카드뉴스 탭 - 원본과 100% 동일한 스타일\"\"\"
    import base64"""
        
        content = content.replace(wrong_import, correct_import)
        
        # 너무 복잡한 Base64 방식 대신 간단한 방식으로 변경
        # onclick에서 직접 HTML 파일 경로 사용 (WSL 경로)
        old_base64_section = """        # 파일 경로 수정 (Base64 Data URL 사용)
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
        
        # 간단한 방식: 절대 경로 사용
        simple_section = """        # 파일 경로 수정 (절대 경로 사용)
        actual_path = card["file_path"]
        # WSL에서의 절대 경로
        import os
        abs_path = os.path.abspath(actual_path)
        # Windows 경로로 변환 (WSL에서 Windows 파일 열기)
        if abs_path.startswith('/home/'):
            # WSL 경로를 Windows 경로로 변환
            file_path = f"file://wsl$/Ubuntu{abs_path}"
        else:
            file_path = f"file://{abs_path}" """
        
        content = content.replace(old_base64_section, simple_section)
        
        # 파일 저장
        with open(source, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 수정 완료!")
        print("   - import 위치 수정")
        print("   - Base64 대신 파일 경로 직접 사용")
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 import 오류 수정 및 간단한 방식 복원...")
    if fix_import_and_restore():
        print("\n✅ 작업 완료!")
        print("\n하지만 Streamlit의 보안 제한으로 파일 직접 열기는 여전히 작동하지 않을 수 있습니다.")
        print("\n💡 최종 권장 방법:")
        print("1. 요약 페이지를 별도의 정적 HTML로 제공")
        print("2. 또는 Streamlit 내에서 카드뉴스 내용을 직접 표시")
    else:
        print("\n❌ 작업 실패!")
