import sys

# 파일 읽기
with open('card_news_app_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# API 키 처리 부분 찾기 및 수정
old_code = '''    # 탭 1: 카드뉴스 생성
    with tabs[0]:
        # API 키 확인
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            st.error("⚠️ ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다!")
            st.stop()
        
        # 생성기 초기화
        generator = CardNewsGenerator(api_key)'''

new_code = '''    # 탭 1: 카드뉴스 생성
    with tabs[0]:
        # API 키 처리 - 사이드바에서 입력받기
        with st.sidebar:
            st.markdown("### 🔑 API 설정")
            
            # 환경변수에서 기본값 로드
            env_api_key = os.getenv('ANTHROPIC_API_KEY', '')
            
            # API 키 입력 필드
            api_key = st.text_input(
                "Claude API Key",
                value=env_api_key,
                type="password",
                help="Claude API 키를 입력하세요. 환경변수가 설정되어 있으면 자동으로 로드됩니다.",
                key="anthropic_api_key"
            )
            
            if api_key:
                st.success("✅ API 키가 설정되었습니다")
            else:
                st.warning("⚠️ API 키를 입력해주세요")
            
            st.markdown("---")
        
        # API 키가 없으면 안내 메시지 표시
        if not api_key:
            st.error("⚠️ API 키가 설정되지 않았습니다!")
            st.info("""
            **API 키 설정 방법:**
            1. 왼쪽 사이드바에서 'API 설정' 섹션 확인
            2. Claude API 키 입력
            3. 또는 `.env` 파일에 `ANTHROPIC_API_KEY` 설정
            
            API 키는 [Anthropic Console](https://console.anthropic.com/)에서 발급받을 수 있습니다.
            """)
            st.stop()
        
        # 생성기 초기화
        generator = CardNewsGenerator(api_key)'''

# 내용 교체
if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ API 키 처리 코드가 성공적으로 수정되었습니다!")
else:
    print("❌ 대상 코드를 찾을 수 없습니다. 파일 구조가 변경되었을 수 있습니다.")
    sys.exit(1)

# 파일 저장
with open('card_news_app_integrated.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 파일이 성공적으로 업데이트되었습니다!")
