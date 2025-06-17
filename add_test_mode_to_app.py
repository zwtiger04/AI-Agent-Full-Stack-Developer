import re

# 파일 읽기
with open('card_news_app_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Import 섹션에 TestModeGenerator 추가
import_pattern = r'(from card_news\.section_analytics import SectionAnalytics)'
import_replacement = r'\1\nfrom card_news.test_mode_generator import TestModeGenerator'
content = re.sub(import_pattern, import_replacement, content)

# 2. main() 함수 시작 부분 찾기
# "st.set_page_config" 이후에 테스트 모드 설정 추가
config_pattern = r'(st\.set_page_config\([^)]+\))'
config_replacement = r'''\1
    
    # 사이드바에 테스트 모드 토글 추가
    with st.sidebar:
        st.markdown("### ⚙️ 설정")
        test_mode = st.checkbox(
            "🧪 테스트 모드",
            help="테스트 모드를 활성화하면 실제 API를 호출하지 않고 더미 카드뉴스를 생성합니다. 비용이 발생하지 않습니다."
        )
        if test_mode:
            st.info("🧪 테스트 모드 활성화됨\\n실제 API 호출 없이 테스트합니다.")
        st.markdown("---")'''

content = re.sub(config_pattern, config_replacement, content, count=1)

# 3. CardNewsGenerator 초기화 부분 수정
generator_pattern = r'generator = CardNewsGenerator\(\)'
generator_replacement = '''generator = CardNewsGenerator()
    test_generator = TestModeGenerator()'''
content = re.sub(generator_pattern, generator_replacement, content)

# 4. 생성 버튼 클릭 시 처리 로직 수정
# "with st.spinner" 부분을 찾아서 수정
spinner_pattern = r'with st\.spinner\("🎨 카드뉴스 생성 중\.\.\. \(30초~1분 소요\)"\):\s*\n\s*# 카드뉴스 생성\s*\n\s*html_content = generator\.generate_card_news\('
spinner_replacement = '''with st.spinner("🎨 카드뉴스 생성 중..." + (" (테스트 모드)" if test_mode else " (30초~1분 소요)")):
                                    # 카드뉴스 생성
                                    if test_mode:
                                        # 테스트 모드: 더미 HTML 생성
                                        html_content = test_generator.generate_test_card_news(
                                            article, auto_theme, emphasis
                                        )
                                        # 비용 없음
                                        st.warning("🧪 테스트 모드로 생성되었습니다. 실제 API는 호출되지 않았습니다.")
                                    else:
                                        # 실제 모드: API 호출
                                        html_content = generator.generate_card_news('''

content = re.sub(spinner_pattern, spinner_replacement, content, flags=re.DOTALL)

# 5. 비용 표시 부분 수정
cost_pattern = r'st\.success\(f"✅ 카드뉴스 생성 완료! \(비용: \$\{COST_PER_REQUEST\}\)"\)'
cost_replacement = '''if test_mode:
                                        st.success("✅ 테스트 카드뉴스 생성 완료! (비용: $0.00)")
                                    else:
                                        st.success(f"✅ 카드뉴스 생성 완료! (비용: ${COST_PER_REQUEST})")'''
content = re.sub(cost_pattern, cost_replacement, content)

# 6. 비용 추적 부분 수정 - 테스트 모드에서는 비용 추적하지 않음
cost_tracking_pattern = r'# 비용 추적 업데이트\s*\n\s*today = datetime\.now\(\)\.strftime'
cost_tracking_replacement = '''# 비용 추적 업데이트 (테스트 모드에서는 건너뛰기)
                                        if not test_mode:
                                            today = datetime.now().strftime'''

content = re.sub(cost_tracking_pattern, cost_tracking_replacement, content)

# 7. 파일명 생성 부분에 테스트 표시 추가
filename_pattern = r'filename = f"detail_\{safe_title\}_\{timestamp\}\.html"'
filename_replacement = '''filename = f"detail_{'TEST_' if test_mode else ''}{safe_title}_{timestamp}.html"'''
content = re.sub(filename_pattern, filename_replacement, content)

# 파일 저장
with open('card_news_app_integrated.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("테스트 모드 추가 완료!")
