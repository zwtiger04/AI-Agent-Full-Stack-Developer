# 🤖 전력산업 뉴스 크롤러

> 전기신문 뉴스 자동 수집 및 Notion 동기화 시스템

## 🎯 주요 기능

- **🔍 스마트 크롤링**: 전기신문에서 전력산업 관련 뉴스 자동 수집
- **🤖 AI 필터링**: 머신러닝 기반 중요 기사 추천
- **📝 Notion 동기화**: 수집된 기사를 Notion 데이터베이스에 자동 저장
- **🔄 자동 학습**: 사용자 피드백 기반 AI 모델 지속 개선

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 프로젝트 클론
git clone <repository-url>
cd AI-Agent-Full-Stack-Developer

# 가상환경 생성 및 활성화 (Python 3.8+)
python -m venv venv
source venv/bin/activate  # zsh/bash
# 또는 venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# 필수 환경변수 설정
NOTION_TOKEN=your_notion_token
NOTION_PARENT_PAGE_ID=your_parent_page_id
```

### 3. 실행
```bash
# 메인 크롤러 실행
python main.py
```

## 📂 프로젝트 구조

```
AI-Agent-Full-Stack-Developer/
├── 📁 crawlers/           # 크롤링 엔진
│   ├── electimes_crawler.py  # 전기신문 크롤러
│   └── base_crawler.py       # 기본 크롤러 클래스
├── 📁 notion/             # Notion 연동
│   └── notion_client.py      # Notion API 클라이언트
├── 📁 processors/         # 데이터 처리
│   └── keyword_processor.py # 키워드 처리기
├── 📁 recommenders/       # AI 추천 시스템
│   └── article_recommender.py
├── 📁 config/             # 설정 파일
├── 📁 logs/               # 로그 파일
├── 📁 feedback/           # AI 학습 데이터
├── 📁 archive/            # 정리된 파일들
│   ├── debug_html/           # Debug HTML 파일들
│   ├── test_files/           # 테스트 파일들
│   ├── old_scripts/          # 이전 스크립트들
│   └── unused_files/         # 미사용 파일들
├── main.py                # 🚀 메인 실행 파일
├── ai_recommender.py      # AI 추천 모델
├── ai_update_content.py   # 콘텐츠 처리
└── requirements.txt       # 의존성 목록
```

## 🔧 핵심 모듈

### 1. ElectimesCrawler
- 전기신문 웹사이트 크롤링
- 키워드 기반 필터링 ('재생에너지', 'VPP', 'ESS' 등)
- AI 기반 중요도 판단

### 2. NotionClient  
- Notion API 연동
- 주간 데이터베이스 자동 생성
- 기사 메타데이터 및 콘텐츠 동기화

### 3. AI Recommender
- TF-IDF + LogisticRegression 기반
- 사용자 피드백 학습
- 실시간 추천 점수 업데이트

## 📊 워크플로우

```mermaid
graph TD
    A[환경설정] --> B[크롤링]
    B --> C[키워드 필터링]
    C --> D[AI 추천 필터링]
    D --> E[Notion 저장]
    E --> F[AI 모델 학습]
    F --> G[추천 업데이트]
```

## ⚙️ 설정

### 키워드 설정
```python
# crawlers/electimes_crawler.py
KEYWORDS = [
    '재생에너지', '전력중개사업', 'VPP', '전력시장', 'ESS',
    '출력제어', '중앙계약', '저탄소 용량', '기후에너지부',
    '태양광', '전력감독원'
]
```

### 크롤링 기준
- **날짜 범위**: 최근 3일 이내
- **페이지 수**: 최대 20페이지
- **필터링**: 키워드 + AI 추천

## 🔄 자동화

### 일일 실행
```bash
# 크론잡 설정 예시 (매일 오전 9시)
0 9 * * * cd /path/to/project && python main.py
```

### 도커 실행
```bash
# 도커 빌드 및 실행
docker-compose up -d
```

## 📈 모니터링

### 로그 확인
```bash
# 최신 로그 확인
tail -f logs/crawler_$(date +%Y%m%d).log
```

### 성능 지표
- 크롤링된 기사 수
- 필터링 통과율
- Notion 동기화 성공률
- AI 모델 정확도

## 🛠️ 개발

### 테스트 실행
```bash
# 테스트 파일들은 archive/test_files/에 보관됨
python -m pytest archive/test_files/
```

### 디버깅
- Debug HTML 파일들: `archive/debug_html/`
- 상세 로그: `logs/` 폴더

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.

## 🤝 기여

1. 이슈 생성
2. 기능 브랜치 생성
3. 변경사항 커밋
4. 풀 리퀘스트 생성

---

> **💡 팁**: 문제가 발생하면 `logs/` 폴더의 최신 로그를 먼저 확인하세요!
