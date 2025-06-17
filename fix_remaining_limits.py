import re

# 파일 읽기
with open('card_news_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# limits 사용 부분 찾아서 수정
# 첫 번째 limits 사용 부분 (라인 728 근처)
old_limits_usage1 = '''        if not limits['daily_ok']:
            st.error(f"❌ 일일 한도를 초과했습니다! (한도: ${daily_limit})")
        else:
            st.info(f"일일 잔여: ${limits['daily_remaining']:.2f}")
        
        if not limits['monthly_ok']:
            st.error(f"❌ 월간 한도를 초과했습니다! (한도: ${monthly_limit})")
        else:
            st.info(f"월간 잔여: ${limits['monthly_remaining']:.2f}")'''

new_limits_usage1 = '''        if not can_gen:
            st.error(f"❌ {message}")
        else:
            daily_remaining = daily_limit - generator.cost_manager.get_daily_cost()
            monthly_remaining = monthly_limit - generator.cost_manager.get_monthly_cost()
            st.info(f"일일 잔여: ${daily_remaining:.2f}")
            st.info(f"월간 잔여: ${monthly_remaining:.2f}")'''

content = content.replace(old_limits_usage1, new_limits_usage1)

# 두 번째 limits 사용 부분 찾기
# if limits['daily_ok'] and limits['monthly_ok']:
content = re.sub(
    r"if limits\['daily_ok'\] and limits\['monthly_ok'\]:",
    "if can_gen:",
    content
)

# 세 번째 사용 부분도 있는지 확인하고 수정
# 전체적으로 limits 변수 사용을 can_gen으로 변경
content = re.sub(r'\blimits\b', 'can_gen, message', content, count=1)  # 첫 번째 할당만

# 파일 저장
with open('card_news_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ limits 관련 코드 수정 완료!")
print("\n수정 내용:")
print("  - limits['daily_ok'] → can_gen")
print("  - limits['monthly_ok'] → can_gen")
print("  - daily_remaining, monthly_remaining 직접 계산으로 변경")
