# 파일 읽기
with open('card_news_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# check_limits 메서드를 can_generate로 완전히 교체
old_method = '''    def check_limits(self, daily_limit: float, monthly_limit: float) -> Dict[str, bool]:
        """한도 확인"""
        return {
            'daily_ok': self.get_daily_cost() < daily_limit,
            'monthly_ok': self.get_monthly_cost() < monthly_limit,
            'daily_remaining': daily_limit - self.get_daily_cost(),
            'monthly_remaining': monthly_limit - self.get_monthly_cost()
        }'''

new_method = '''    def can_generate(self, daily_limit: float = 10, monthly_limit: float = 50) -> tuple[bool, str]:
        """생성 가능 여부 확인"""
        daily_cost = self.get_daily_cost()
        monthly_cost = self.get_monthly_cost()
        
        if daily_cost >= daily_limit:
            return False, f"일일 한도 초과 (${daily_cost:.2f}/${daily_limit})"
        if monthly_cost >= monthly_limit:
            return False, f"월간 한도 초과 (${monthly_cost:.2f}/${monthly_limit})"
        
        return True, "생성 가능"'''

content = content.replace(old_method, new_method)

# 파일 저장
with open('card_news_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ can_generate 메서드 교체 완료!")
