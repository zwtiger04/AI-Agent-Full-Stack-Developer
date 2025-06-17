import re

# 파일 읽기
with open('card_news_app_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 체크박스 부분 수정 - 테스트 모드에서는 자동으로 체크되도록
checkbox_pattern = r'if st\.checkbox\(\s*"위 예상 비용을 확인했으며'
checkbox_replacement = '''if test_mode or st.checkbox(
                                "위 예상 비용을 확인했으며'''

content = re.sub(checkbox_pattern, checkbox_replacement, content)

# 비용 정보 섹션에 테스트 모드 표시 추가
cost_info_pattern = r'(with st\.expander\("💰 비용 정보", expanded=True\):)'
cost_info_replacement = r'''\1
                        if test_mode:
                            st.info("🧪 테스트 모드에서는 비용이 발생하지 않습니다!")'''

content = re.sub(cost_info_pattern, cost_info_replacement, content)

# 일일 한도 체크 부분 수정
limit_check_pattern = r'if current_daily_cost \+ COST_PER_REQUEST > daily_limit:'
limit_check_replacement = '''if not test_mode and current_daily_cost + COST_PER_REQUEST > daily_limit:'''

content = re.sub(limit_check_pattern, limit_check_replacement, content)

# 파일 저장
with open('card_news_app_integrated.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("테스트 모드 개선 완료!")
