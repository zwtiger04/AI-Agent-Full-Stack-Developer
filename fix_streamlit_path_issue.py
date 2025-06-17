#!/usr/bin/env python3
"""
Streamlit 환경에서 상대 경로 문제 해결
file_path를 절대 URL로 변경
"""
import os
import shutil
from datetime import datetime

def fix_streamlit_path_issue():
    """Streamlit 앱의 경로 문제 수정"""
    
    # 백업 생성
    source = "card_news_app.py"
    backup = f"card_news_app.py.backup_path_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        shutil.copy2(source, backup)
        print(f"✅ 백업 생성: {backup}")
        
        # 파일 읽기
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # render_summary_tab에서 경로 수정 부분 찾기
        old_section = """        # 파일 경로 수정 (상대 경로로)
        file_path = card["file_path"].replace('output/card_news/html/', '')"""
        
        new_section = """        # 파일 경로 수정 (전체 경로 사용)
        # Streamlit 환경에서는 file:// 프로토콜 사용
        import os
        full_path = os.path.abspath(card["file_path"])
        file_path = f"file://{full_path}" """
        
        # 내용 교체
        if old_section in content:
            content = content.replace(old_section, new_section)
            
            # 파일 저장
            with open(source, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ 경로 문제 수정 완료!")
            print("   - 상대 경로 → 절대 경로 (file:// 프로토콜)")
            return True
        else:
            print("⚠️  예상한 코드를 찾을 수 없습니다.")
            
            # 다른 방법 시도
            # onclick 부분을 수정
            old_onclick = """onclick=\"window.location.href='{file_path}'\" """
            new_onclick = """onclick=\"window.open('{file_path}', '_blank')\" """
            
            if old_onclick in content:
                content = content.replace(old_onclick, new_onclick)
                
                with open(source, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ onclick 방식 변경 완료!")
                print("   - window.location.href → window.open")
                return True
            
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Streamlit 경로 문제 수정 시작...")
    if fix_streamlit_path_issue():
        print("\n✅ 작업 완료!")
        print("\n이제 Streamlit 앱을 재시작하세요.")
    else:
        print("\n❌ 작업 실패!")
        print("수동으로 확인이 필요합니다.")
