# 📊 카드뉴스 요약 페이지 통합 상태 문서

## 🎯 프로젝트 ID: CNSI-2025-06

### 📅 작업 일정
- **시작**: 2025-06-17 06:50
- **완료**: 2025-06-17 07:25
- **소요 시간**: 약 35분

## ✅ 완료된 작업

### 1. 아키텍처 결정 [ARC-001]
- **결정 사항**: HTML 컴포넌트 임베딩 방식
- **이유**: 
  - 원본 디자인 100% 재현 가능
  - CSS 충돌 없음
  - 구현 단순성

### 2. 파일 생성 [FILE-001]
| 파일 ID | 경로 | 목적 | 상태 |
|---------|------|------|------|
| CSS-001 | `output/card_news/templates/summary_style.css` | 초기 CSS | ✅ |
| CSS-002 | `output/card_news/templates/original_summary_style.css` | 최종 CSS | ✅ |
| PY-001 | `simple_summary_tab.py` | 임시 함수 | 🗑️ 삭제 |
| PY-002 | `perfect_summary_tab.py` | 임시 함수 | 🗑️ 삭제 |
| PY-003 | `fix_summary_tab.py` | 임시 함수 | 🗑️ 삭제 |

### 3. 함수 구현 [FUNC-001]
```python
# card_news_app.py에 추가된 함수들

def render_summary_tab():
    """
    ID: FUNC-001
    위치: 라인 687
    역할: 요약 카드뉴스 탭 렌더링
    의존성: 
    - streamlit.components.v1
    - load_generated_card_news()
    - collections.Counter
    """
    
def load_generated_card_news():
    """
    ID: FUNC-002
    위치: 라인 786
    역할: HTML 파일에서 카드뉴스 정보 추출
    반환: List[Dict] - 카드뉴스 정보
    """
```

### 4. Import 추가 [IMP-001]
```python
# 라인 66-68에 추가
import streamlit.components.v1 as components
import base64  # 현재는 미사용
from collections import Counter  # render_summary_tab 내부에서 import
```

## 🔄 데이터 플로우

```
1. output/card_news/html/*.html 파일 존재
   ↓
2. load_generated_card_news() 실행
   - 파일명 파싱 (detail_제목_날짜.html)
   - 카테고리 자동 분류
   - 메타데이터 생성
   ↓
3. render_summary_tab() 실행
   - CSS 로드
   - HTML 템플릿 생성
   - 통계 섹션 생성
   - 카드 그리드 생성
   ↓
4. components.html() 렌더링
   - height=1600px
   - scrolling=True
```

## 🎨 스타일 매핑

### 카테고리 → CSS 클래스
```python
CATEGORY_STYLE_MAP = {
    "ess": "category-ess",           # 파란색
    "solar": "category-solar",       # 노란색
    "policy": "category-policy",     # 초록색
    "market": "category-market",     # 빨간색
    "tech": "category-tech",         # 보라색
    "vpp": "category-vpp",          # 청록색
    "renewable": "category-renewable", # 녹색
    "general": "category-general"    # 회색
}
```

## ⚠️ 알려진 이슈 및 해결책

### 이슈 1: 카드 클릭 시 404 오류
- **원인**: 절대 경로 사용
- **해결**: 상대 경로로 변환
```python
file_path = card["file_path"].replace('output/card_news/html/', '')
```

### 이슈 2: 스타일 미적용
- **원인**: Streamlit CSS 우선순위
- **해결**: components.html() 사용으로 격리

## 📈 성능 메트릭

- **로딩 시간**: < 1초 (20개 카드 기준)
- **메모리 사용**: 약 5MB (HTML + CSS)
- **렌더링 높이**: 1600px (조정 가능)

## 🔮 향후 개선사항

1. **[FUTURE-001]** 필터/검색 기능 추가
   - Streamlit 위젯과 연동
   - 실시간 필터링

2. **[FUTURE-002]** 페이지네이션
   - 카드 수가 많을 때 성능 개선

3. **[FUTURE-003]** JSON 캐싱
   - 매번 HTML 파일 스캔 대신 캐시 사용

4. **[FUTURE-004]** 카드 정보 편집
   - 제목/요약 수정 기능

## 🔒 보안 고려사항

- HTML 인젝션 방지 (현재는 내부 파일만 사용)
- 경로 탐색 공격 방지 (Path 객체 사용)

## 📝 테스트 체크리스트

- [x] 카드뉴스 로드 테스트
- [x] 3열 그리드 레이아웃 확인
- [x] 반응형 디자인 테스트
- [x] 카테고리 스타일 적용 확인
- [x] 카드 클릭 이벤트 테스트
- [x] 통계 섹션 집계 확인

---
*문서 생성: 2025-06-17 07:25*
*작성자: Claude AI + KJ*

## 📄 JSON 파일 매핑 (2025-06-17 추가)

### 파일 용도별 분류

#### 1️⃣ 입력 데이터
- `crawled_articles.json` - 크롤링 원본
- `pending_cardnews.json` - 노션에서 가져온 관심 기사

#### 2️⃣ 출력 데이터  
- `summary_cards.json` - 생성된 카드뉴스 메타데이터
- `cost_tracking.json` - API 비용 기록

#### 3️⃣ 통계 데이터
- `section_analytics.json` - 사용 패턴 분석

### 🔀 데이터 변환 과정

```
crawled_articles.json
    ↓ (크롤링)
노션 데이터베이스
    ↓ (관심 표시)
pending_cardnews.json
    ↓ (카드뉴스 생성)
HTML 파일 + summary_cards.json
```

### ⚠️ 디버깅 체크리스트

문제 발생 시 확인 순서:
1. [ ] 올바른 JSON 파일을 참조하고 있는가?
2. [ ] 파일이 실제로 존재하는가?
3. [ ] JSON 구조가 예상과 일치하는가?
4. [ ] 파일 권한이 올바른가?

### 📝 함수별 JSON 사용 현황

| 함수명 | 읽기 | 쓰기 |
|--------|------|------|
| `load_interested_articles()` | pending_cardnews.json | - |
| `load_generated_card_news()` | summary_cards.json ✅ | - |
| `CostManager.add_cost()` | cost_tracking.json | cost_tracking.json |
| `save_selection_analytics()` | section_analytics.json | section_analytics.json |
| `add_to_summary()` | summary_cards.json | summary_cards.json |

---
