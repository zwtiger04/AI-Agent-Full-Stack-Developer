# 📋 카드뉴스 시스템 현황 문서
## 📅 최종 업데이트: 2025-06-17

---

## 🏗️ 시스템 아키텍처

### [ARCH-001] 전체 시스템 구조
```mermaid
graph LR
    A[전기신문 크롤링] --> B[노션 저장]
    B --> C[관심 표시]
    C --> D[카드뉴스 생성]
    D --> E[요약 페이지]
    E --> F[상세보기]
```

### [ARCH-002] 파일 구조
```
AI-Agent-Full-Stack-Developer/
├── card_news_app.py          # [FILE-001] 메인 Streamlit 앱
├── card_news_paths.py        # [FILE-002] 경로 관리 모듈
├── card_news/
│   ├── types.py             # [FILE-003] 타입 정의
│   ├── validators.py        # [FILE-004] 검증 시스템
│   ├── decorators.py        # [FILE-005] 데코레이터
│   └── test_mode_generator.py # [FILE-006] 테스트 모드
├── data/card_news/
│   └── json/
│       ├── summary_cards.json      # [JSON-001] 요약 카드 데이터
│       ├── cost_tracking.json      # [JSON-002] 비용 추적
│       ├── pending_cardnews.json   # [JSON-003] 대기 중 기사
│       └── processed_articles.json # [JSON-004] 처리 완료 기사
└── output/card_news/
    ├── html/                # [DIR-001] 생성된 카드뉴스 HTML
    └── templates/          # [DIR-002] CSS 템플릿
```

---

## 🔄 데이터 플로우

### [FLOW-001] 카드뉴스 생성 플로우
1. **크롤링** → `pending_cardnews.json`
2. **관심 표시** → Streamlit UI에서 선택
3. **생성** → Claude API 호출
4. **저장** → `output/card_news/html/`
5. **등록** → `summary_cards.json` 업데이트
6. **표시** → 요약 카드뉴스 탭

### [FLOW-002] 자세히보기 플로우
1. **요약 탭** → 카드 목록 표시
2. **파일 경로** → `summary_cards.json`에서 파일명 읽기
3. **절대 경로 변환** → `get_path('output_html') / filename`
4. **Base64 인코딩** → HTML 내용을 Data URL로 변환
5. **새창 열기** → `window.open(data_url, '_blank')`

---

## 📦 주요 컴포넌트

### [COMP-001] CostManager 클래스
```python
class CostManager:
    def __init__(self)
    def add_cost(amount: float, description: str)
    def get_daily_cost() -> float          # [METHOD-001]
    def get_monthly_cost() -> float        # [METHOD-002]
    def can_generate() -> Tuple[bool, str] # [METHOD-003]
```

### [COMP-002] CardNewsGenerator 클래스
```python
class CardNewsGenerator:
    def __init__(self)
    def generate_card_news(article, sections, theme) # [METHOD-004]
    def get_color_theme(keywords) -> Dict           # [METHOD-005]
    def save_to_file(content, article) -> str       # [METHOD-006]
```

### [COMP-003] TestModeGenerator 클래스
```python
class TestModeGenerator:
    def generate_test_card_news(article, sections, theme) # [METHOD-007]
```

### [COMP-004] 전역 함수
```python
def load_interested_articles() -> List[Dict]  # [FUNC-001]
def load_generated_card_news() -> List[Dict]  # [FUNC-002]
def render_summary_tab() -> None              # [FUNC-003]
def update_summary_json(article_info) -> None # [FUNC-004]
```

---

## ✅ 완료된 작업

### [DONE-001] TypeError 해결 (2025-06-15)
- 타입 시스템 구축
- 검증 시스템 구현
- @fully_validated 데코레이터 적용

### [DONE-002] 파일 경로 표준화 (2025-06-15)
- card_news_paths 모듈 생성
- 하드코딩된 경로 제거
- 자동 마이그레이션 구현

### [DONE-003] 카드뉴스 앱 통합 (2025-06-16)
- Phase 1-5 완료
- 테스트 모드 분리
- 5개 탭 구조 구현

### [DONE-004] 요약 페이지 Streamlit 통합 (2025-06-16)
- render_summary_tab() 구현
- 원본 스타일 100% 재현
- 탭 구조에 통합

### [DONE-005] 자세히보기 링크 수정 (2025-06-17)
- 경로 시스템 표준화
- 절대 경로 사용으로 변경
- 파일 존재 검증 추가
- 오류 처리 개선

---

## 📋 해야할 작업

### [TODO-001] 파일 서빙 방식 개선
- Base64 인코딩 대신 정적 파일 서빙 고려
- 대용량 파일 처리 최적화
- 캐싱 메커니즘 구현

### [TODO-002] 사용자 경험 개선
- 로딩 인디케이터 추가
- 파일 다운로드 옵션
- 같은 창에서 열기 옵션

### [TODO-003] 크롤링 스케줄러
- 자동 크롤링 시스템
- 중복 방지 강화
- 실시간 알림

### [TODO-004] AI 모델 고도화
- GPT-4 활용 검토
- 카드뉴스 템플릿 다양화
- 자동 카테고리 분류 개선

### [TODO-005] 대시보드 강화
- 실시간 통계
- 비용 예측 모델
- 성과 분석 지표

---

## 🔑 핵심 규칙

### [RULE-001] 경로 사용
```python
# ❌ 금지
path = "output/card_news/html/file.html"

# ✅ 필수
from card_news_paths import get_path, get_path_str
path = get_path('output_html') / 'file.html'
```

### [RULE-002] 메서드명 표준
- `get_daily_cost()` (~~get_today_cost()~~)
- `get_monthly_cost()` (~~get_month_cost()~~)
- `can_generate()` (~~check_limits()~~)
- `load_interested_articles()` (~~load_pending_articles()~~)

### [RULE-003] JSON 파일 키
| 용도 | 키 이름 | 파일 경로 |
|------|---------|-----------|
| 요약 카드 | `summary_json` | data/card_news/json/summary_cards.json |
| 비용 추적 | `cost_tracking` | data/card_news/json/cost_tracking.json |
| 대기 기사 | `pending_cardnews` | data/card_news/json/pending_cardnews.json |

### [RULE-004] 타입 검증
- 모든 생성 함수에 `@fully_validated` 적용
- Article, ThemeData 타입 사용
- 문자열은 `ensure_string()` 처리

---

## 📊 시스템 상태

### 현재 버전
- **card_news_app.py**: v3.0 (2025-06-17)
- **card_news_paths.py**: v1.2
- **타입 시스템**: v1.0

### 성능 지표
- 카드뉴스 생성: 평균 15초
- 요약 페이지 로딩: < 2초
- 메모리 사용: 안정적

### 알려진 이슈
- 없음 (2025-06-17 기준)

---

## 🚀 다음 마일스톤
1. **v3.1**: 파일 서빙 최적화
2. **v3.2**: 크롤링 자동화
3. **v4.0**: AI 모델 업그레이드

---

*이 문서는 카드뉴스 시스템의 현재 상태를 종합적으로 정리한 마스터 문서입니다.*
*모든 ID는 추적 가능하도록 고유하게 부여되었습니다.*
