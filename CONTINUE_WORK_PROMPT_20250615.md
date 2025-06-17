# 🔧 카드뉴스 생성 시스템 TypeError 근본 해결 작업

## 📌 작업 컨텍스트
전력산업 뉴스 카드뉴스 생성 시스템에서 지속적으로 발생하는 TypeError를 근본적으로 해결하는 작업입니다.

## 🏠 작업 환경
```bash
# 위치: WSL Ubuntu
cd /home/zwtiger/AI-Agent-Full-Stack-Developer
source venv/bin/activate

# 실행 중: Streamlit 앱 (포트 8501)
streamlit run card_news_app_integrated.py
```

## 🚨 현재 문제 상황
### 최신 오류 [ISSUE-004]
```python
TypeError: unhashable type: 'list'
# 위치: card_news_app_integrated.py line 538
# 코드: template = self.templates.get(theme_name, self.templates['modern'])
```

### 근본 원인
- 시스템 전반에 걸친 타입 불일치
- 문자열/튜플/리스트가 혼재되어 딕셔너리 키로 사용
- 중앙화된 타입 검증 시스템 부재

## 📊 작업 현황
### ✅ 완료된 작업
- [TASK-001~004] 기본 수정 완료
- [TASK-005] section_selector.py TypeError 수정 (2025-06-15)
- [TASK-006] analytics_integration.py 타입 정규화 (2025-06-15)

### 🔴 미완료 작업 (근본 해결)
- [TODO-001] 타입 시스템 구축
- [TODO-002] 중앙 검증 시스템
- [TODO-003] 데코레이터 시스템
- [TODO-004] 기존 코드 리팩토링
- [TODO-005] 테스트 및 검증

## 🎯 작업 요청
다음 단계별 작업을 진행해주세요:

### Phase 1: 타입 시스템 구축 [TODO-001]
1. `card_news/types.py` 파일 생성
2. Section 데이터 클래스 구현
3. 타입 별칭 정의 (SectionId, SectionScore 등)

### Phase 2: 중앙 검증 시스템 [TODO-002]
1. `card_news/validators.py` 파일 생성
2. `ensure_string()` - 안전한 문자열 변환
3. `normalize_sections()` - 섹션 데이터 정규화

### Phase 3: 즉시 수정 필요 [ISSUE-004]
1. `card_news_app_integrated.py` line 538 근처 수정
2. theme_name을 안전하게 문자열로 변환
3. 유사한 패턴 모두 수정

## 🔍 참고 문서
- 시스템 구조: `CARDNEWS_SYSTEM_STRUCTURE_20250615.md`
- 작업 현황: `CARDNEWS_WORK_STATUS_20250615.md`
- 수정 기록: `FIX_TYPEERROR_20250615.md`

## ⚡ 빠른 시작 명령어
```bash
# 현재 상태 확인
cd /home/zwtiger/AI-Agent-Full-Stack-Developer
git status
git diff

# 로그 확인
tail -f logs/streamlit_*.log | grep -A 5 -B 5 "TypeError"

# 테스트 실행
python3 test_fix_result.py
```

## 주의사항
- 작업 전 백업 필수
- 타입 변경 시 전체 데이터 플로우 고려
- 테스트 모드로 먼저 검증
