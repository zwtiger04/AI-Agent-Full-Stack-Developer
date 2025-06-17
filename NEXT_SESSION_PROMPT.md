# 🔧 카드뉴스 생성 오류 수정 요청 - TypeError 해결

## 현재 상황
- **위치**: WSL Ubuntu - `/home/zwtiger/AI-Agent-Full-Stack-Developer`
- **실행 중**: Streamlit 앱 (포트 8501)
- **오류**: `TypeError: unhashable type: 'list'`
- **발생 시점**: 카드뉴스 생성 버튼 클릭 시

## 오류 상세
```
TypeError: unhashable type: 'list'
```
- emphasis가 리스트 형태로 전달되어 해싱이 필요한 곳에서 오류 발생
- 딕셔너리 키나 set에 리스트를 사용하려 할 때 발생하는 오류

## 작업 요청
1. **오류 위치 파악**
   - Streamlit 로그 확인
   - 정확한 오류 발생 라인 찾기

2. **emphasis 데이터 흐름 추적**
   - 어디서 emphasis가 리스트로 변환되는지
   - 어디서 해싱이 시도되는지

3. **수정 방안**
   - emphasis를 튜플로 변환하거나
   - 해싱이 필요한 부분에서 문자열로 변환

## 관련 파일
- `card_news_app_integrated.py` - 메인 앱
- `card_news/section_analytics.py` - 분석 모듈 (의심)
- `card_news/section_selector.py` - 섹션 선택기

## 이전 작업 내역
- [TASK-001] article['id'] → article['page_id'] 수정 완료
- [TASK-002] emphasis 다양한 형식 처리 추가 완료
- [TASK-003] API 검증 시스템 구축 완료
- [TASK-004] 테스트 모드 추가 완료

## 테스트 방법
1. 먼저 테스트 모드로 확인
2. `./check_before_generate.sh`로 사전 검증
3. 실제 생성 시도

작업 시작 전에 현재 프로세스 상태를 확인하고, 안전하게 진행해주세요.
