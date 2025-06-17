# card_news_app.py 파일을 수정하여 명확한 HTML 생성 프롬프트로 변경

with open('card_news_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 프롬프트 부분 찾아서 수정
old_prompt = """당신은 전력 산업 전문 카드뉴스 디자이너입니다. 주어진 기사를 바탕으로 시각적으로 매력적이고 정보가 풍부한 5페이지 카드뉴스를 만들어주세요."""

new_prompt = """당신은 전력 산업 전문 카드뉴스 웹 개발자입니다. 주어진 기사를 바탕으로 완전한 HTML 코드를 생성해주세요.

반드시 실행 가능한 HTML/CSS/JavaScript 코드를 작성하세요. 기획안이나 설명이 아닌 실제 동작하는 웹페이지 코드가 필요합니다."""

content = content.replace(old_prompt, new_prompt)

# 추가로 프롬프트 끝부분도 수정
content = content.replace(
    '{emphasis_prompt}"""',
    '{emphasis_prompt}' + '\n\n반드시 완전한 HTML 코드를 ```html 코드블록 ``` 안에 작성해주세요. 설명이나 기획안이 아닌 실제 코드만 필요합니다."""'
)

with open('card_news_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("프롬프트 수정 완료!")
