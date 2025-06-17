# 🚨 카드뉴스 시스템 긴급 수정 작업

## 📋 이전 작업 요약
- 작업일: 2025-06-16
- 완료 사항: Phase 1-4 모든 통합 및 테스트 완료
- 주요 문서: INTEGRATED_PROJECT_GUIDE.md (통합 가이드)

## 🔍 해결해야 할 문제

### 문제 1: 스타일/구성항목 수동 설정 기능 누락
**증상**: 
- 기존에 있던 섹션 선택 UI의 수동 설정 옵션이 사라짐
- 사용자가 원하는 섹션을 직접 선택할 수 없음

**예상 원인**:
- card_news_app_integrated.py의 기능이 card_news_app.py로 제대로 이관되지 않음
- 통합 과정에서 UI 컴포넌트 누락

### 문제 2: 노션 관심 기사 로드 실패
**증상**:
- 노션 데이터베이스의 '관심' 체크된 기사가 불러와지지 않음
- pending_cardnews.json에 테스트 데이터만 있음

**예상 원인**:
- 노션 API 연동 코드 미작동
- 관심 기사 필터링 로직 문제

## 🎯 작업 지시사항

### 1단계: 원인 분석
```bash
# 1. 수동 설정 기능 확인
grep -n "수동\|manual\|custom" card_news_app.py
grep -n "수동\|manual\|custom" card_news_app_integrated.py

# 2. 섹션 선택 UI 비교
grep -B5 -A5 "섹션 선택\|선택된 섹션" card_news_app.py
grep -B5 -A5 "섹션 선택\|선택된 섹션" card_news_app_integrated.py

# 3. 노션 연동 코드 확인
grep -n "notion\|load_interested\|watch_interested" *.py
find . -name "*notion*.py" -o -name "*interested*.py" | grep -v __pycache__
```

### 2단계: 계획 수립
1. 두 파일의 차이점 분석 (diff 도구 활용)
2. 누락된 기능 목록 작성
3. 우선순위 결정 (수동 설정 > 노션 연동)

### 3단계: 구현
- 백업 우선: `cp card_news_app.py card_news_app.py.bak_20250616`
- 단계별 수정 및 테스트

## 📌 주의사항
1. **기존 기능 보존**: 현재 작동하는 기능은 절대 손상시키지 않음
2. **점진적 수정**: 한 번에 하나씩 수정하고 테스트
3. **문서화**: 모든 변경사항은 INTEGRATED_PROJECT_GUIDE.md에 기록

## 🔗 참고 파일
- 메인 파일: `/home/zwtiger/AI-Agent-Full-Stack-Developer/card_news_app.py`
- 참조 파일: `/home/zwtiger/AI-Agent-Full-Stack-Developer/card_news_app_integrated.py`
- 가이드: `/home/zwtiger/AI-Agent-Full-Stack-Developer/INTEGRATED_PROJECT_GUIDE.md`

## 💡 시작 메시지
"NEXT_WORK_PROMPT_20250616.md 파일을 참고하여 카드뉴스 시스템의 두 가지 문제를 해결하겠습니다. 먼저 원인 분석부터 시작하겠습니다."

---
*이 프롬프트를 사용하여 다음 세션에서 작업을 이어가세요.*
