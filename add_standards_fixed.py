import re

# 표준 섹션 추가
standards_content = '''
## 📏 코딩 표준 및 관리 지침

### [STANDARDS-002] 메서드 및 변수 명명 규칙
1. **메서드명 표준화** (통합 완료)
   - `get_daily_cost()` - 일일 비용 조회
   - `get_monthly_cost()` - 월간 비용 조회
   - `can_generate()` - 생성 가능 여부 확인
   - `get_color_theme()` - 색상 테마 가져오기
   - `load_interested_articles()` - 관심 기사 로드 (전역 함수)
   - `mark_as_processed()` - 처리 완료 표시

2. **파일 경로 상수** (중앙화 완료)
   ```python
   # card_news_paths.py 사용
   from card_news_paths import get_paths, get_path, get_path_str
   
   # 하드코딩 금지 ❌
   path = "/home/zwtiger/..."  # 절대 사용 금지
   
   # 올바른 사용 ✅
   path = get_path_str('output_html')
   ```

3. **테스트 모드 구분**
   ```python
   # 파일명
   filename = f"{'TEST_' if test_mode else ''}detail_{title}_{date}.html"
   
   # 경로
   output_dir = Path(get_path_str('output_test' if test_mode else 'output_html'))
   
   # 데이터 저장
   if not test_mode:
       save_selection_analytics()
       add_to_summary()
       mark_as_processed()
   ```

### [STANDARDS-003] 버튼 동작 명확화
- **💾 저장**: 처리 완료 표시 + 목록에서 제거 (파일은 이미 자동 저장됨)
- **📥 다운로드**: 사용자 PC로 다운로드만
- **🗑️ 삭제**: 테스트 파일만 삭제 (실제 파일은 보호)

---
'''

# 파일 읽기
with open('INTEGRATED_PROJECT_GUIDE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 적절한 위치 찾기 - 키워드 목록 다음에 추가
pattern = r'(### 🚀 향후 개발 계획)'
replacement = standards_content + '\n' + r'\1'
new_content = re.sub(pattern, replacement, content)

# 파일 저장
with open('INTEGRATED_PROJECT_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ 코딩 표준 추가 완료!")
