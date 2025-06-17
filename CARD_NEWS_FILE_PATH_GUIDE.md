# 📁 카드뉴스 파일 경로 관리 가이드

## 📅 최종 업데이트: 2025-06-17

---

## 🗂️ 디렉토리 구조

```
/home/zwtiger/AI-Agent-Full-Stack-Developer/
│
├── data/card_news/
│   ├── json/                      # JSON 데이터 파일
│   │   ├── summary_cards.json     # 요약 카드 메타데이터
│   │   ├── cost_tracking.json     # 비용 추적
│   │   ├── pending_cardnews.json  # 대기 중 기사
│   │   └── processed_articles.json # 처리 완료 기사
│   └── analytics/
│       └── section_analytics.json  # 섹션 분석 데이터
│
└── output/card_news/
    ├── html/                      # 실제 카드뉴스 HTML
    │   ├── detail_SK이터닉스-40MW-규모-태양광-직접전력거래계약-체결_2062360b.html
    │   ├── detail_엔라이튼-AJ네트웍스-천안센터-669kW-자가용-태양광-구축RE100-전환점_20b2360b.html
    │   └── ... (18개 파일)
    ├── test/                      # 테스트 모드 출력
    │   └── TEST_detail_*.html
    └── templates/                 # 스타일 템플릿
        └── original_summary_style.css
```

---

## 📋 파일명 규칙

### 1. 상세 카드뉴스 (실제)
- **패턴**: `detail_{제목}_{고유ID}.html`
- **위치**: `output/card_news/html/`
- **예시**: 
  ```
  detail_SK이터닉스-40MW-규모-태양광-직접전력거래계약-체결_2062360b.html
  detail_그린피스-이재명-정부에-기후위기-속-지속가능한-구조-전환-촉구_2082360b.html
  ```

### 2. 테스트 카드뉴스
- **패턴**: `TEST_detail_{제목}_{timestamp}.html`
- **위치**: `output/card_news/test/`
- **특징**: 
  - TEST_ 접두사로 구분
  - 요약 페이지에 포함되지 않음
  - 통계에 집계되지 않음

### 3. 파일명 생성 규칙
```python
# 실제 모드
filename = f"detail_{safe_title}_{article_id}.html"

# 테스트 모드
filename = f"TEST_detail_{safe_title}_{timestamp}.html"

# 안전한 제목 변환
safe_title = re.sub(r'[^\w\s-]', '', title)
safe_title = re.sub(r'[-\s]+', '-', safe_title)
```

---

## 🔄 파일 경로 접근 방법

### ❌ 잘못된 방법
```python
# 하드코딩된 경로
path = "output/card_news/html/detail.html"
path = "/home/zwtiger/AI-Agent-Full-Stack-Developer/output/card_news/html/"
```

### ✅ 올바른 방법
```python
from card_news_paths import get_path, get_path_str

# Path 객체로 받기
html_dir = get_path('output_html')
file_path = html_dir / filename

# 문자열로 받기
json_path = get_path_str('summary_json')
```

---

## 📊 파일 관리 현황

### 현재 파일 수 (2025-06-17)
- **상세 카드뉴스**: 18개
- **JSON 데이터**: 5개
- **총 용량**: 약 0.3MB

### 주요 파일 목록
```
1. detail_SK이터닉스-40MW-규모-태양광-직접전력거래계약-체결_2062360b.html
2. detail_엔라이튼-AJ네트웍스-천안센터-669kW-자가용-태양광-구축RE100-전환점_20b2360b.html
3. detail_전력거래소-나주서-ESS-입찰-설명회중앙계약시장-제도-전환-본격화_20b2360b.html
4. detail_전남도-시군-계통안정-ESS-지원단-운영지역-사업자-진출-돕기로_20b2360b.html
5. detail_LG에너지솔루션-美에서-ESS용-LFP-배터리-대규모-양산-시작_2062360b.html
```

---

## 🔍 파일 검색 및 관리

### 파일 찾기
```python
# 특정 파일 존재 확인
file_path = get_path('output_html') / 'detail_xxx.html'
if file_path.exists():
    print(f"파일 발견: {file_path}")

# 모든 카드뉴스 파일 목록
html_dir = get_path('output_html')
card_files = list(html_dir.glob('detail_*.html'))
```

### 파일 정리
```python
# 오래된 파일 정리 (30일 이상)
from datetime import datetime, timedelta

cutoff_date = datetime.now() - timedelta(days=30)
for file in html_dir.glob('detail_*.html'):
    if file.stat().st_mtime < cutoff_date.timestamp():
        print(f"삭제 대상: {file.name}")
```

---

## ⚠️ 주의사항

1. **경로 하드코딩 금지**
   - 항상 `card_news_paths` 모듈 사용

2. **파일명 중복 방지**
   - 고유 ID 또는 타임스탬프 포함

3. **테스트 파일 분리**
   - TEST_ 접두사 필수
   - 별도 디렉토리 사용

4. **정기적인 정리**
   - 오래된 테스트 파일 삭제
   - 용량 모니터링

---

## 🚀 향후 개선 사항

1. **자동 정리 시스템**
   - 30일 이상 된 테스트 파일 자동 삭제
   - 용량 임계치 관리

2. **파일 버전 관리**
   - 수정 이력 추적
   - 백업 자동화

3. **CDN 연동**
   - 정적 파일 외부 호스팅
   - 로딩 속도 개선

---

*이 문서는 카드뉴스 파일 경로 관리를 위한 참조 가이드입니다.*
