# 작업 리스트 파일 업데이트
with open('CARD_NEWS_INTEGRATION_TASK_LIST.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Phase 2 완료 표시
updates = [
    ('- [ ] Phase 2: 메서드명 표준화', '- [x] Phase 2: 메서드명 표준화 ✅'),
    ('- [ ] 2.1 CostManager 클래스', '- [x] 2.1 CostManager 클래스'),
    ('- [ ] `get_today_cost()` → `get_daily_cost()`', '- [x] `get_today_cost()` → `get_daily_cost()`'),
    ('- [ ] `get_month_cost()` → `get_monthly_cost()`', '- [x] `get_month_cost()` → `get_monthly_cost()`'),
    ('- [ ] `check_limits()` → `can_generate()`', '- [x] `check_limits()` → `can_generate()`'),
    ('- [ ] 2.2 CardNewsGenerator 클래스', '- [x] 2.2 CardNewsGenerator 클래스'),
    ('- [ ] `get_color_scheme()` → `get_color_theme()`', '- [x] `get_color_scheme()` → `get_color_theme()`'),
    ('- [ ] API 초기화 방식 변경', '- [x] API 초기화 방식 변경'),
]

for old, new in updates:
    content = content.replace(old, new)

# 현재 상태 업데이트
content = content.replace('## 🔄 현재 상태 (2025-06-15 21:20)', '## 🔄 현재 상태 (2025-06-15 21:35)')
content = content.replace('**현재: Phase 1 완료, Phase 2 준비**', '**현재: Phase 2 완료, Phase 3 준비**')
content = content.replace('**다음: Phase 2.1 - CostManager 메서드명 표준화**', '**다음: Phase 3.1 - 기사 로드 방식 변경**')

# 추가 메모
additional_notes = '''
### Phase 2 완료 내역
- ✅ 모든 메서드명 표준화 완료
- ✅ limits 딕셔너리 사용 코드 모두 수정
- ✅ can_generate 반환값 변경 (tuple[bool, str])
- ✅ determine_color_theme → get_color_theme 변경
- ✅ 미사용 get_color_scheme 메서드 제거
'''

# 작업 리스트 앞에 추가
content = content.replace('### Phase 3: 기능 통합', additional_notes + '\n### Phase 3: 기능 통합')

with open('CARD_NEWS_INTEGRATION_TASK_LIST.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Phase 2 완료 - 작업 리스트 업데이트!")
