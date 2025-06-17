# 파일 읽기
with open('card_news_app_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 테스트 모드 부분 수정
old_test_mode = '''    # 테스트 모드 설정
    test_mode = st.sidebar.checkbox(
        "🧪 테스트 모드",
        help="테스트 모드를 활성화하면 실제 API를 호출하지 않고 더미 카드뉴스를 생성합니다. 비용이 발생하지 않습니다."
    )
    if test_mode:
        st.sidebar.info("🧪 테스트 모드 활성화됨\\n실제 API 호출 없이 테스트합니다.")'''

new_test_mode = '''    # 사이드바 설정
    with st.sidebar:
        st.markdown("### ⚙️ 설정")
        test_mode = st.checkbox(
            "🧪 테스트 모드",
            help="테스트 모드를 활성화하면 실제 API를 호출하지 않고 더미 카드뉴스를 생성합니다. 비용이 발생하지 않습니다."
        )
        if test_mode:
            st.info("🧪 테스트 모드 활성화됨\\n실제 API 호출 없이 테스트합니다.")
        st.markdown("---")'''

content = content.replace(old_test_mode, new_test_mode)

# 파일 저장
with open('card_news_app_integrated.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("사이드바 개선 완료!")
