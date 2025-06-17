# 📚 Streamlit 요약 페이지 완전 통합 상세 계획

## 📅 작성일: 2025-06-16
## 🎯 목표: 요약 페이지를 별도 HTML에서 Streamlit 탭으로 완전 통합

---

## 📋 전체 통합 계획 (5일 일정)

### Phase 1: 데이터 구조 준비 (Day 1)

#### 1.1 새로운 데이터 저장 구조
```python
# data/card_news/json/summary_cards.json
{
    "cards": [
        {
            "id": "unique_id",
            "title": "제목",
            "summary": "요약",
            "keywords": ["ESS", "VPP"],
            "date": "2025-06-16",
            "file_path": "detail_제목_날짜.html",
            "category": "ESS",
            "added_date": "2025-06-16T10:00:00"
        }
    ]
}
```

#### 1.2 마이그레이션 스크립트
```python
# migrate_summary_to_json.py
- improved_summary.html 파싱
- JSON 형식으로 변환
- 기존 링크 정보 보존
```

### Phase 2: Streamlit UI 구현 (Day 2-3)

#### 2.1 새로운 탭 추가
```python
# card_news_app.py 수정
tabs = st.tabs([
    "📰 카드뉴스 생성",
    "📚 요약 카드뉴스",  # 새 탭
    "📊 분석 대시보드",
    ...
])
```

#### 2.2 요약 페이지 UI 구현
```python
def render_summary_tab():
    st.header("📚 전력산업 카드뉴스 모음")
    
    # 필터링 옵션
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox("카테고리", ["전체", "ESS", "VPP", ...])
    with col2:
        date_filter = st.date_input("날짜 필터")
    with col3:
        search_term = st.text_input("검색")
    
    # 카드 그리드 표시
    display_summary_cards(category_filter, date_filter, search_term)
```

### Phase 3: 파일 참조 수정 (Day 3-4)

#### 3.1 update_summary.py 수정
```python
# 기존: HTML 파일 직접 수정
# 변경: JSON 데이터 업데이트
def add_to_summary(article, file_path, base_path=None):
    summary_data = load_summary_json()
    new_card = create_card_data(article, file_path)
    summary_data['cards'].append(new_card)
    save_summary_json(summary_data)
```

### Phase 4: 하위 호환성 유지 (Day 4-5)

#### 4.1 레거시 HTML 생성 (선택사항)
```python
def generate_static_summary_html():
    """기존 HTML 파일도 함께 생성 (하위 호환성)"""
    cards = load_summary_json()
    html = render_summary_html(cards)
    save_to_legacy_path(html)
```

---

## 📝 파일별 상세 수정 사항

### 1. card_news_app.py

#### 수정 사항:
```python
# Line 459, 575: 홈 버튼 제거
- <a href="../improved_summary.html" class="home-button">🏠</a>
+ <!-- 홈 버튼 제거 - Streamlit 탭으로 대체 -->

# Line 841: 탭 추가
- tabs = st.tabs(["📰 카드뉴스 생성", "📊 분석 대시보드", "📋 생성 기록", "💰 비용 관리", "ℹ️ 사용 안내"])
+ tabs = st.tabs(["📰 카드뉴스 생성", "📚 요약 카드뉴스", "📊 분석 대시보드", "📋 생성 기록", "💰 비용 관리", "ℹ️ 사용 안내"])

# 새로운 import 추가
+ from summary_manager import SummaryManager
+ from summary_ui import render_summary_tab
```

### 2. update_summary.py

#### 전면 리팩토링:
```python
# 기존 코드를 JSON 기반으로 변경
import json
from pathlib import Path
from card_news_paths import get_path_str

class SummaryUpdater:
    def __init__(self):
        self.json_path = Path(get_path_str('summary_json'))
        
    def add_to_summary(self, article, file_path, base_path=None):
        # JSON 업데이트 로직
        pass
```

### 3. 새 파일: summary_manager.py

```python
"""요약 카드뉴스 데이터 관리"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class SummaryManager:
    def __init__(self):
        self.data_path = Path(get_path_str('summary_json'))
        self.ensure_data_file()
    
    def load_cards(self) -> List[Dict]:
        """모든 카드 로드"""
        pass
    
    def add_card(self, card_data: Dict) -> bool:
        """새 카드 추가"""
        pass
    
    def filter_cards(self, category=None, date_range=None, search=None):
        """카드 필터링"""
        pass
```

### 4. 새 파일: summary_ui.py

