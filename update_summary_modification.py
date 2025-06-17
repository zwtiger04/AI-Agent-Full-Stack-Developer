#!/usr/bin/env python3
"""
update_summary.py 백업 및 수정
- 기존 카드 형식과 일치하도록 수정
- 자세히 보기 링크 포함
"""
import os
import shutil
from datetime import datetime

def backup_and_update_summary():
    """update_summary.py 백업 및 수정"""
    
    # 백업 생성
    source = "update_summary.py"
    backup = f"update_summary.py.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        shutil.copy2(source, backup)
        print(f"✅ 백업 생성: {backup}")
        
        # 파일 읽기
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 새 카드 HTML 부분 찾기
        old_card_html = '''        # 새 카드 HTML 생성
        new_card = f\'\'\'
            <!-- 기사: {article['title'][:50]}... -->
            <div class="news-card" onclick="window.location.href='{rel_path}'">
                <span class="card-category {category_class}">{category_label}</span>
                <h3 class="card-title">{article['title']}</h3>
                <p class="card-summary">
                    {article.get('summary', '')}
                </p>
                <span class="card-date">{article.get('date', datetime.now().strftime('%Y-%m-%d'))}</span>
            </div>
\'\'\''''
        
        # 기존 카드 형식으로 변경 (자세히 보기 포함)
        new_card_html = '''        # 새 카드 HTML 생성
        new_card = f\'\'\'
            <!-- 기사: {article['title'][:50]}... -->
            <div class="news-card" onclick="window.location.href='{rel_path}'">
                <span class="card-category {category_class}\">{category_label}</span>
                <h3 class="card-title">{article['title']}</h3>
                <p class="card-summary">
                    {article.get('summary', '')}
                </p>
                <div class="card-meta">
                    <span>{article.get('source', '전기신문')}</span>
                    <a href="{rel_path}" class="read-more" onclick="event.stopPropagation()">자세히 보기 →</a>
                </div>
            </div>
\'\'\''''
        
        # 내용 교체
        if old_card_html in content:
            content = content.replace(old_card_html, new_card_html)
            
            # 파일 저장
            with open(source, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ update_summary.py 수정 완료!")
            print("   - card-meta 구조 추가")
            print("   - 자세히 보기 링크 추가")
            print("   - event.stopPropagation() 추가")
            return True
        else:
            print("⚠️  예상한 코드 구조를 찾을 수 없습니다.")
            print("   수동으로 확인이 필요합니다.")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 update_summary.py 수정 시작...")
    if backup_and_update_summary():
        print("\n✅ 작업 완료!")
        print("\n다음 단계:")
        print("1. python3 fix_summary_links.py  # 기존 카드 수정")
        print("2. 새 카드 생성 시 자동으로 올바른 형식 적용됨")
    else:
        print("\n❌ 작업 실패!")
