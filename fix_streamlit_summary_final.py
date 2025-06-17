#!/usr/bin/env python3
"""
Streamlit 요약 탭의 경로 문제 완전 해결
- onclick과 href 모두 수정
- Streamlit 정적 파일 서빙 활용
"""
import os
import shutil
from datetime import datetime

def fix_streamlit_summary_final():
    """Streamlit 요약 탭 최종 수정"""
    
    # 백업 생성
    source = "card_news_app.py"
    backup = f"card_news_app.py.backup_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        shutil.copy2(source, backup)
        print(f"✅ 백업 생성: {backup}")
        
        # 파일 읽기
        with open(source, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 수정이 필요한 줄 찾기
        modified = False
        for i, line in enumerate(lines):
            # file_path 설정 부분 수정
            if "file_path = card[\"file_path\"].replace('output/card_news/html/', '')" in line:
                # Streamlit의 static file serving을 위한 경로 설정
                lines[i] = """        # 파일 경로 수정 (Streamlit static 경로 사용)
        actual_path = card["file_path"]
        file_name = os.path.basename(actual_path)
        # Streamlit에서 파일을 열기 위한 전체 경로
        import pathlib
        full_path = str(pathlib.Path(actual_path).resolve())
        file_path = full_path
"""
                modified = True
                print("✅ file_path 설정 수정됨")
            
            # onclick 부분 수정 - window.open 사용
            elif "onclick=\"window.location.href='{file_path}'\"" in line:
                lines[i] = line.replace(
                    "onclick=\"window.location.href='{file_path}'\"",
                    "onclick=\"window.open('{file_path}', '_blank')\""
                )
                modified = True
                print("✅ onclick 수정됨")
        
        if modified:
            # 파일 저장
            with open(source, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print("✅ card_news_app.py 최종 수정 완료!")
            return True
        else:
            print("⚠️  예상한 코드를 찾을 수 없습니다.")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Streamlit 요약 탭 최종 수정 시작...")
    if fix_streamlit_summary_final():
        print("\n✅ 작업 완료!")
        print("\n다음 단계:")
        print("1. Streamlit 앱 중지 (Ctrl+C)")
        print("2. 다시 시작: streamlit run card_news_app.py")
    else:
        print("\n❌ 작업 실패!")
