import sys

# 파일 읽기
with open('card_news_app_integrated.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# main 함수 시작 부분 찾기
main_func_line = -1
for i, line in enumerate(lines):
    if line.strip() == 'def main():':
        main_func_line = i
        break

if main_func_line == -1:
    print("❌ main 함수를 찾을 수 없습니다.")
    sys.exit(1)

# main 함수 첫 줄에 load_dotenv() 추가
insert_line = main_func_line + 1
# 들여쓰기 맞추기
lines.insert(insert_line, '    # .env 파일 로드\n')
lines.insert(insert_line + 1, '    load_dotenv()\n')
lines.insert(insert_line + 2, '    \n')

# 파일 저장
with open('card_news_app_integrated.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ load_dotenv() 호출이 추가되었습니다!")
