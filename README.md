# Power Industry News Crawler

## 최근 작업 내역 (2025-06-02)

- Ollama API 응답 파싱 로직 수정: 생성된 요약과 핵심 내용을 정확히 추출하도록 개선
- 키워드 분석 시스템 개선 필요성 확인: 현재 키워드 도출이 정교하지 못한 문제 발견
- Notion 동기화 시 기존 기사 업데이트 로직 개선: 출처, 한줄요약, 핵심 내용 업데이트 기능 추가
- .cursorrules의 코딩 규칙을 숙지하고 일관성 있게 개발 진행
- Notion 연동을 위해 .env에 NOTION_PARENT_PAGE_ID 환경변수 추가 및 사용법 안내
- Notion Parent Page ID와 Page ID의 차이, 추출 방법 명확히 문서화
- ElectimesCrawler로 기사 크롤링 및 Notion 동기화 테스트: notion_client import 경로 수정, 크롤링 결과 기사 링크 수집 정상, 키워드 필터로 실제 동기화 기사 없음 확인
- 크롤러가 메인 기사 외에 인기기사 등도 수집하던 문제를 section#section-list li.item 셀렉터로 수정하여 해결
- 최근 3일 이내 기사만 페이지를 넘기며 크롤링하도록 is_recent_article 기준 변경 및 페이지네이션 로직 개선
- Selenium 클릭 방식에서 URL 직접 조합 방식으로 페이지네이션 변경, 크롤링 안정성 향상
- 여러 페이지(최대 11페이지) 이동하며 3일 이내 기사 7건 크롤링 및 Notion 동기화 성공 확인
- AI 추천 기능 고도화를 위해 기사 본문 분석 필요성 확인
- 본문 분석을 위한 선행 작업으로 Notion DB 내 기존 기사들의 '바로가기' 링크 및 본문 내용 보완 필요
- **현재 Notion 기사 페이지 내부에 기사 원본 링크가 존재하는 것을 확인, 이를 활용하여 DB 컬럼 업데이트 계획**
- **한줄요약 및 핵심 내용 생성 방식 개선 및 `googletrans-py` 설치:**
  - 기존 LLM 기반 방식과 함께 규칙 기반 방식 추가 구현
  - `ai_update_content.py`에 규칙 기반 요약/핵심 내용 추출 함수 추가 (`generate_one_line_summary_rule_based`, `generate_key_content_rule_based`)
  - 기존 LLM 함수(`generate_one_line_summary_with_llm`, `generate_key_content`)에 `use_llm` 인자 추가하여 규칙 기반 함수 호출 기능 구현
  - `update_empty_fields.py` 스크립트에서 규칙 기반 함수를 사용하도록 변경 (`use_llm=False` 적용)
  - `notion_client.py`의 메인 동기화 로직에서도 규칙 기반 함수를 기본으로 사용하도록 변경 (`use_llm=False` 적용)
  - 필요에 따라 `use_llm=True`로 설정하여 LLM 기반 방식으로 전환 가능
- **AI 추천 시스템 역할 명확화:** 사용자 피드백 기반으로 AI 모델 학습 및 새로운 기사 추천에 활용하는 기능은 그대로 유지
- **크롤링 기준 명확화:** 전기신문에서 최근 3일 이내, 키워드 포함 기사만 크롤링하며, Notion 중복 체크는 동기화 단계에서 이루어짐을 확인

전력 산업 관련 뉴스와 공지사항을 자동으로 수집하고 Notion에 정리하는 시스템입니다.

## 주요 기능

- 전력 관련 주요 미디어 및 공공기관 웹사이트 크롤링 (현재: 전기신문)
- 최근 3일 이내, 키워드 포함 기사 필터링 및 수집
- **규칙 기반** 또는 **LLM 기반(선택 사항)** 한줄요약 및 핵심 내용 생성
- **주차별 Notion 데이터베이스 자동 생성 및 뉴스 데이터 동기화 (중복 기사 처리 포함)**
- 사용자 피드백 기반 **AI 추천** 시스템 (AI 추천 결과 Notion에 반영)
- 카드 뉴스 자동 생성 (향후 구현 예정)

## 설치 방법

