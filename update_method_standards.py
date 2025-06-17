import re

# 파일 읽기
with open('INTEGRATED_PROJECT_GUIDE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# CostManager 섹션 찾기 및 업데이트
costmanager_section = '''#### CostManager 클래스
```python
class CostManager:
    def __init__(self)
    def load_costs(self) -> dict
    def save_costs(self) -> None
    def add_cost(self, amount: float) -> None
    def get_daily_cost(self) -> float      # NOT get_today_cost()
    def get_monthly_cost(self) -> float    # NOT get_month_cost()
    def can_generate(self, daily_limit: float = 10, monthly_limit: float = 50) -> tuple
```'''

new_costmanager_section = '''#### CostManager 클래스
```python
class CostManager:
    """비용 관리 클래스 - 아래 메서드만 사용할 것"""
    
    def __init__(self)
    def load_costs(self) -> dict
    def save_costs(self) -> None
    def add_cost(self, amount: float) -> None
    def get_daily_cost(self) -> float      # ❌ NEVER: get_today_cost()
    def get_monthly_cost(self) -> float    # ❌ NEVER: get_month_cost()
    def can_generate(self, daily_limit: float = 10, monthly_limit: float = 50) -> tuple[bool, str]
    
    # ⚠️ 새로운 메서드 추가 금지! 위 메서드만 사용
```'''

content = content.replace(costmanager_section, new_costmanager_section)

# CardNewsGenerator 섹션 업데이트
cardnews_section = '''#### CardNewsGenerator 클래스
```python
class CardNewsGenerator:
    def __init__(self, api_key: str)       # API 키는 생성자에서 받기
    def get_color_theme(self, keyword: str) -> Dict[str, str]  # NOT get_color_scheme()
    def generate_card_news(self, article: Union[Dict, Article], 
                          theme: Union[str, Dict], 
                          sections: List[str]) -> str
```'''

new_cardnews_section = '''#### CardNewsGenerator 클래스
```python
class CardNewsGenerator:
    """카드뉴스 생성 클래스 - 아래 메서드만 사용할 것"""
    
    def __init__(self, api_key: str)       # API 키는 생성자에서 받기
    def get_color_theme(self, keyword: str) -> Dict[str, str]  # ❌ NEVER: get_color_scheme()
    def generate_card_news(self, article: Union[Dict, Article], 
                          theme: Union[str, Dict], 
                          sections: List[str]) -> str
    
    # ⚠️ 새로운 메서드 추가 금지! 필요시 유틸리티 함수로 분리
```'''

content = content.replace(cardnews_section, new_cardnews_section)

# 금지 사항 섹션 추가
forbidden_section = '''
### 5. 금지 사항 [STD-FORBIDDEN-001]

#### ❌ 절대 하지 말아야 할 것들
1. **메서드명 변형 금지**
   - ❌ `get_today_cost()` - 사용 금지
   - ❌ `get_month_cost()` - 사용 금지  
   - ❌ `check_limits()` - 사용 금지
   - ❌ `get_color_scheme()` - 사용 금지

2. **새로운 메서드 추가 금지**
   - CostManager와 CardNewsGenerator에 새 메서드 추가 금지
   - 필요한 기능은 유틸리티 함수나 별도 클래스로 구현

3. **Import 방식 변형 금지**
   - ❌ `import anthropic` - 사용 금지
   - ✅ `from anthropic import Anthropic` - 올바른 방식

4. **파일명 임의 변경 금지**
   - 정의된 상수만 사용 (COST_TRACKING_FILE 등)
'''

# 통합 체크리스트 앞에 삽입
integration_pattern = r'### 4\. 통합 시 체크리스트'
content = re.sub(integration_pattern, forbidden_section + '\n### 4. 통합 시 체크리스트', content)

# 파일 저장
with open('INTEGRATED_PROJECT_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 메서드 표준이 강화되었습니다!")
