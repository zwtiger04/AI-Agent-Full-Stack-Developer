# CODE_DESCRIPTION.md

## 최근 업데이트 (2025-06-02)

### 전력산업 뉴스 크롤링 및 분석 작업 실패
- **파일:** main.py
- **변경 내용:**
  - 오류 처리 로직 추가 필요
- **영향:** 작업 중단 및 재시도 필요

## 최근 업데이트 (2025-06-02)

### Notion 동기화 결과
- **파일:** notion_client.py
- **변경 내용:**
  - 동기화 로직 개선
  - 에러 처리 강화
- **영향:** 데이터 동기화 안정성 향상

## 최근 업데이트 (2025-06-02)

### 전력산업 뉴스 크롤링 결과
- **파일:** electimes_crawler.py
- **변경 내용:**
  - 크롤링 로직 개선
  - 필터링 로직 강화
- **영향:** 관련 뉴스 수집 정확도 향상

## 최근 업데이트 (2025-06-02)

### 전력산업 뉴스 크롤링 및 분석 작업 시작
- **파일:** main.py, electimes_crawler.py, article_recommender.py, notion_client.py
- **변경 내용:**
  - 디버그 파일 자동 정리 기능 추가
  - 문서 관리 시스템 통합
  - 패턴 감지 및 문서화 기능 추가
- **영향:** 코드 품질 향상 및 문서 일관성 유지

## 최근 업데이트 (2025-06-02)

### 전력산업 뉴스 크롤링 및 분석 작업 실패
- **파일:** main.py
- **변경 내용:**
  - 오류 처리 로직 추가 필요
- **영향:** 작업 중단 및 재시도 필요

## 최근 업데이트 (2025-06-02)

### Notion 동기화 결과
- **파일:** notion_client.py
- **변경 내용:**
  - 동기화 로직 개선
  - 에러 처리 강화
- **영향:** 데이터 동기화 안정성 향상

## 최근 업데이트 (2025-06-02)

### 전력산업 뉴스 크롤링 결과
- **파일:** electimes_crawler.py
- **변경 내용:**
  - 크롤링 로직 개선
  - 필터링 로직 강화
- **영향:** 관련 뉴스 수집 정확도 향상

## 최근 업데이트 (2025-06-02)

### 전력산업 뉴스 크롤링 및 분석 작업 시작
- **파일:** main.py, electimes_crawler.py, article_recommender.py, notion_client.py
- **변경 내용:**
  - 디버그 파일 자동 정리 기능 추가
  - 문서 관리 시스템 통합
  - 패턴 감지 및 문서화 기능 추가
- **영향:** 코드 품질 향상 및 문서 일관성 유지

## 최근 업데이트 (2025-06-02)

### Ollama API 응답 파싱 로직 수정
- **파일:** `ai_update_content.py`
- **변경 내용:** Ollama API 응답에서 생성된 텍스트를 추출하는 로직 수정
- **이전 코드:**
  ```python
  summary = result.get('message', {}).get('content', '').strip()
  ```
- **수정된 코드:**
  ```python
  summary = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
  ```
- **변경 이유:** Ollama API 응답 구조(`result['choices'][0]['message']['content']`)와 일치하도록 수정
- **영향:** 요약과 핵심 내용이 Notion에 정확히 반영됨

### 요약 및 핵심 내용 생성 방식 개선 및 Ollama 응답 파싱 로직 수정
- **파일:** `ai_update_content.py`, `update_empty_fields.py`, `notion_client.py`
- **변경 내용:**
  - 기존 LLM 기반 방식과 함께 규칙 기반 요약/핵심 내용 생성 함수 추가 (`ai_update_content.py`).
  - LLM 함수에 `use_llm` 인자를 추가하여 규칙 기반 함수 호출 기능 구현 (`ai_update_content.py`).
  - `update_empty_fields.py` 스크립트와 `notion_client.py`의 메인 동기화 로직에서 규칙 기반 함수를 기본으로 사용하도록 변경 (`use_llm=False` 적용).
  - Ollama API 응답에서 생성된 텍스트를 추출하는 로직 수정 (`ai_update_content.py`).
  - `googletrans` 대신 `googletrans-py`를 사용하여 LLM이 생성한 **영어** 요약/핵심 내용을 **한국어**로 번역하는 로직 추가 (`ai_update_content.py`).
