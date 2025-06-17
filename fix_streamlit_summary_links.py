#!/usr/bin/env python3
"""
Streamlit 앱의 요약 탭 링크 수정
render_summary_tab 함수에서 href="#"를 실제 경로로 변경
"""
import os
import shutil
from datetime import datetime

def fix_streamlit_summary_links():
    """Streamlit 앱의 요약 탭 링크 수정"""
    
    # 백업 생성
    source = "card_news_app.py"
    backup = f"card_news_app.py.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        shutil.copy2(source, backup)
        print(f"✅ 백업 생성: {backup}")
        
        # 파일 읽기
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 수정할 부분 찾기 - render_summary_tab 함수 내의 href="#" 부분
        old_line = '<a href="#" class="read-more">자세히 보기 →</a>'
        new_line = '<a href="{file_path}" class="read-more" onclick="event.stopPropagation()">자세히 보기 →</a>'
        
        # 내용 교체
        if old_line in content:
            content = content.replace(old_line, new_line)
            
            # 파일 저장
            with open(source, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ card_news_app.py 수정 완료!")
            print("   - render_summary_tab 함수의 href 수정")
            print("   - event.stopPropagation() 추가")
            return True
        else:
            print("⚠️  예상한 코드를 찾을 수 없습니다.")
            
            # create_card_grid 함수도 확인
            old_line2 = '<a href="#" class="read-more" onclick="event.stopPropagation(); window.open(\'{card["file_path"]}\', \'_blank\'); return false;">자세히 보기 →</a>'
            if old_line2 in content:
                # 이 부분도 수정 필요
                new_line2 = '<a href="{card["file_path"]}" class="read-more" onclick="event.stopPropagation()">자세히 보기 →</a>'
                content = content.replace(old_line2, new_line2)
                
                with open(source, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ create_card_grid 함수 수정 완료!")
                return True
                
            print("   수동으로 확인이 필요합니다.")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Streamlit 앱 요약 탭 링크 수정 시작...")
    if fix_streamlit_summary_links():
        print("\n✅ 작업 완료!")
        print("\n다음 단계:")
        print("1. Streamlit 앱 재시작")
        print("2. '요약 카드뉴스' 탭에서 테스트")
    else:
        print("\n❌ 작업 실패!")
