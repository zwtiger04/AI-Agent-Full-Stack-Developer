def render_summary_tab():
    """요약 카드뉴스 탭 - 컴포넌트 방식으로 단순 구현"""
    import streamlit.components.v1 as components
    from pathlib import Path
    from datetime import datetime
    
    # CSS 파일 읽기
    css_path = Path('output/card_news/templates/summary_style.css')
    if css_path.exists():
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
    else:
        st.error("CSS 파일을 찾을 수 없습니다.")
        return
    
    # 카드뉴스 데이터 로드
    card_news_list = load_generated_card_news()
    
    # HTML 생성
    today = datetime.now().strftime("%Y년 %m월 %d일")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>전력산업 카드뉴스</title>
        <style>{css_content}</style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>전력산업 카드뉴스</h1>
                <p class="subtitle">{today} | 총 {len(card_news_list)}개의 카드뉴스</p>
            </div>
            
            <div class="news-grid">
    """
    
    # 카드 추가
    for card in card_news_list:
        card_html = f'''
        <div class="news-card" onclick="window.open('{card["file_path"]}', '_blank')">
            <span class="card-category category-{card["category"]}">{card["category_name"]}</span>
            <h3 class="card-title">{card["title"]}</h3>
            <p class="card-summary">{card["summary"]}</p>
            <div class="card-meta">
                <span>{card["source"]} | {card["date"]}</span>
                <a href="#" class="read-more">자세히 보기 →</a>
            </div>
        </div>
        '''
        html_content += card_html
    
    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    
    # 컴포넌트로 렌더링
    components.html(html_content, height=1200, scrolling=True)
