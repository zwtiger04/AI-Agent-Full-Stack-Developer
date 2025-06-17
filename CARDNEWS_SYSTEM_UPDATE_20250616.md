# 📋 카드뉴스 시스템 구조 업데이트 (2025-06-16)

## 🔄 주요 변경사항

### 1. 파일 경로 통일
#### 이전 (문제점)
- **두 개의 pending_cardnews.json 파일이 존재**
  - `./pending_cardnews.json` - 실제 데이터 (34개)
  - `data/card_news/json/pending_cardnews.json` - 통계용 (2개)
- 서로 다른 파일을 참조하여 데이터 불일치 발생

#### 현재 (해결)
- **단일 파일 사용**: `data/card_news/json/pending_cardnews.json`
- **상수 사용**: `PENDING_CARDNEWS_FILE`
- 모든 모듈에서 동일한 파일 참조

### 2. 노션 연동 구조

```
┌─────────────────────┐     ┌─────────────────────┐
│   Notion Database   │────▶│ InterestMonitor     │
│  (관심 체크 기사)    │     │ (watch_interested)  │
└─────────────────────┘     └──────────┬──────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │ pending_cardnews    │
                            │      .json          │
                            └──────────┬──────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │  Streamlit App      │
                            │ (card_news_app.py)  │
                            └─────────────────────┘
```

### 3. 주요 함수 및 클래스

#### CardNewsGenerator
- `load_pending_articles()`: 대기 중인 기사 로드
- `generate_card_news()`: 카드뉴스 생성
- `cost_manager`: 비용 관리

#### InterestMonitor
- `check_new_interests()`: 노션에서 새 관심 기사 확인
- `save_pending_articles()`: 기사 목록 저장

#### load_interested_articles()
- 위치: `card_news_app.py`의 전역 함수
- 역할: 통일된 경로에서 기사 로드

## 📁 파일 구조

```
AI-Agent-Full-Stack-Developer/
├── card_news_app.py              # 메인 Streamlit 앱
├── watch_interested_articles.py  # 노션 모니터링
├── run_level2.py                # 통합 실행 스크립트
├── data/
│   └── card_news/
│       └── json/
│           ├── pending_cardnews.json     # 관심 기사 목록 (통일)
│           ├── cost_tracking.json        # 비용 추적
│           └── processed_articles.json   # 처리된 기사
└── notion/
    └── notion_client.py         # 노션 API 클라이언트
```

## 🔧 환경 변수

```bash
# .env 파일 필수 항목
NOTION_API_KEY=secret_xxxxx
NOTION_PARENT_PAGE_ID=2002360b26038007a59fcda976552022
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

## 🚀 실행 방법

### 1. 개별 실행
```bash
# 노션 모니터링 (백그라운드)
python3 watch_interested_articles.py &

# Streamlit 앱
streamlit run card_news_app.py
```

### 2. 통합 실행
```bash
python3 run_level2.py
```

## 📌 주의사항

1. **경로 하드코딩 금지**
   - 항상 `PENDING_CARDNEWS_FILE` 상수 사용
   - `card_news_paths` 모듈 활용

2. **파일 동기화**
   - 모든 모듈이 같은 파일을 참조하는지 확인
   - 레거시 파일 제거 필요

3. **노션 연동**
   - API 키 설정 필수
   - 주기적인 모니터링 필요

---
*최종 업데이트: 2025-06-16 12:50*