- **영향:**
  - 요약 및 핵심 내용 생성 품질 및 안정성 향상 (기본값: 규칙 기반).
  - Notion에 요약과 핵심 내용이 정확히 반영됨.
  - LLM 기반 방식은 `googletrans-py`를 통한 번역을 사용하여 코드 유지 및 필요 시 전환 가능.

### 키워드 분석 시스템
- **현재 상태:** 
  - 단순 빈도수 기반 키워드 추출
  - 무의미한 키워드와 일반적인 키워드가 많이 포함됨
- **개선 계획:**
  1. 데이터베이스가 쌓일 때까지 사용자 제시 키워드 중심으로 분석
  2. AI 패턴 학습 지속
  3. 무의미한 키워드와 일반적인 키워드 필터링 로직 추가

### 문서 자동 업데이트 시스템
- **계획:**
  1. 작업 시작/완료 시 자동 문서화
  2. 새로운 컨벤션이나 패턴 발견 시 자동 문서화
  3. 문서 간 일관성 유지를 위한 검증 로직 추가

### 코드 중복 및 미사용 코드 개선
- **변경 내용:**
  - `notion/notion_client.py`: 데이터베이스 검색 로직 중복 제거 (`_search_database` 메서드 추가) 및 데이터베이스 생성 로직 분리 (`_create_weekly_database` 메서드 추가).
  - `processors/keyword_processor.py`: `_get_stop_words` 메서드에서 중복된 불용어 제거 및 목록 정리.
  - `utils/document_manager.py` 생성 및 문서 검증/관리 로직 통합 (기존 `document_validator.py`, `document_updater.py` 대체/개선).
  - `utils/debug_cleanup.py` 스크립트 생성.
  - `pattern_detector.py`: 미사용 구조 검사 관련 코드 (메서드 및 호출 부분) 주석 처리/제거.
- **영향:** 코드베이스의 중복 감소, 각 모듈의 응집도 향상, 유지보수 용이성 증가.

## 코드 구조

### 크롤링 모듈 (`crawlers/`)
- `electimes_crawler.py`: 전기신문 기사 크롤링
- `kpx_crawler.py`: 한국전력거래소 공지사항 크롤링 (향후 구현)

### Notion 연동 모듈 (`notion/`)
- `notion_client.py`: Notion API 연동 및 데이터베이스 관리
- `ai_update_content.py`: AI 기반 기사 내용 업데이트

### 유틸리티 모듈 (`utils/`)
- `date_utils.py`: 날짜 관련 유틸리티 함수
- `text_utils.py`: 텍스트 처리 유틸리티 함수
- `debug_cleanup.py`: 디버그 파일 정리 스크립트
- `document_manager.py`: 문서 검증 및 관리 유틸리티

### 설정 모듈 (`config/`)
- `config.py`: 환경 변수 및 설정 관리

## 주요 기능 설명

### 1. 기사 크롤링
- 최근 3일 이내 기사만 수집
- 키워드 기반 필터링
- 본문 내용 추출 및 정제

### 2. Notion 동기화
- 주차별 데이터베이스 자동 생성
- 기사 정보 동기화 (제목, 출처, 날짜, 키워드, 한줄요약, 핵심 내용)
- 중복 기사 처리

### 3. AI 기반 내용 생성
- Ollama API를 사용한 한줄요약 생성
- Ollama API를 사용한 핵심 내용 추출
- 실패 시 폴백 메커니즘

## 향후 개선 사항

### 1. 키워드 분석 시스템
- [ ] 사용자 제시 키워드 중심 분석 구현
- [ ] AI 패턴 학습 로직 구현
- [ ] 키워드 필터링 로직 구현

### 2. 문서 자동 업데이트
- [ ] 작업 시작/완료 시 자동 문서화 구현
- [ ] 새로운 컨벤션이나 패턴 자동 문서화 구현
- [ ] 문서 일관성 검증 로직 구현

### 3. 성능 최적화
- [ ] 비동기 처리 도입
- [ ] 병렬 처리 도입
- [ ] 캐싱 전략 구현

### 임시 스크립트 (`update_empty_fields.py`)
- **파일:** `update_empty_fields.py`
- **변경 내용:** 23주차 기사의 요약과 핵심 내용을 강제로 업데이트하기 위한 임시 코드. 이제 규칙 기반으로 작동.
- **영향:** 특정 주차 기사 내용 일괄 업데이트 가능.
- **제거 예정일:** 2024년 6월 30일 