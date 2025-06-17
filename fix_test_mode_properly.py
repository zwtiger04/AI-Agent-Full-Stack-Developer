# 파일 읽기
with open('card_news_app_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# TestModeGenerator import 추가
if 'from card_news.test_mode_generator import TestModeGenerator' not in content:
    import_position = content.find('from card_news.section_analytics import SectionAnalytics')
    if import_position != -1:
        end_of_line = content.find('\n', import_position)
        content = content[:end_of_line+1] + 'from card_news.test_mode_generator import TestModeGenerator\n' + content[end_of_line+1:]

# main() 함수 내부에 테스트 모드 추가
# st.title 이후에 추가
main_content = '''def main():
    st.title("⚡ 전력산업 카드뉴스 생성기")
    st.markdown("---")
    
    # 테스트 모드 설정
    test_mode = st.sidebar.checkbox(
        "🧪 테스트 모드",
        help="테스트 모드를 활성화하면 실제 API를 호출하지 않고 더미 카드뉴스를 생성합니다. 비용이 발생하지 않습니다."
    )
    if test_mode:
        st.sidebar.info("🧪 테스트 모드 활성화됨\\n실제 API 호출 없이 테스트합니다.")
    
    # 분석 대시보드 인스턴스
    analytics_dashboard = AnalyticsDashboard()'''

# main() 함수 시작 부분 교체
old_main_start = '''def main():
    st.title("⚡ 전력산업 카드뉴스 생성기")
    st.markdown("---")
    
    # 분석 대시보드 인스턴스
    analytics_dashboard = AnalyticsDashboard()'''

content = content.replace(old_main_start, main_content)

# TestModeGenerator 초기화 추가
generator_init = '''        # 생성기 초기화
        generator = CardNewsGenerator(api_key)
        section_selector = SectionSelector()'''

new_generator_init = '''        # 생성기 초기화
        generator = CardNewsGenerator(api_key)
        test_generator = TestModeGenerator()
        section_selector = SectionSelector()'''

content = content.replace(generator_init, new_generator_init)

# 파일 저장
with open('card_news_app_integrated.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("테스트 모드 수정 완료!")
