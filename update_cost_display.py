import re

# 파일 읽기
with open('card_news_app.py', 'r') as f:
    content = f.read()

# 1. 비용 경고 부분 수정
old_cost_warning = '''# 비용 경고
                st.markdown(f"""
                <div class="cost-warning">
                    <strong>💰 비용 안내</strong><br>
                    이 카드뉴스를 생성하면 <strong>${COST_PER_REQUEST}</strong> (약 {COST_PER_REQUEST_KRW}원)의 비용이 발생합니다.<br>
                    오늘 사용: ${today_cost:.2f} / ${daily_limit:.2f}<br>
                    이번 달: ${month_cost:.2f} / ${monthly_limit:.2f}
                </div>
                """, unsafe_allow_html=True)'''

new_cost_warning = '''# 비용 경고
                if test_mode:
                    st.markdown("""
                    <div class="cost-warning" style="background: #d1fae5; border-color: #10b981;">
                        <strong>🧪 테스트 모드 안내</strong><br>
                        테스트 모드에서는 <strong>비용이 발생하지 않습니다</strong>.<br>
                        실제 API를 호출하지 않고 템플릿 기반으로 카드뉴스를 생성합니다.<br>
                        생성된 파일은 별도의 테스트 폴더에 저장됩니다.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="cost-warning">
                        <strong>💰 비용 안내</strong><br>
                        이 카드뉴스를 생성하면 <strong>${COST_PER_REQUEST}</strong> (약 {COST_PER_REQUEST_KRW}원)의 비용이 발생합니다.<br>
                        오늘 사용: ${today_cost:.2f} / ${daily_limit:.2f}<br>
                        이번 달: ${month_cost:.2f} / ${monthly_limit:.2f}
                    </div>
                    """, unsafe_allow_html=True)'''

content = content.replace(old_cost_warning, new_cost_warning)

# 2. 체크박스 수정
old_checkbox = 'confirm = st.checkbox(f"비용 ${COST_PER_REQUEST} 발생을 확인했습니다", key=f"confirm_{idx}")'
new_checkbox = '''confirm = st.checkbox(
                            f"{'테스트 생성을 진행합니다' if test_mode else f'비용 ${COST_PER_REQUEST} 발생을 확인했습니다'}", 
                            key=f"confirm_{idx}"
                        )'''
content = content.replace(old_checkbox, new_checkbox)

# 3. 생성 완료 메시지 수정
old_success = 'st.success(f"✅ 카드뉴스 생성 완료! (비용: ${COST_PER_REQUEST})")'
new_success = '''st.success(f"✅ 카드뉴스 생성 완료! {'(테스트 모드 - 비용 없음)' if test_mode else f'(비용: ${COST_PER_REQUEST})'}")'''
content = content.replace(old_success, new_success)

# 4. 사용 안내의 비용 정보 수정
old_guide_cost = '- 기사당 비용: 약 $0.555'
new_guide_cost = '- 기사당 비용: 약 $0.555 (테스트 모드에서는 무료)'
content = content.replace(old_guide_cost, new_guide_cost)

# 파일 저장
with open('card_news_app.py', 'w') as f:
    f.write(content)

print("✅ 비용 표시 수정 완료!")
