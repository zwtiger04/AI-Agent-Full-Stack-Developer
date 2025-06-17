import re
from datetime import datetime

# 파일 읽기
with open('CARD_NEWS_INTEGRATION_TASK_LIST.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Phase 4 완료로 업데이트
content = re.sub(
    r'\[ \] Phase 4: 테스트 및 검증',
    '[x] Phase 4: 테스트 및 검증 ✅',
    content
)

# Phase 4 세부사항 모두 체크
content = re.sub(
    r'- \[ \] 4\.1 기능 테스트',
    '- [x] 4.1 기능 테스트',
    content
)
content = re.sub(
    r'- \[ \] 4\.2 UI 테스트',
    '- [x] 4.2 UI 테스트',
    content
)
content = re.sub(
    r'- \[ \] 4\.3 파일 I/O 테스트',
    '- [x] 4.3 파일 I/O 테스트',
    content
)

# 새로운 섹션 추가 - Phase 5
new_section = '''

### Phase 5: 테스트 모드 완전 분리 ✅ (2025-06-16 추가)
- [x] 5.1 파일 경로 분리
  - [x] `output/card_news/test/` 디렉토리 추가
  - [x] 테스트 파일 전용 경로 관리
- [x] 5.2 파일명 구분
  - [x] `TEST_` 접두사 추가
  - [x] 테스트/실제 파일 명확히 구분
- [x] 5.3 데이터 격리
  - [x] 분석 통계 저장 차단
  - [x] 요약 페이지 추가 차단
  - [x] 처리 완료 표시 차단
- [x] 5.4 UI 개선
  - [x] 테스트 모드 비용 표시 변경
  - [x] 테스트 파일 관리 섹션 추가
  - [x] 일괄 삭제 기능 구현

## 📊 전체 진행률: 100% 완료! 🎉

## 🔄 다음 단계
**현재: 모든 통합 작업 완료**
**상태: 프로덕션 준비 완료**'''

# "## 🔄 다음 단계" 부분 교체
pattern = r'## 🔄 다음 단계.*$'
content = re.sub(pattern, new_section, content, flags=re.DOTALL)

# 파일 저장
with open('CARD_NEWS_INTEGRATION_TASK_LIST.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ CARD_NEWS_INTEGRATION_TASK_LIST.md 업데이트 완료!")
