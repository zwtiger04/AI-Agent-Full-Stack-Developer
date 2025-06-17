def render_summary_tab():
    """요약 카드뉴스 탭 - 원본과 100% 동일한 스타일"""
    import streamlit.components.v1 as components
    from pathlib import Path
    from datetime import datetime
    from collections import Counter
    
    # 원본 CSS 파일 읽기
    css_path = Path('output/card_news/templates/original_summary_style.css')
    if css_path.exists():
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
    else:
        st.error("CSS 파일을 찾을 수 없습니다.")
        return
    
    # 카드뉴스 데이터 로드
    card_news_list = load_generated_card_news()
    
    # 카테고리별 집계
    category_counts = Counter([card['category_name'] for card in card_news_list])
    top_categories = category_counts.most_common(4)
    
    # HTML 생성 - 원본과 동일한 구조
    today = datetime.now().strftime("%Y년 %m월 %d일")
    
    html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>전력산업 카드뉴스 - {today}</title>
    <style>{css_content}</style>
</head>
<body>
    <div class="container">
        <!-- 헤더 섹션 -->
        <div class="header">
            <h1>전력산업 주요 뉴스</h1>
            <p class="subtitle">{today} | 에너지 전환의 현장을 전합니다</p>
        </div>

        <!-- 통계 섹션 -->
        <div class="stats-section">
            <h2 class="stats-title">오늘의 주요 지표</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{len(card_news_list)}</div>
                    <div class="stat-label">전체 기사</div>
                </div>
"""
    
    # 상위 카테고리 3개 추가
    for category, count in top_categories[:3]:
        html_content += f"""
                <div class="stat-item">
                    <div class="stat-number">{count}</div>
                    <div class="stat-label">{category} 관련</div>
                </div>
"""
    
    html_content += """
            </div>
        </div>

        <!-- 뉴스 그리드 -->
        <div class="news-grid">
"""
    
    # 카드 추가 - 원본과 동일한 구조
    for i, card in enumerate(card_news_list):
        # 파일 경로 수정 (상대 경로로)
        file_path = card["file_path"].replace('output/card_news/html/', '')
        
        card_html = f'''
            <!-- 기사 {i+1}: {card["title"][:20]} -->
            <div class="news-card" onclick="window.location.href='{file_path}'">
            <span class="card-category category-{card["category"]}">{card["category_name"]}</span>
            <h3 class="card-title">{card["title"]}</h3>
            <p class="card-summary">
            {card["summary"]}
            </p>
            <div class="card-meta">
            <span>{card["source"]}</span>
            <a href="#" class="read-more">자세히 보기 →</a>
            </div>
            </div>
'''
        html_content += card_html
    
    html_content += """
        </div>
    
            </div>
        </div>
</body>
</html>
"""
    
    # 컴포넌트로 렌더링 - 높이 증가
    components.html(html_content, height=1600, scrolling=True)
