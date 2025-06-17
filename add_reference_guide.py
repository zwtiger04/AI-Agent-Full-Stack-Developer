import re

# 파일 읽기
with open('INTEGRATED_PROJECT_GUIDE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 추가할 내용
reference_guide = '''
### 6. 통합 작업 참조 체계 [STD-REFERENCE-001]

#### 새 대화 시작 시 필수 확인
1. **CARD_NEWS_INTEGRATION_TASK_LIST.md** - 현재 진행 상황
   - 어느 Phase까지 완료되었는지 확인
   - 다음 작업이 무엇인지 확인
   - 미해결 이슈가 있는지 확인

2. **INTEGRATED_PROJECT_GUIDE.md [STANDARDS-001]** - 코딩 표준
   - 메서드명 규칙 확인
   - Import 표준 확인
   - 파일 경로 상수 확인
   - 금지 사항 확인

3. **작업 중인 파일의 최신 상태**
   - `card_news_app.py` 현재 상태
   - 최근 변경 사항 확인
   - 오류나 경고 확인

#### 작업 전 체크리스트
- [ ] 메서드명이 표준과 일치하는가?
- [ ] Import 구조가 표준을 따르는가?
- [ ] 파일 경로 상수를 사용하는가?
- [ ] 새 메서드를 추가하지 않았는가?
- [ ] 이전 대화의 미완료 작업이 있는가?

#### 작업 컨텍스트 전달 템플릿
```markdown
# 카드뉴스 통합 작업 계속

## 참조 문서
- INTEGRATED_PROJECT_GUIDE.md [STANDARDS-001]
- CARD_NEWS_INTEGRATION_TASK_LIST.md

## 현재 상황
- 작업 파일: card_news_app.py
- 완료: Phase [X]
- 진행 중: Phase [Y]
- 미해결 이슈: [있으면 기재]

## 다음 작업
[구체적인 작업 내용]
```
'''

# 통합 체크리스트 뒤에 추가 (STD-INTEGRATION-001 뒤)
integration_pattern = r'(### 4\. 통합 시 체크리스트.*?\n\n)'
match = re.search(integration_pattern, content, re.DOTALL)

if match:
    # 체크리스트 섹션 끝 위치 찾기
    end_pos = match.end()
    
    # 새 섹션 삽입
    content = content[:end_pos] + reference_guide + '\n' + content[end_pos:]
    
    # 파일 저장
    with open('INTEGRATED_PROJECT_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 통합 작업 참조 체계가 추가되었습니다!")
else:
    print("❌ 삽입 위치를 찾을 수 없습니다.")
