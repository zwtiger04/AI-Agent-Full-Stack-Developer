# 🔌 전력산업 뉴스 크롤러 & 카드뉴스 자동화 시스템

## 📋 프로젝트 개요
- **목적**: 전력산업 관련 뉴스를 자동으로 수집하여 노션(Notion)에 정리하고 카드뉴스로 제작하는 통합 시스템
- **환경**: WSL (Windows Subsystem for Linux) - Ubuntu
- **위치**: `/home/zwtiger/AI-Agent-Full-Stack-Developer`
- **작성일**: 2025년 6월 10일

## 🏗️ 시스템 구성

### 1. 뉴스 크롤러 시스템
- 전기신문(electimes.com) 자동 크롤링
- 최근 3일 이내 기사 필터링
- 키워드 기반 선별 (재생에너지, VPP, ESS 등)
- AI 추천 시스템 (사용자 피드백 학습)

### 2. 노션 연동 시스템
- 주차별 데이터베이스 자동 생성
- 기사 요약 및 핵심 내용 자동 생성
- 중복 방지 및 업데이트 관리

### 3. 카드뉴스 제작 시스템
- Streamlit 기반 웹 UI
- Claude AI를 활용한 HTML 카드뉴스 생성
- 비용 관리 및 안전장치 포함

## 🚀 빠른 시작 가이드

### 1️⃣ 환경 설정
```bash
# 프로젝트 폴더로 이동
cd /home/zwtiger/AI-Agent-Full-Stack-Developer

# 가상환경 활성화 (있는 경우)
source venv/bin/activate

# 환경변수 설정 확인
cat .env
```

### 2️⃣ 기본 크롤링 실행
```bash
# 뉴스 크롤링 및 노션 동기화
python main.py
```

### 3️⃣ 카드뉴스 생성 (Level 2 자동화)
```bash
# 전체 시스템 실행
python3 run_level2.py

# 또는 UI만 실행
streamlit run card_news_app.py
```

## 📊 주요 기능

### 뉴스 크롤링
- **대상**: 전기신문 웹사이트
- **필터링 기준**:
  - 최근 3일 이내 기사
  - 키워드 포함 여부
  - AI 추천 점수
- **키워드 목록**:
  - 재생에너지, 전력중개사업, VPP, ESS
  - 태양광, 전력감독원, 전력망
  - 기후에너지부, 풍력, 해상풍력

### 노션 데이터베이스
- **자동 생성**: "전력 산업 뉴스 YYYY년 WW주차"
- **저장 정보**:
  - 제목, 출처, 날짜
  - 키워드 태그
  - 한줄요약 (AI 생성)
  - 핵심 내용 (AI 생성)
  - 원문 링크
  - 관심/AI추천 체크박스

### 카드뉴스 제작
- **트리거**: 노션에서 '관심' 표시한 기사
- **생성 방식**: Claude AI (HTML)
- **비용**: 기사당 약 $0.555 (750원)
- **안전장치**:
  - 사전 비용 고지
  - 일일/월간 한도 설정
  - 체크박스 확인 필수

## 📁 프로젝트 구조
```
AI-Agent-Full-Stack-Developer/
├── main.py                    # 메인 크롤러 실행
├── run_level2.py             # 카드뉴스 자동화 실행
├── card_news_app.py          # Streamlit UI
├── watch_interested_articles.py  # 관심 기사 모니터링
├── crawlers/                 # 크롤러 모듈
│   └── electimes_crawler.py  # 전기신문 크롤러
├── notion/                   # 노션 연동
│   └── notion_client.py      # 노션 API 클라이언트
├── feedback/                 # AI 모델 저장
├── detailed/                 # 생성된 카드뉴스 HTML
├── logs/                     # 실행 로그
└── .env                      # 환경변수 (API 키)
```

## 🔧 환경변수 설정

`.env` 파일 필수 항목:
```bash
# 노션 설정
NOTION_API_KEY=secret_xxxxx
NOTION_PARENT_PAGE_ID=2002360b26038007a59fcda976552022

# AI API
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx  # 선택사항

# GitHub (카드뉴스 이미지 업로드용)
GITHUB_TOKEN=ghp_xxxxx

# 크롤링 설정
CRAWL_INTERVAL=3600
MAX_ARTICLES=50
```

## 💰 비용 정보
- **크롤링/노션**: 무료
- **카드뉴스 생성**: 
  - Claude API 사용
  - 기사당 약 $0.555
  - 월 예상: $10-50 (사용량에 따라)

## 📝 사용 시나리오

### 일일 워크플로우
1. **아침**: `python main.py` 실행하여 새 기사 수집
2. **점검**: 노션에서 관심 있는 기사에 체크
3. **제작**: `python3 run_level2.py`로 카드뉴스 생성
4. **공유**: 생성된 HTML 파일 활용

### 주간 리포트
1. 노션 데이터베이스에서 주간 기사 확인
2. 관심 기사들로 카드뉴스 세트 제작
3. 요약 페이지 생성 및 공유

## 🛠️ 문제 해결

### 크롤링 오류
```bash
# 로그 확인
tail -f logs/crawler_*.log

# 수동 테스트
python -c "from crawlers.electimes_crawler import ElectimesCrawler; c = ElectimesCrawler(None); print(c.crawl())"
```

### 노션 연동 오류
```bash
# API 키 확인
grep NOTION .env

# 데이터베이스 ID 확인
python -c "from notion.notion_client import NotionClient; n = NotionClient(); print(n.get_weekly_database_id())"
```

### 카드뉴스 생성 오류
```bash
# Streamlit 포트 확인
lsof -i :8501

# 비용 추적 확인
cat cost_tracking.json
```

## 🚀 향후 개발 계획
1. **크롤러 확장**: 더 많은 뉴스 소스 추가
2. **AI 고도화**: GPT-4 활용 검토
3. **자동화 강화**: 스케줄러 추가
4. **UI 개선**: 더 나은 사용자 경험

## 📞 기술 지원
- **프로젝트 관리자**: KJ
- **개발 지원**: Claude AI (Anthropic)
- **문서 업데이트**: 2025년 6월 10일

---

⚡ **Power Industry News Automation System** - 전력산업의 미래를 함께 만들어갑니다!
