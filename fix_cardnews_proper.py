# 백업 파일을 원본으로 복원
import shutil
shutil.copy('card_news_app.py.bak', 'card_news_app.py')

# 파일 읽기
with open('card_news_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 302-305번 줄(0-based index로는 301-304) 수정
# Python 코드에서 문제가 있는 부분 찾아서 수정
for i in range(len(lines)):
    if i == 301 and lines[i].strip() == '기사 제목: {title}':
        lines[i] = '기사 제목: {article["title"]}\n'
    elif i == 302 and lines[i].strip() == '키워드: {keywords_str}':
        lines[i] = '키워드: {", ".join(article.get("keywords", []))}\n'
    elif i == 303 and lines[i].strip() == '기사 내용:':
        pass  # 그대로 둠
    elif i == 304 and lines[i].strip() == '{content}"""':
        lines[i] = '{article.get("content", "")}' + '\n'
        # emphasis_prompt 추가
        lines[i] += '{emphasis_prompt}"""\n'

# 파일 다시 쓰기
with open('card_news_app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
    
print("수정 완료!")