```python
"""요약 카드뉴스 Streamlit UI"""
import streamlit as st
from summary_manager import SummaryManager

def render_summary_tab():
    """요약 카드뉴스 탭 렌더링"""
    manager = SummaryManager()
    
    # 헤더
    st.header("📚 전력산업 카드뉴스 모음")
    
    # 필터
    render_filters()
    
    # 카드 그리드
    render_card_grid(manager)
```

---

## 🛡️ 안전한 마이그레이션 전략

### 📌 핵심 원칙
1. **기존 기능 유지**: 마이그레이션 중에도 시스템은 정상 작동해야 함
2. **점진적 전환**: 한 번에 모든 것을 바꾸지 않고 단계별로 진행
3. **롤백 가능**: 문제 발생 시 즉시 이전 상태로 복구 가능

### 🔄 단계별 진행 계획

#### Step 0: 백업 및 준비 (30분)
```bash
# 1. 전체 백업
cp -r /mnt/c/Users/KJ/Desktop/EnhancedCardNews /mnt/c/Users/KJ/Desktop/EnhancedCardNews_backup_$(date +%Y%m%d)
cp update_summary.py update_summary.py.bak
cp card_news_app.py card_news_app.py.bak

# 2. 테스트 환경 준비
mkdir -p test_migration
cp improved_summary.html test_migration/
```

#### Step 1: 데이터 구조 준비 (2시간)
```python
# 1. card_news_paths.py에 경로 추가
'summary_json': str(data_dir / 'json' / 'summary_cards.json'),

# 2. 마이그레이션 스크립트 실행 (읽기만)
python3 migrate_summary.py --dry-run
```

#### Step 2: 하이브리드 모드 구현 (4시간)
```python
# update_summary.py 수정 - 이중 쓰기
def add_to_summary(article, file_path, base_path=None):
    # 1. 기존 HTML 업데이트 (유지)
    update_html_summary(article, file_path, base_path)
    
    # 2. 새로운 JSON도 업데이트 (추가)
    update_json_summary(article, file_path)
```

#### Step 3: Streamlit UI 추가 (4시간)
```python
# card_news_app.py - 새 탭 추가
with tab_summary:
    # 임시: 두 가지 뷰 제공
    view_mode = st.radio("보기 모드", ["새로운 뷰", "기존 HTML 링크"])
```

#### Step 4: 검증 및 전환 (2시간)

#### Step 5: 정리 (1시간)

### ⚠️ 위험 요소 및 대응 방안

1. **데이터 손실**: 백업 3중화
2. **링크 깨짐**: 심볼릭 링크 생성
3. **성능 저하**: 페이지네이션 구현
4. **UI 일관성**: 기존 CSS 재사용

### 📊 예상 일정
**총 예상 시간**: 13.5시간 (여유 포함 2일)

---

## 🎯 중요 코드 위치 및 수정 지점

### 1. update_summary.py

#### 현재 구조
```python
# Line 14: 요약 페이지 경로
SUMMARY_PATH = "/mnt/c/Users/KJ/Desktop/EnhancedCardNews/improved_summary.html"

# Line 49: add_to_summary 함수
def add_to_summary(article: Dict, file_path: str, base_path: Optional[str] = None) -> bool:
```

### 2. card_news_app.py

#### 현재 구조
```python
# Line 38: update_summary import
from update_summary import add_to_summary, update_summary_date

# Line 459, 575: 홈 버튼 HTML
<a href="../improved_summary.html" class="home-button">🏠</a>

# Line 841: 탭 생성
tabs = st.tabs(["📰 카드뉴스 생성", "📊 분석 대시보드", ...])

# Line 980-983: 요약 페이지 추가 호출
if add_to_summary(article, str(file_path), str(generator.output_dir)):
    st.success("📝 요약 페이지에 추가되었습니다!")
```

### 3. 신규 파일 생성 위치

```
AI-Agent-Full-Stack-Developer/
├── summary_manager.py      # 요약 데이터 관리 클래스
├── summary_ui.py          # Streamlit UI 컴포넌트
├── migrate_summary.py     # 마이그레이션 스크립트
└── data/card_news/json/
    └── summary_cards.json # 요약 데이터 저장
```

### 4. 테스트 시나리오

1. 새 카드뉴스 생성 → 요약 추가 확인
2. 기존 카드 표시 확인
3. 필터링/검색 동작 확인
4. 상세 페이지 링크 확인

### 5. 롤백 절차

```bash
# 문제 발생 시 롤백
cp update_summary.py.bak update_summary.py
cp card_news_app.py.bak card_news_app.py
rm data/card_news/json/summary_cards.json
rm summary_*.py
```
