import re

# 파일을 읽어옵니다
with open('card_news_app.py.bak', 'r', encoding='utf-8') as f:
    content = f.read()

# 문제가 되는 부분을 찾아서 수정합니다
# 302-305번 줄의 {title}, {keywords_str}, {content}를 실제 변수로 치환
content = content.replace(
    """기사 제목: {title}
키워드: {keywords_str}
기사 내용:
{content}"""\"\"\"""",
    """기사 제목: {article["title"]}
키워드: {", ".join(article.get("keywords", []))}
기사 내용:
{article.get("content", "")}"""

# emphasis_prompt 추가
{emphasis_prompt}\"\"\""""
)

# 파일을 다시 씁니다
with open('card_news_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("수정 완료!")