1. Python 3.8 이상 설치
2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```
3. 환경 변수 설정:
   - `.env` 파일 생성 후 Notion API 키, MongoDB 연결 정보, **Notion Parent Page ID (`NOTION_PARENT_PAGE_ID`)** 설정

## 프로젝트 구조

```
power_news_crawler/
├── crawlers/           # 크롤링 모듈
├── processors/         # 데이터 처리 모듈
├── notion/            # Notion 연동 모듈
├── utils/             # 유틸리티 함수
└── config/            # 설정 파일
```

## 사용 방법

1. 크롤러 실행:
```bash
python main.py
```

## 주요 키워드

- 재생에너지
- 전력중개사업
- VPP
- 전력시장
- ESS
- 출력제어
- 중앙계약
- 저탄소 용량
- 전력산업
- 전력정책
- 재생에너지입찰
- 보조서비스
- 예비력시장
- 하향예비력
- 계통포화
- **전력망**
- **기후에너지부**
- **태양광**
- **전력감독원**
- **풍력**
- **해상풍력**
- **전력가격**
- **SMP**

## 🚀 개발 진행 상황

### 2025년 6월 2일 작업 요약

- **코드 구조 및 품질 개선:**
  - **중복 코드 제거:** `NotionClient`의 데이터베이스 검색 로직 중복 제거 및 `KeywordProcessor` 불용어 중복 제거.
  - **미사용 코드 정리:** `PatternDetector`의 미사용 구조 검사 코드 정리.
  - **기능 통합:** 문서 검증 및 관리 로직을 `DocumentManager` 유틸리티 클래스로 통합.
  - **디버그 파일 정리:** 오래된 디버그 파일을 정리하는 유틸리티 스크립트 추가.
- **Notion 연동 오류 수정:** `NotionClient`에서 데이터베이스 접근 시 발생했던 `'NotionClient' object has no attribute 'databases'` 오류를 수정했습니다. `get_weekly_database_id` 메서드에 `parent_page_id` 인자를 추가하여 해결했습니다.
- **크롤러 문제 개선:**
    - 기사 목록에서 제목/날짜 정보를 제대로 가져오지 못해 `Skipping item with missing title or date` 메시지가 반복되는 문제를 해결했습니다. 전기신문 웹사이트의 HTML 구조를 분석하여 `electimes_crawler.py` 파일의 CSS 선택자(`h4.titles a.linked`, `em.replace-date`)를 수정했습니다.
    - 크롤러가 불필요하게 오래된 페이지까지 탐색하여 성능이 저하되는 문제를 개선했습니다. `ElectimesCrawler.get_news_list` 메서드에 3일 이내 기사 출현 여부를 기준으로 페이지 탐색을 조기 중단하는 로직을 추가했습니다 (연속 3페이지 동안 최근 기사 없으면 중단).
    - 기사 목록 단계에서 이루어지던 3일 이내 및 키워드 필터링 로직을 `main.py`로 옮겨, 각 기사의 상세 내용(본문)을 가져온 후 본문 내용을 기반으로 필터링 및 AI 추천 판단을 수행하도록 변경했습니다.
- **메인 스크립트 로직 개선:** `main.py`에서 기사 목록만 가져오던 것을 수정하여, 각 기사의 상세 내용을 추가로 크롤링하고 이를 기사 데이터에 병합한 후 Notion에 동기화하도록 변경했습니다. 이로써 Notion에 본문 내용이 함께 저장됩니다.
- **디버깅 효율성 향상:** `ElectimesCrawler.get_news_list`의 최대 페이지 탐색 수를 디버깅을 위해 일시적으로 줄였습니다.
- **요약 및 핵심 내용 생성 방식 개선:**
  - 규칙 기반 요약/핵심 내용 생성 기능 추가 및 기본값으로 설정.
  - LLM 기반 방식은 선택적으로 사용 가능하도록 유지.
  - 관련 함수에 `use_llm` 인자 추가 및 사용 로직 반영.
- **AI 추천 시스템 유지:** 사용자 피드백 기반 AI 패턴 분석 및 추천 기능 계속 작동.
- **크롤링 기준 확인:** 최근 3일 이내, 키워드 포함 기사만 크롤링하며, Notion 중복 체크는 동기화 단계에서 처리됨을 명확히 함.

현재까지의 작업으로 Notion 연동 및 기본적인 크롤링 파이프라인은 개선되었습니다. 요약/핵심 내용 생성 방식에 규칙 기반을 도입하여 안정성을 높였습니다.

[TODO] AI 추천 로직 상세 내용 기반 개선
[TODO] Notion 동기화 시 중복 처리 로직 강화 (현재 URL 기준이나 추가 검증 필요)
[TODO] 다른 웹사이트 크롤러 추가 구현 (예: KPXCrawler 활성화)
[TODO] 로깅 및 에러 핸들링 강화
[TODO] 키워드 분석 시스템 개선: 
  - 데이터베이스가 쌓일 때까지 사용자 제시 키워드 중심으로 분석
  - AI 패턴 학습 지속
  - 무의미한 키워드와 일반적인 키워드 필터링 로직 추가
[TODO] 문서 자동 업데이트 시스템 구현:
  - README.md, DEVELOPMENT_CONTEXT.md, CODE_DESCRIPTION.md 주기적 업데이트
  - 작업 시작/완료 시 자동 문서화
  - 새로운 컨벤션이나 패턴 발견 시 문서화
[TODO] **임시 스크립트 (`update_empty_fields.py`) 제거:** 23주차 기사 전체 업데이트 임시 코드 (2024년 6월 30일 제거 예정)

## 🔒 보안 설정

### 환경변수 설정
1. `.env.example` 파일을 복사하여 `.env` 파일을 생성하세요:
   ```bash
   cp .env.example .env
   ```

2. `.env` 파일을 열어 실제 API 키로 교체하세요:
   - `NOTION_API_KEY`: Notion 통합 API 키
   - `OPENAI_API_KEY`: OpenAI API 키
   - `GITHUB_TOKEN`: GitHub Personal Access Token
   - 기타 필요한 키들

### ⚠️ 중요한 보안 주의사항
- **절대로 `.env` 파일을 Git에 커밋하지 마세요!**
- API 키가 노출된 경우 즉시 재발급하세요
- `.gitignore`에 `.env`가 포함되어 있는지 확인하세요
- 공개 저장소에서는 실제 API 키를 사용하지 마세요
