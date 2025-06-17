# 📁 카드뉴스 파일 경로 구조 가이드

## ⚠️ 중요 공지 (2025-06-15 업데이트)
**기존 경로 구조가 완전히 변경되었습니다. 반드시 이 가이드를 참고하여 올바른 경로를 사용하세요.**

## 🚫 사용하지 말아야 할 경로 (DEPRECATED)

```bash
# ❌ 이전 경로들 - 더 이상 사용하지 마세요!
/mnt/c/Users/KJ/Desktop/EnhancedCardNews/detailed/  # Windows 직접 경로
./cost_tracking.json                                 # 프로젝트 루트의 JSON
./pending_cardnews.json                             # 프로젝트 루트의 JSON
./processed_articles.json                           # 프로젝트 루트의 JSON
```

## ✅ 새로운 표준 경로 구조

### 1. 기본 디렉토리 구조
```
/home/zwtiger/AI-Agent-Full-Stack-Developer/
├── data/card_news/
│   ├── json/                 # 모든 JSON 데이터 파일
│   │   ├── cost_tracking.json
│   │   ├── pending_cardnews.json
│   │   ├── processed_articles.json
│   │   └── generated_cardnews_history.json
│   ├── analytics/           # 분석 데이터
│   │   └── section_analytics.json
│   └── cache/              # 임시 캐시 파일
├── output/card_news/
│   ├── html/               # 생성된 카드뉴스 HTML
│   ├── images/             # 카드뉴스 이미지
│   └── templates/          # HTML 템플릿
├── backup/card_news/       # 자동 백업
│   └── YYYYMMDD_HHMMSS/   # 타임스탬프별 백업
├── logs/card_news/         # 로그 파일
│   ├── generation/         # 생성 로그
│   ├── errors/            # 오류 로그
│   └── access/            # 접근 로그
└── config/
    └── paths.json         # 경로 설정 파일
```

### 2. 코드에서 경로 사용법

#### ❌ 잘못된 사용법
```python
# 하드코딩된 경로 사용 금지
output_dir = "/mnt/c/Users/KJ/Desktop/EnhancedCardNews/detailed"
json_file = "pending_cardnews.json"
```

#### ✅ 올바른 사용법
```python
# 경로 관리자 사용
from card_news_paths import get_paths, get_path, get_path_str

# 경로 가져오기
paths = get_paths()
output_dir = get_path('output_html')  # Path 객체
json_file = get_path_str('pending_cardnews')  # 문자열

# 또는 직접 사용
PENDING_CARDNEWS_FILE = get_path_str('pending_cardnews')
```

### 3. 사용 가능한 경로 키

| 키 | 설명 | 실제 경로 |
|---|---|---|
| `cost_tracking` | 비용 추적 JSON | `data/card_news/json/cost_tracking.json` |
| `pending_cardnews` | 대기 중인 카드뉴스 | `data/card_news/json/pending_cardnews.json` |
| `processed_articles` | 처리된 기사 | `data/card_news/json/processed_articles.json` |
| `generated_history` | 생성 이력 | `data/card_news/json/generated_cardnews_history.json` |
| `section_analytics` | 섹션 분석 데이터 | `data/card_news/analytics/section_analytics.json` |
| `output_html` | HTML 출력 디렉토리 | `output/card_news/html/` |
| `output_images` | 이미지 출력 디렉토리 | `output/card_news/images/` |
| `logs` | 로그 디렉토리 | `logs/card_news/` |

### 4. 환경 변수 설정 (선택사항)

```bash
# .env 파일에 추가 (커스텀 경로가 필요한 경우)
CARDNEWS_ROOT=/custom/path/to/project

# 레거시 Windows 경로 (임시 호환성)
CARDNEWS_LEGACY_PATH=/mnt/c/Users/KJ/Desktop/EnhancedCardNews/detailed
```

### 5. 마이그레이션 체크리스트

