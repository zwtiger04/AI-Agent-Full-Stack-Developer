# 파일 읽기
with open('card_news_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# check_limits 메서드 찾아서 제거
new_lines = []
skip_lines = False
for i, line in enumerate(lines):
    if 'def check_limits(' in line:
        skip_lines = True
        continue
    elif skip_lines and 'class CardNewsGenerator:' in line:
        skip_lines = False
    
    if not skip_lines:
        new_lines.append(line)

# can_generate 메서드가 있는지 확인
has_can_generate = any('def can_generate(' in line for line in new_lines)
if not has_can_generate:
    print("❌ can_generate 메서드가 없습니다!")
else:
    # 파일 저장
    with open('card_news_app.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("✅ check_limits 메서드 제거 완료!")

