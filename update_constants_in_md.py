import re

# 파일 읽기
with open('INTEGRATED_PROJECT_GUIDE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 파일 구조 표준 섹션 찾아서 업데이트
file_structure_section = '''#### 데이터 파일 규칙
```python
# 설정 파일
COST_TRACKING_FILE = 'cost_tracking.json'              # 비용 추적
PENDING_CARDNEWS_FILE = 'pending_cardnews.json'        # 대기 중 기사
PROCESSED_ARTICLES_FILE = 'processed_articles.json'    # 처리 완료 기사
GENERATED_HISTORY_FILE = 'generated_cardnews_history.json'  # 생성 이력

# 디렉토리 구조
OUTPUT_DIR = 'card_news/'                   # 카드뉴스 출력
SECTION_STYLES_PATH = 'card_news/section_styles.css'
ANALYTICS_DATA_DIR = 'analytics_data/'      # 분석 데이터
LOGS_DIR = 'logs/'                         # 로그 파일
```'''

new_file_structure_section = '''#### 데이터 파일 규칙
```python
# ⚠️ 절대 변경 금지! 아래 상수만 사용할 것
# 비용 관련 상수 (2025년 6월 기준)
COST_PER_REQUEST = 0.555                    # USD - Claude API 요청당 비용
COST_PER_REQUEST_KRW = 750                  # KRW - 원화 환산 비용

# JSON 파일 경로 (절대 임의로 변경하지 말 것)
COST_TRACKING_FILE = 'cost_tracking.json'              # 비용 추적
PENDING_CARDNEWS_FILE = 'pending_cardnews.json'        # 대기 중 기사
PROCESSED_ARTICLES_FILE = 'processed_articles.json'    # 처리 완료 기사
GENERATED_HISTORY_FILE = 'generated_cardnews_history.json'  # 생성 이력

# 경로 상수 (절대 경로 문자열 직접 사용 금지)
SECTION_STYLES_PATH = 'card_news/section_styles.css'   # 섹션 스타일 CSS
OUTPUT_DIR = 'card_news/'                              # 카드뉴스 출력 디렉토리
ANALYTICS_DATA_DIR = 'analytics_data/'                 # 분석 데이터 디렉토리
LOGS_DIR = 'logs/'                                     # 로그 파일 디렉토리

# ❌ 금지 사항:
# - 'cost_tracking.json' 같은 문자열 직접 사용 금지
# - self.cost_file = 'cost_tracking.json' 형태 금지
# - 항상 위 상수 사용: self.cost_file = COST_TRACKING_FILE
```'''

content = content.replace(file_structure_section, new_file_structure_section)

# 금지 사항에도 추가
forbidden_addition = '''
5. **파일 경로 및 상수 임의 정의 금지**
   - ❌ `self.cost_file = 'cost_tracking.json'` - 직접 문자열 사용 금지
   - ✅ `self.cost_file = COST_TRACKING_FILE` - 상수만 사용
   - ❌ 새로운 파일 경로 상수 추가 금지
   - ❌ 비용 관련 수치 임의 변경 금지
'''

# 금지 사항 섹션에 추가
forbidden_pattern = r'4\. \*\*파일명 임의 변경 금지\*\*\n   - 정의된 상수만 사용 \(COST_TRACKING_FILE 등\)'
new_forbidden = '''4. **파일명 임의 변경 금지**
   - 정의된 상수만 사용 (COST_TRACKING_FILE 등)''' + forbidden_addition

content = re.sub(forbidden_pattern, new_forbidden, content)

# 파일 저장
with open('INTEGRATED_PROJECT_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 상수 정의가 MD 파일에 명확히 반영되었습니다!")