- [ ] 모든 하드코딩된 경로를 `get_path()` 함수로 변경
- [ ] 프로젝트 루트의 JSON 파일이 `data/card_news/json/`로 이동되었는지 확인
- [ ] Windows 경로 참조를 제거하고 새 경로 사용
- [ ] `card_news_paths.py` import 추가
- [ ] 백업 폴더 확인 (`backup/card_news/`)

### 6. 문제 해결

#### Q: 기존 파일을 찾을 수 없다고 나올 때
```python
# 자동 마이그레이션 실행
from card_news_paths import get_paths
paths = get_paths()
migrated = paths.migrate_legacy_files()
print(f"마이그레이션된 파일: {migrated}")
```

#### Q: Windows에서 파일에 접근하려면?
```bash
# WSL 경로를 Windows 탐색기에서 열기
\\wsl$\Ubuntu\home\zwtiger\AI-Agent-Full-Stack-Developer\output\card_news\html

# 또는 생성된 배치 파일 실행
/mnt/c/Users/KJ/Desktop/EnhancedCardNews/file_locations.bat
```

#### Q: 권한 오류가 발생할 때
```python
# 권한 문제 시 대체 경로 자동 사용
# CardNewsPaths 클래스가 자동으로 처리
```

## 📌 핵심 규칙

1. **절대 하드코딩된 경로를 사용하지 마세요**
2. **항상 `card_news_paths` 모듈을 통해 경로를 가져오세요**
3. **새 파일 생성 시 적절한 디렉토리에 배치하세요**
4. **백업은 자동으로 생성됩니다**
5. **로그는 `logs/card_news/`에서 확인하세요**

---
*이 가이드는 2025-06-15 경로 표준화 작업의 일부로 작성되었습니다.*

## 🧪 테스트 모드 경로 관리 (2025-06-16 추가)

### 테스트 파일 경로
- **테스트 HTML 출력**: `output/card_news/test/`
- **파일명 규칙**: `TEST_detail_{제목}_{날짜}.html`
- **경로 키**: `output_test`

### 테스트 모드 파일 구분
```python
# 테스트 모드에 따른 경로 분기
if test_mode:
    output_dir = Path(get_path_str('output_test'))  # test/ 폴더
    filename = f"TEST_{base_filename}"
else:
    output_dir = generator.output_dir  # html/ 폴더
    filename = base_filename
```

### 테스트 파일 관리
- **위치**: Streamlit UI → "💰 비용 관리" 탭 → "🧪 테스트 파일 관리"
- **기능**:
  - 테스트 파일 개수 확인
  - 모든 테스트 파일 삭제
  - 7일 이상 된 파일 자동 정리

### 데이터 격리
테스트 모드에서는 다음 작업이 **차단**됩니다:
- ❌ `save_selection_analytics()` - 분석 통계 저장
- ❌ `add_to_summary()` - 요약 페이지 추가
- ❌ `mark_as_processed()` - 처리 완료 표시
- ❌ 비용 추적 업데이트

---
*테스트 모드 분리 작업: 2025-06-16 완료*

## 📚 요약 페이지 경로 관리 (2025-06-16 계획)

### 현재 경로
- **Windows HTML**: `/mnt/c/Users/KJ/Desktop/EnhancedCardNews/improved_summary.html`
- **상세 카드뉴스 (Windows)**: `/mnt/c/Users/KJ/Desktop/EnhancedCardNews/detailed/`
- **상세 카드뉴스 (WSL)**: `output/card_news/html/`

### 통합 후 경로
- **JSON 데이터**: `data/card_news/json/summary_cards.json`
- **경로 키**: `summary_json`
- **모든 파일이 프로젝트 내부로 통합**

### 마이그레이션 매핑
```python
# 기존 링크
onclick="window.location.href='detailed/파일명.html'"

# 통합 후 매핑
file_path = Path(get_path_str('output_html')) / filename
```

---
