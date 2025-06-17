# 📋 카드뉴스 시스템 변경 로그

## [2025-06-16] - Phase 5 완료

### 추가됨
- 수동 섹션 선택 기능 (라디오 버튼 + multiselect UI)
- 테마 선택 기능 (5가지 테마)
- load_interested_articles() 전역 함수
- CARDNEWS_SYSTEM_UPDATE_20250616.md 문서

### 변경됨
- "기사 목록 새로고침" 버튼 기능 강화 (노션 연동)
- 파일 경로 통일 (PENDING_CARDNEWS_FILE 상수 사용)
- watch_interested_articles.py 파일 경로 수정

### 수정됨
- pending_cardnews.json 파일 위치 불일치 문제
- 통계 표시 오류 (2개 → 34개)
- InterestMonitor import 누락 문제

### 문서
- CARDNEWS_WORK_STATUS_20250616.md 생성
- INTEGRATED_PROJECT_GUIDE.md Phase 5 추가
- CARD_NEWS_INTEGRATION_TASK_LIST.md 완료 상태 업데이트
- README.md 최근 업데이트 섹션 추가

---

## [2025-06-15] - Phase 1-4 완료

### 추가됨
- 타입 시스템 (card_news/types.py)
- 검증 시스템 (card_news/validators.py)
- 데코레이터 시스템 (card_news/decorators.py)
- 테스트 모드 기능
- 파일 경로 표준화 시스템

### 수정됨
- TypeError: unhashable type 오류 해결
- 메서드명 표준화
- Import 구조 정리

### 변경됨
- 파일 경로 구조 전면 개편
- 하드코딩된 경로 제거

---

## [2025-06-10] - 초기 시스템 구축

### 추가됨
- 전기신문 크롤러
- 노션 데이터베이스 연동
- AI 추천 시스템
- Streamlit 기반 카드뉴스 생성 UI
- Claude API 연동

### 기능
- 주차별 자동 데이터베이스 생성
- 키워드 기반 필터링
- AI 요약 생성
- HTML 카드뉴스 생성

---
*이 로그는 주요 변경사항만 기록합니다. 세부 사항은 각 날짜별 WORK_STATUS 문서를 참조하세요.*
