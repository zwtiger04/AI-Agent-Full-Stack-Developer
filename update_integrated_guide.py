# INTEGRATED_PROJECT_GUIDE.md 업데이트 내용 추가
content_to_add = '''
## 🔄 최근 업데이트 (2025-06-16)

### ✅ 테스트 모드 완전 분리
- **파일 경로 분리**: 테스트 파일은 `output/card_news/test/`에 저장
- **파일명 구분**: 테스트 파일은 `TEST_` 접두사 추가
- **데이터 격리**: 테스트 데이터는 실제 통계/분석에서 제외
- **비용 표시 개선**: 테스트 모드 전용 안내 메시지

---

## 🧪 테스트 모드 시스템

### 개요
테스트 모드는 실제 API 호출 없이 카드뉴스 생성 프로세스를 테스트할 수 있는 기능입니다.

### 주요 특징
1. **완전한 데이터 분리**
   - 테스트 파일 전용 디렉토리: `output/card_news/test/`
   - 파일명 패턴: `TEST_detail_{제목}_{날짜}.html`
   - 분석 통계에서 제외
   - 요약 페이지 추가 차단

2. **비용 없음**
   - Claude API 호출하지 않음
   - 미리 정의된 HTML 템플릿 사용
   - 5가지 테마: modern, minimal, bold, eco, tech

3. **테스트 파일 관리**
   - 위치: "💰 비용 관리" 탭 → "🧪 테스트 파일 관리" 섹션
   - 일괄 삭제 기능
   - 7일 이상 된 파일 자동 정리

### 동작 플로우
```mermaid
graph LR
    A[테스트 모드 체크] --> B{test_mode?}
    B -->|Yes| C[TestModeGenerator]
    B -->|No| D[CardNewsGenerator]
    C --> E[TEST_ 파일 생성]
    D --> F[일반 파일 생성]
    E --> G[test/ 폴더 저장]
    F --> H[html/ 폴더 저장]
    G --> I[통계 제외]
    H --> J[통계 포함]
```

---
'''

# 파일 읽기
with open('INTEGRATED_PROJECT_GUIDE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# "## 📁 프로젝트 구조" 섹션 찾아서 그 앞에 추가
import re
pattern = r'(## 📁 프로젝트 구조)'
replacement = content_to_add + '\n' + r'\1'
new_content = re.sub(pattern, replacement, content)

# 파일 저장
with open('INTEGRATED_PROJECT_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ INTEGRATED_PROJECT_GUIDE.md 업데이트 완료!")
