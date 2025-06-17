# 전력산업 카드뉴스 섹션 유연화 시스템 구현

## 작업 환경
- WSL Ubuntu 환경
- 작업 폴더: /home/zwtiger/AI-Agent-Full-Stack-Developer
- 주요 파일: card_news_app.py
- Python 환경: venv 활성화 필요

## 현재 상황 (2025.06.11)
### 완료된 작업
1. 요약 페이지 그리드 레이아웃 수정 ✅
2. 전문가 의견/시사점 섹션 분리 ✅
3. 색상 시스템 정비 ✅

### 이번 작업 목표
카드뉴스의 2-4번 섹션을 기사 내용에 따라 동적으로 선택하는 시스템 구현

## 구현 작업 목록

### 1. 디렉토리 구조 생성
```bash
card_news/
├── __init__.py
├── section_config.py
├── section_selector.py
├── section_analytics.py
└── section_styles.css
```

### 2. section_config.py 구현
- 필수 섹션 (1, 5번) 정의
- 선택 가능한 10개 섹션 정의
- 각 섹션별 트리거 단어 설정
- 섹션별 min/max 아이템 수 설정

### 3. section_selector.py 구현
- SectionSelector 클래스
- analyze_article() 메서드: 기사 분석
- recommend_sections() 메서드: 상위 3개 선택
- 트리거 단어 기반 점수 계산 로직

### 4. section_styles.css 작성
- 10개 섹션별 CSS 스타일
- 반응형 디자인 고려
- 다크 테마 기준
- 호버 효과 및 애니메이션

### 5. card_news_app.py 수정
- section_selector 임포트
- generate_card_news() 메서드 수정
- 동적 프롬프트 생성 로직 추가
- 선택된 섹션만 포함하도록 수정

### 6. section_analytics.py 구현
- 섹션 사용 추적
- JSON 파일로 데이터 저장
- 주간 패턴 분석 함수
- 리포트 생성 기능

### 7. 테스트 케이스 작성
- 각 섹션 타입별 테스트
- 트리거 단어 매칭 테스트
- 프롬프트 생성 검증

## 주의사항
1. **기존 코드 호환성**: 현재 동작하는 기능 유지
2. **에러 처리**: 섹션 선택 실패 시 기본값 사용
3. **로깅**: 모든 선택 과정 기록
4. **성능**: 프롬프트 길이 5000 토큰 이하 유지

## 참조 문서
- README.md (프로젝트 개요)
- INTEGRATED_PROJECT_GUIDE.md (전체 구조)
- 현재까지 수정된 card_news_app.py

## 작업 시작 체크리스트
- [ ] venv 활성화: `source venv/bin/activate`
- [ ] 작업 브랜치 생성: `git checkout -b feature/flexible-sections`
- [ ] 필요 패키지 확인: pandas, matplotlib
- [ ] 백업 생성: `cp card_news_app.py card_news_app_backup_$(date +%Y%m%d).py`

## 예상 결과물
1. 기사 내용에 따라 최적화된 섹션 구성
2. 불필요한 섹션 제거로 가독성 향상
3. 섹션 사용 패턴 데이터 수집
4. 향후 자동 확장 가능한 구조

이제 작업을 시작해주세요!
