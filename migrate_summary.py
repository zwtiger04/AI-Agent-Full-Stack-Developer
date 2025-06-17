#!/usr/bin/env python3
"""
요약 HTML을 JSON 형식으로 마이그레이션하는 스크립트
"""
import json
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from card_news_paths import get_path_str
import argparse

class SummaryMigrator:
    def __init__(self):
        self.html_path = Path("output/card_news/summary/improved_summary.html")
        self.json_path = Path(get_path_str('summary_json'))
        
    def parse_html(self):
        """HTML 파일을 파싱하여 카드 정보 추출"""
        if not self.html_path.exists():
            print(f"❌ HTML 파일을 찾을 수 없습니다: {self.html_path}")
            return None
            
        with open(self.html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        cards = []
        
        # 모든 news-card 찾기
        for card_div in soup.find_all('div', class_='news-card'):
            try:
                # onclick 속성에서 파일 경로 추출
                onclick = card_div.get('onclick', '')
                file_match = re.search(r"'([^']+\.html)'", onclick)
                file_path = file_match.group(1) if file_match else ''
                
                # 카테고리 추출
                category_span = card_div.find('span', class_='card-category')
                category = category_span.text.strip() if category_span else ''
                
                # 제목 추출
                title_h3 = card_div.find('h3', class_='card-title')
                title = title_h3.text.strip() if title_h3 else ''
                
                # 요약 추출
                summary_p = card_div.find('p', class_='card-summary')
                summary = summary_p.text.strip() if summary_p else ''
                
                # 날짜 추출
                date_span = card_div.find('span', class_='card-date')
                date = date_span.text.strip() if date_span else ''
                
                # 파일명에서 ID 생성
                file_name = Path(file_path).name if file_path else ''
                card_id = file_name.replace('.html', '') if file_name else f"card_{len(cards)}"
                
                # 키워드 추출 (카테고리 기반)
                keywords = self._extract_keywords(category, title)
                
                card_data = {
                    "id": card_id,
                    "title": title,
                    "summary": summary,
                    "keywords": keywords,
                    "date": date,
                    "file_path": file_path.replace('../html/', ''),  # 상대 경로 정리
                    "category": category,
                    "added_date": datetime.now().isoformat()
                }
                
                cards.append(card_data)
                
            except Exception as e:
                print(f"⚠️ 카드 파싱 오류: {e}")
                continue
                
        return {"cards": cards}
    
    def _extract_keywords(self, category, title):
        """카테고리와 제목에서 키워드 추출"""
        keywords = []
        
        # 카테고리 매핑
        category_keywords = {
            "ESS": ["ESS", "에너지저장"],
            "VPP": ["VPP", "가상발전소"],
            "재생에너지": ["재생에너지", "신재생"],
            "태양광": ["태양광", "솔라"],
            "풍력": ["풍력", "해상풍력"],
            "전력시장": ["전력시장", "전력거래"],
            "정책": ["정책", "정부"],
            "투자": ["투자", "금융"]
        }
        
        # 카테고리 기반 키워드
        for cat, kws in category_keywords.items():
            if cat in category:
                keywords.extend(kws)
                break
        
        # 제목에서 키워드 추출
        keyword_patterns = ["ESS", "VPP", "태양광", "풍력", "재생에너지", "전력", "에너지", "배터리"]
        for pattern in keyword_patterns:
            if pattern in title and pattern not in keywords:
                keywords.append(pattern)
        
        return keywords[:5]  # 최대 5개
    
    def save_json(self, data, dry_run=False):
        """JSON 파일로 저장"""
        if dry_run:
            print("\n🔍 [DRY RUN] JSON 데이터 미리보기:")
            print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])
            print(f"\n총 {len(data['cards'])}개의 카드가 마이그레이션될 예정입니다.")
            return True
            
        try:
            # 디렉토리 확인
            self.json_path.parent.mkdir(parents=True, exist_ok=True)
            
            # JSON 저장
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            print(f"✅ JSON 파일 저장 완료: {self.json_path}")
            print(f"   총 {len(data['cards'])}개의 카드 마이그레이션 완료")
            return True
            
        except Exception as e:
            print(f"❌ JSON 저장 실패: {e}")
            return False
    
    def migrate(self, dry_run=False):
        """마이그레이션 실행"""
        print("🚀 요약 페이지 마이그레이션 시작...")
        
        # HTML 파싱
        data = self.parse_html()
        if not data:
            return False
        
        # JSON 저장
        return self.save_json(data, dry_run)

def main():
    parser = argparse.ArgumentParser(description='요약 HTML을 JSON으로 마이그레이션')
    parser.add_argument('--dry-run', action='store_true', help='실제 저장하지 않고 미리보기만')
    args = parser.parse_args()
    
    migrator = SummaryMigrator()
    success = migrator.migrate(dry_run=args.dry_run)
    
    if success and not args.dry_run:
        print("\n✅ 마이그레이션 완료!")
        print("다음 단계: update_summary.py를 수정하여 JSON도 업데이트하도록 변경")

if __name__ == "__main__":
    main()
