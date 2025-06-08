# 🔌 전력산업 기사 크롤링-노션 연동 프로젝트 구조 분석

## 📁 프로젝트 기본 정보
- **위치**: `/home/zwtiger/AI-Agent-Full-Stack-Developer`
- **환경**: WSL (Windows Subsystem for Linux)
- **목적**: 전력산업 관련 뉴스를 자동으로 크롤링하여 노션(Notion)에 정리하고 AI 추천 시스템으로 관리
- **작성일**: 2025-06-08

## 🏗️ Main.py 구조 및 실행 흐름

### 1. **초기 설정 단계**
```python
# 로깅 시스템 설정 - 실행 기록을 logs 폴더에 날짜별로 저장
setup_logging()

# 환경변수 로드 (.env 파일에서 API 키 등 불러오기)
load_dotenv()
```

### 2. **주요 구성 요소 초기화**
```python
# Notion 클라이언트 생성 (노션 API 연결)
notion = NotionClient()

# 전기신문 크롤러 생성 (웹 크롤링 담당)
crawler = ElectimesCrawler(notion)
```

### 3. **메인 프로세스 (6단계)**

**단계 1️⃣: 노션 클라이언트 초기화**
- 노션 API 키로 연결 설정
- 데이터를 저장할 준비

**단계 2️⃣: 기사 크롤링**
- 전기신문 웹사이트에서 최근 3일 이내 기사 수집
- 키워드 필터링: `재생에너지`, `전력중개사업`, `VPP`, `ESS`, `태양광` 등
- AI 모델이 있으면 추가 필터링 적용

**단계 3️⃣: 노션 데이터베이스 연결**
- 현재 주차에 맞는 데이터베이스 찾기 (예: "전력 산업 뉴스 2025년 24주차")
- 없으면 새로 생성

**단계 4️⃣: 노션 동기화**
- 크롤링한 기사를 노션에 저장
- 중복 방지: URL이 같은 기사는 업데이트만 수행
- 각 기사마다 생성되는 정보:
  - 제목, 출처, 날짜
  - 키워드 태그
  - 한줄요약 (AI 생성)
  - 핵심 내용 (AI 생성)
  - 원문 링크

**단계 5️⃣: AI 추천 모델 학습**
- 사용자가 '관심' 표시한 기사들을 학습 데이터로 사용
- 향후 비슷한 기사를 자동으로 추천하도록 모델 훈련

**단계 6️⃣: AI 추천 업데이트**
- 기존 기사들에 대해 AI 추천 여부 업데이트
- 'AI추천' 체크박스 자동 설정

## 🔧 주요 파일 및 역할

### **환경 설정 파일**
- `.env`: API 키와 설정값 저장
  - `NOTION_API_KEY`: 노션 연결용
  - `OPENAI_API_KEY`: ChatGPT 사용 (요약/핵심내용 생성)
  - `CRAWL_INTERVAL`: 크롤링 주기 (3600초 = 1시간)
  - `MAX_ARTICLES`: 한 번에 가져올 최대 기사 수

### **핵심 모듈**
1. **crawlers/electimes_crawler.py**
   - 전기신문 웹사이트 크롤링
   - Selenium 웹드라이버로 동적 페이지 처리
   - 키워드 매칭 및 날짜 필터링

2. **notion/notion_client.py**
   - 노션 API 통신 담당
   - 데이터베이스 생성/조회/업데이트
   - 기사 페이지 생성 및 관리

3. **ai_recommender.py**
   - AI 추천 모델 학습
   - 사용자 피드백 기반 개인화

4. **ai_update_content.py**
   - ChatGPT API로 기사 요약 생성
   - 핵심 내용 추출

## 💡 실행 방법

```bash
# WSL 터미널에서
cd /home/zwtiger/AI-Agent-Full-Stack-Developer

# Python 가상환경 활성화 (있는 경우)
source venv/bin/activate

# 메인 스크립트 실행
python main.py
```

## 📊 데이터 흐름

```
전기신문 웹사이트
    ↓ (크롤링)
ElectimesCrawler
    ↓ (필터링: 날짜, 키워드, AI)
크롤링된 기사 리스트
    ↓ (동기화)
NotionClient
    ↓ (저장)
노션 데이터베이스
    ↓ (피드백)
AI 추천 모델 학습
```

## 🔍 주요 기능별 상세 설명

### **키워드 필터링 시스템**
- 고정 키워드 리스트로 관련 기사만 선별
- 제목과 본문 모두에서 키워드 검색
- 매칭된 키워드는 노션에 태그로 저장

### **AI 추천 시스템**
- 사용자가 '관심' 체크한 기사들을 positive 샘플로 학습
- LogisticRegression 모델 사용
- TF-IDF 벡터화로 텍스트를 숫자로 변환

### **자동 요약 시스템**
- OpenAI API (ChatGPT) 활용
- 긴 기사 본문을 한 줄로 요약
- 핵심 내용 3-5개 포인트로 정리

## 📁 프로젝트 디렉토리 구조

```
AI-Agent-Full-Stack-Developer/
├── main.py                 # 메인 실행 스크립트
├── .env                    # 환경변수 (API 키 등)
├── requirements.txt        # Python 패키지 목록
├── crawlers/              # 크롤러 모듈
│   ├── __init__.py
│   ├── base_crawler.py    # 크롤러 기본 클래스
│   └── electimes_crawler.py # 전기신문 크롤러
├── notion/                # 노션 연동 모듈
│   ├── __init__.py
│   └── notion_client.py   # 노션 API 클라이언트
├── processors/            # 데이터 처리 모듈
│   └── keyword_processor.py
├── recommenders/          # AI 추천 모듈
│   └── article_recommender.py
├── feedback/              # AI 모델 및 피드백 데이터
├── logs/                  # 실행 로그
└── venv/                  # Python 가상환경
```

## 🔐 보안 주의사항

- `.env` 파일에는 민감한 API 키가 포함되어 있으므로 절대 공개 저장소에 업로드하지 않아야 함
- `.gitignore`에 `.env` 파일이 포함되어 있는지 확인 필요

## 🚀 향후 개선 가능 사항

1. **다양한 뉴스 소스 추가**
   - 현재는 전기신문만 크롤링
   - 다른 전력산업 관련 매체 추가 가능

2. **크롤링 스케줄러**
   - 현재는 수동 실행
   - cron이나 스케줄러로 자동화 가능

3. **AI 모델 고도화**
   - 더 정교한 추천 알고리즘 적용
   - 사용자별 개인화 강화

4. **Zapier 연동**
   - 노션 외 다른 서비스와 연동
   - 자동화 워크플로우 구축
