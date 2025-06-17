import re

# 파일 읽기
with open('card_news_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 변경 기록
changes = []

# 1. CostManager 메서드 변경
# get_today_cost -> get_daily_cost
content = re.sub(r'def get_today_cost\(self\)', 'def get_daily_cost(self)', content)
content = re.sub(r'\.get_today_cost\(\)', '.get_daily_cost()', content)
changes.append("get_today_cost → get_daily_cost (4곳)")

# get_month_cost -> get_monthly_cost  
content = re.sub(r'def get_month_cost\(self\)', 'def get_monthly_cost(self)', content)
content = re.sub(r'\.get_month_cost\(\)', '.get_monthly_cost()', content)
changes.append("get_month_cost → get_monthly_cost (4곳)")

# check_limits -> can_generate (반환값도 변경)
old_check_limits = '''def check_limits(self, daily_limit: float, monthly_limit: float) -> Dict[str, bool]:
        """일일/월간 한도 체크"""
        return {
            'daily_ok': self.get_daily_cost() < daily_limit,
            'monthly_ok': self.get_monthly_cost() < monthly_limit,
            'daily_remaining': daily_limit - self.get_daily_cost(),
            'monthly_remaining': monthly_limit - self.get_monthly_cost()
        }'''

new_can_generate = '''def can_generate(self, daily_limit: float = 10, monthly_limit: float = 50) -> tuple[bool, str]:
        """생성 가능 여부 확인"""
        daily_cost = self.get_daily_cost()
        monthly_cost = self.get_monthly_cost()
        
        if daily_cost >= daily_limit:
            return False, f"일일 한도 초과 (${daily_cost:.2f}/${daily_limit})"
        if monthly_cost >= monthly_limit:
            return False, f"월간 한도 초과 (${monthly_cost:.2f}/${monthly_limit})"
        
        return True, "생성 가능"'''

content = content.replace(old_check_limits, new_can_generate)
changes.append("check_limits → can_generate (메서드 시그니처 변경)")

# check_limits 호출 부분 수정
# limits = generator.cost_manager.check_limits(daily_limit, monthly_limit)
content = re.sub(
    r'limits = generator\.cost_manager\.check_limits\((.*?)\)',
    r'can_gen, message = generator.cost_manager.can_generate(\1)',
    content
)

# limits 사용 부분도 수정해야 함
# if not limits['daily_ok'] or not limits['monthly_ok']:
content = re.sub(
    r"if not limits\['daily_ok'\] or not limits\['monthly_ok'\]:",
    "if not can_gen:",
    content
)

# 2. CardNewsGenerator 클래스 변경
# get_color_scheme 메서드 제거 (사용하지 않음)
# determine_color_theme이 실제로 사용되므로 이름만 변경
content = re.sub(r'def determine_color_theme\(', 'def get_color_theme(', content)
content = re.sub(r'\.determine_color_theme\(', '.get_color_theme(', content)
changes.append("determine_color_theme → get_color_theme")

# get_color_scheme 메서드 완전히 제거
get_color_scheme_pattern = r'def get_color_scheme\(self, keywords\):[\s\S]*?return \[.*?\]\n'
content = re.sub(get_color_scheme_pattern, '', content)
changes.append("get_color_scheme 메서드 제거 (미사용)")

# 3. CardNewsGenerator 초기화 방식 변경
# __init__ 메서드 수정
old_init = '''def __init__(self):
        """카드뉴스 생성기 초기화"""
        self.anthropic_client = None'''

new_init = '''def __init__(self, api_key: str = None):
        """카드뉴스 생성기 초기화
        
        Args:
            api_key: Anthropic API 키 (선택사항, 나중에 setup_api로 설정 가능)
        """
        self.anthropic_client = None
        if api_key:
            self.setup_api(api_key)'''

content = content.replace(old_init, new_init)
changes.append("CardNewsGenerator.__init__ 시그니처 변경")

# 4. main 함수에서 load_dotenv() 추가
main_pattern = r'def main\(\):\n    st\.title'
new_main = '''def main():
    # 환경변수 로드
    load_dotenv()
    
    st.title'''
content = re.sub(main_pattern, new_main, content)
changes.append("main 함수에 load_dotenv() 추가")

# 파일 저장
with open('card_news_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Phase 2 완료: 메서드명 표준화")
print("\n변경 내용:")
for change in changes:
    print(f"  - {change}")

# 추가 분석
print("\n⚠️ 추가 확인 필요 사항:")
print("  - limits['daily_remaining'] 등 사용처 수동 확인 필요")
print("  - can_generate 반환값 변경에 따른 UI 수정 필요")
