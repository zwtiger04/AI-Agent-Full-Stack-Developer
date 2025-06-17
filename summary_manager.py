"""
요약 카드뉴스 데이터 관리 클래스
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from card_news_paths import get_path_str

class SummaryManager:
    def __init__(self):
        self.data_path = Path(get_path_str('summary_json'))
        self.ensure_data_file()
    
    def ensure_data_file(self):
        """데이터 파일이 없으면 생성"""
        if not self.data_path.exists():
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump({"cards": []}, f, ensure_ascii=False, indent=2)
    
    def load_cards(self) -> List[Dict]:
        """모든 카드 로드"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('cards', [])
        except Exception as e:
            print(f"❌ 카드 로드 실패: {e}")
            return []
    
    def add_card(self, card_data: Dict) -> bool:
        """새 카드 추가"""
        try:
            cards = self.load_cards()
            
            # ID가 없으면 생성
            if 'id' not in card_data:
                file_name = Path(card_data.get('file_path', '')).name
                card_data['id'] = file_name.replace('.html', '') if file_name else f"card_{len(cards)}"
            
            # 중복 체크
            if any(card['id'] == card_data['id'] for card in cards):
                print(f"⚠️ 이미 존재하는 카드: {card_data['id']}")
                return False
            
            # 추가 날짜 설정
            if 'added_date' not in card_data:
                card_data['added_date'] = datetime.now().isoformat()
            
            cards.append(card_data)
            
            # 저장
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump({"cards": cards}, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ 카드 추가 실패: {e}")
            return False
    
    def filter_cards(self, category: Optional[str] = None, 
                    date_range: Optional[tuple] = None, 
                    search: Optional[str] = None) -> List[Dict]:
        """카드 필터링"""
        cards = self.load_cards()
        
        # 카테고리 필터
        if category and category != "전체":
            cards = [c for c in cards if c.get('category') == category]
        
        # 날짜 필터
        if date_range:
            start_date, end_date = date_range
            cards = [c for c in cards if self._is_in_date_range(c.get('date', ''), start_date, end_date)]
        
        # 검색 필터
        if search:
            search_lower = search.lower()
            cards = [c for c in cards if self._matches_search(c, search_lower)]
        
        return cards
    
    def _is_in_date_range(self, date_str: str, start: str, end: str) -> bool:
        """날짜 범위 확인"""
        try:
            if not date_str:
                return True  # 날짜가 없으면 포함
            # 날짜 파싱 및 비교 로직
            return True  # 임시
        except:
            return True
    
    def _matches_search(self, card: Dict, search_term: str) -> bool:
        """검색어 매칭"""
        searchable_fields = ['title', 'summary', 'category']
        searchable_text = ' '.join(str(card.get(field, '')) for field in searchable_fields)
        searchable_text += ' ' + ' '.join(card.get('keywords', []))
        
        return search_term in searchable_text.lower()
    
    def get_categories(self) -> List[str]:
        """모든 카테고리 목록"""
        cards = self.load_cards()
        categories = list(set(card.get('category', '') for card in cards if card.get('category')))
        return sorted(categories)
    
    def get_card_by_id(self, card_id: str) -> Optional[Dict]:
        """ID로 카드 조회"""
        cards = self.load_cards()
        for card in cards:
            if card.get('id') == card_id:
                return card
        return None
    
    def update_card(self, card_id: str, updates: Dict) -> bool:
        """카드 업데이트"""
        try:
            cards = self.load_cards()
            
            for i, card in enumerate(cards):
                if card.get('id') == card_id:
                    cards[i].update(updates)
                    
                    with open(self.data_path, 'w', encoding='utf-8') as f:
                        json.dump({"cards": cards}, f, ensure_ascii=False, indent=2)
                    
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ 카드 업데이트 실패: {e}")
            return False
    
    def delete_card(self, card_id: str) -> bool:
        """카드 삭제"""
        try:
            cards = self.load_cards()
            cards = [c for c in cards if c.get('id') != card_id]
            
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump({"cards": cards}, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ 카드 삭제 실패: {e}")
            return False

# 테스트
if __name__ == "__main__":
    manager = SummaryManager()
    cards = manager.load_cards()
    print(f"✅ 총 {len(cards)}개의 카드 로드됨")
    
    # 카테고리 목록
    categories = manager.get_categories()
    print(f"📁 카테고리: {categories}")
