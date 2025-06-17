import re

# 파일 읽기
with open('card_news_app_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 비용 정보 섹션에 테스트 모드 표시 추가
cost_expander_pattern = r'(with st\.expander\("💰 비용 정보", expanded=True\):)'
cost_expander_replacement = r'''\1
                        if test_mode:
                            st.info("🧪 테스트 모드에서는 비용이 발생하지 않습니다!")'''

content = re.sub(cost_expander_pattern, cost_expander_replacement, content)

# 2. 일일 한도 체크에 테스트 모드 처리 추가
daily_limit_pattern = r'if current_daily_cost \+ COST_PER_REQUEST > daily_limit:'
daily_limit_replacement = 'if not test_mode and current_daily_cost + COST_PER_REQUEST > daily_limit:'

content = content.replace(daily_limit_pattern, daily_limit_replacement)

# 3. 체크박스 처리에 테스트 모드 추가
checkbox_pattern = r'if st\.checkbox\(\s*"위 예상 비용을 확인했으며, 카드뉴스 생성에 동의합니다"'
checkbox_replacement = 'if test_mode or st.checkbox(\n                                "위 예상 비용을 확인했으며, 카드뉴스 생성에 동의합니다"'

content = re.sub(checkbox_pattern, checkbox_replacement, content)

# 4. spinner 메시지 수정
spinner_pattern = r'with st\.spinner\("🎨 카드뉴스 생성 중\.\.\. \(30초~1분 소요\)"\):'
spinner_replacement = '''with st.spinner("🎨 카드뉴스 생성 중..." + (" (테스트 모드)" if test_mode else " (30초~1분 소요)")):'''

content = content.replace(spinner_pattern, spinner_replacement)

# 5. 카드뉴스 생성 로직 수정
generation_pattern = r'# 카드뉴스 생성\s*\n\s*html_content = generator\.generate_card_news\('
generation_replacement = '''# 카드뉴스 생성
                                    if test_mode:
                                        # 테스트 모드: 더미 HTML 생성
                                        html_content = test_generator.generate_test_card_news(
                                            article, auto_theme, emphasis
                                        )
                                    else:
                                        # 실제 모드: API 호출
                                        html_content = generator.generate_card_news('''

content = re.sub(generation_pattern, generation_replacement, content)

# 6. 성공 메시지 수정
success_pattern = r'st\.success\(f"✅ 카드뉴스 생성 완료! \(비용: \$\{COST_PER_REQUEST\}\)"\)'
success_replacement = '''if test_mode:
                                            st.success("✅ 테스트 카드뉴스 생성 완료! (비용: $0.00)")
                                        else:
                                            st.success(f"✅ 카드뉴스 생성 완료! (비용: ${COST_PER_REQUEST})")'''

content = re.sub(success_pattern, success_replacement, content)

# 7. 비용 추적 업데이트에 테스트 모드 처리
cost_update_pattern = r'# 비용 추적 업데이트\s*\n\s*today = datetime'
cost_update_replacement = '''# 비용 추적 업데이트
                                        if not test_mode:
                                            today = datetime'''

content = re.sub(cost_update_pattern, cost_update_replacement, content)

# 8. 파일명에 테스트 표시 추가
filename_pattern = r'filename = f"detail_\{safe_title\}_\{timestamp\}\.html"'
filename_replacement = '''filename = f"detail_{'TEST_' if test_mode else ''}{safe_title}_{timestamp}.html"'''

content = content.replace(filename_pattern, filename_replacement)

# 파일 저장
with open('card_news_app_integrated.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("테스트 모드 로직 추가 완료!")
