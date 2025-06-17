#!/usr/bin/env python3
"""
요약 카드뉴스의 "자세히 보기" 링크 수정
href="#" → 실제 상세 카드뉴스 경로로 변경
"""
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime

def fix_summary_links():
    """자세히 보기 링크 수정"""
    summary_path = "output/card_news/summary/improved_summary.html"
    
    # 백업 생성
    backup_path = f"{summary_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # HTML 파일 읽기
        with open(summary_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 백업 저장
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ 백업 생성: {backup_path}")
        
        # BeautifulSoup으로 파싱
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 모든 news-card 찾기
        news_cards = soup.find_all('div', class_='news-card')
        fixed_count = 0
        
        for card in news_cards:
            # onclick 속성에서 경로 추출
            onclick = card.get('onclick', '')
            match = re.search(r"window\.location\.href='([^']+)'", onclick)
            
            if match:
                href_path = match.group(1)
                
                # 해당 카드 내의 "자세히 보기" 링크 찾기
                read_more = card.find('a', class_='read-more')
                if read_more and read_more.get('href') == '#':
                    read_more['href'] = href_path
                    # onclick 이벤트 제거 (중복 방지)
                    read_more['onclick'] = 'event.stopPropagation()'
                    fixed_count += 1
                    print(f"✅ 수정됨: {href_path}")
        
        # 수정된 HTML 저장
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        
        print(f"\n✅ 총 {fixed_count}개의 링크가 수정되었습니다.")
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        # 오류 시 백업 복원
        if os.path.exists(backup_path):
            os.rename(backup_path, summary_path)
            print("⚠️  백업에서 복원되었습니다.")
        return False

if __name__ == "__main__":
    print("🔧 요약 카드뉴스 링크 수정 시작...")
    if fix_summary_links():
        print("✅ 수정 완료!")
    else:
        print("❌ 수정 실패!")
