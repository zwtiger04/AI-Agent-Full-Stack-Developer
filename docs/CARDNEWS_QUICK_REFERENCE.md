# 🚀 카드뉴스 시스템 빠른 참조 가이드

## 📁 핵심 파일 위치

### 실행 파일
```bash
card_news_app.py          # 메인 Streamlit 앱
update_summary.py         # 요약 페이지 업데이트
migrate_summary.py        # HTML→JSON 마이그레이션
```

### 데이터 파일
```bash
data/card_news/json/
├── cost_tracking.json         # 비용 추적
├── pending_cardnews.json      # 대기 중 카드뉴스
├── processed_articles.json    # 처리된 기사
└── summary_cards.json         # [NEW] 요약 카드 데이터
```

### 출력 파일
```bash
output/card_news/
├── html/                      # 상세 카드뉴스
├── summary/                   # [NEW] 요약 페이지
│   └── improved_summary.html
└── test/                      # 테스트 모드 파일
```

## 🔧 주요 클래스 및 메서드

### SummaryManager (summary_manager.py)
```python
manager = SummaryManager()
cards = manager.load_cards()                    # 전체 로드
manager.add_card(card_data)                     # 추가
filtered = manager.filter_cards(category="ESS") # 필터링
categories = manager.get_categories()           # 카테고리 목록
```

### CardNewsGenerator (card_news_app.py)
```python
generator = CardNewsGenerator(api_key)
html = generator.generate_card_news(article, theme, sections)
theme = generator.get_color_theme(keywords)
```

### CostManager (card_news_app.py)
```python
manager = CostManager()
can_generate, message = manager.can_generate()  # 한도 체크
daily = manager.get_daily_cost()               # 일일 비용
monthly = manager.get_monthly_cost()           # 월간 비용
```

## 📊 데이터 구조

### summary_cards.json
```json
{
    "cards": [{
        "id": "detail_제목_날짜",
        "title": "카드뉴스 제목",
        "summary": "요약 내용",
        "keywords": ["ESS", "VPP"],
        "date": "2025-06-16",
        "file_path": "detail_제목_날짜.html",
        "category": "ESS",
        "added_date": "2025-06-16T23:00:00"
    }]
}
```

### pending_cardnews.json
```json
[{
    "page_id": "노션_페이지_ID",
    "title": "기사 제목",
    "url": "원문 URL",
    "content": "기사 내용",
    "summary": "요약",
    "keywords": ["키워드"],
    "date": "날짜"
}]
```

## 🎨 UI 컴포넌트

### Streamlit 탭 구조
```python
tabs = st.tabs([
    "📰 카드뉴스 생성",
    "📚 요약 카드뉴스",      # [NEW]
    "📊 분석 대시보드",
    "📋 생성 기록",
    "💰 비용 관리",
    "ℹ️ 사용 안내"
])
```

### 카테고리 색상
```python
colors = {
    "ESS": "#FF6B6B",
    "VPP": "#4ECDC4",
    "재생에너지": "#45B7D1",
    "태양광": "#FFA500",
    "풍력": "#98D8C8"
}
```

## 🔄 핵심 플로우

### 카드뉴스 생성 플로우
```
1. 노션 관심 체크 → pending_cardnews.json
2. Streamlit 앱에서 선택
3. CardNewsGenerator.generate()
4. HTML 파일 생성 (output/card_news/html/)
5. update_summary.add_to_summary()
   ├── update_html_summary() → improved_summary.html
   └── update_json_summary() → summary_cards.json
```

### 요약 조회 플로우
```
1. "📚 요약 카드뉴스" 탭 선택
2. summary_ui.render_summary_tab()
3. SummaryManager.load_cards()
4. 필터링/검색 적용
5. display_card_grid() 표시
```

## 💡 자주 사용하는 명령어

### 실행
```bash
# 메인 앱 실행
streamlit run card_news_app.py

# 마이그레이션 (dry-run)
python3 migrate_summary.py --dry-run

# 테스트
python3 summary_manager.py
```

### 파일 확인
```bash
# JSON 데이터 확인
cat data/card_news/json/summary_cards.json | jq .

# 카드 개수 확인
cat data/card_news/json/summary_cards.json | jq '.cards | length'

# 특정 카테고리 필터
cat data/card_news/json/summary_cards.json | jq '.cards[] | select(.category == "ESS")'
```

## ⚠️ 주의사항

### 경로 관련
- 항상 상대 경로 사용
- card_news_paths.py 통해 경로 가져오기
- Windows 절대 경로 금지

### 하이브리드 모드
- HTML과 JSON 모두 업데이트
- 한쪽 실패해도 다른 쪽은 진행
- 롤백 가능하도록 백업 유지

### 타입 안전성
- @fully_validated 데코레이터 사용
- ensure_string() 으로 문자열 보장
- Union 타입으로 유연성 확보

---
*최종 업데이트: 2025-06-16 23:50*
