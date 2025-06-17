"""
카드뉴스 공통 테마 및 스타일
모든 UI 컴포넌트에서 일관된 스타일 유지
"""

# 색상 팔레트
COLORS = {
    "bg_primary": "#0f0f0f",
    "bg_secondary": "rgba(255, 255, 255, 0.05)",
    "bg_hover": "rgba(255, 255, 255, 0.08)",
    "primary": "#667eea",
    "secondary": "#764ba2",
    "text_primary": "#ffffff",
    "text_secondary": "#cccccc",
    "text_muted": "#888888",
    "border": "rgba(255, 255, 255, 0.1)"
}

# 카테고리 색상
CATEGORY_COLORS = {
    "ESS": {"bg": "rgba(255, 107, 107, 0.8)", "text": "#FF6B6B"},
    "VPP": {"bg": "rgba(78, 205, 196, 0.8)", "text": "#4ECDC4"},
    "재생에너지": {"bg": "rgba(69, 183, 209, 0.8)", "text": "#45B7D1"},
    "태양광": {"bg": "rgba(255, 165, 0, 0.8)", "text": "#FFA500"},
    "풍력": {"bg": "rgba(152, 216, 200, 0.8)", "text": "#98D8C8"},
    "전력시장": {"bg": "rgba(240, 98, 146, 0.8)", "text": "#F06292"},
    "정책": {"bg": "rgba(126, 87, 194, 0.8)", "text": "#7E57C2"},
    "투자": {"bg": "rgba(92, 107, 192, 0.8)", "text": "#5C6BC0"},
    "기술": {"bg": "rgba(66, 165, 245, 0.8)", "text": "#42A5F5"},
    "시장": {"bg": "rgba(38, 166, 154, 0.8)", "text": "#26A69A"}
}

# 기본 CSS
BASE_CSS = f"""
<style>
/* 다크 테마 기본 설정 */
.stApp {{
    background-color: {COLORS['bg_primary']} !important;
}}

/* 헤더 스타일 */
.main-header {{
    text-align: center;
    padding: 60px 20px;
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
    border-radius: 30px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    color: white;
}}

.main-header::before {{
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: pulse 4s ease-in-out infinite;
}}

@keyframes pulse {{
    0%, 100% {{ transform: scale(1); opacity: 0.5; }}
    50% {{ transform: scale(1.1); opacity: 0.8; }}
}}

/* 카드 스타일 */
.news-card {{
    background: {COLORS['bg_secondary']};
    border: 1px solid {COLORS['border']};
    border-radius: 20px;
    padding: 30px;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}}

.news-card:hover {{
    background: {COLORS['bg_hover']};
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
}}

/* 애니메이션 */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.news-card {{
    animation: fadeInUp 0.6s ease forwards;
}}
</style>
"""

def get_category_style(category):
    """카테고리별 스타일 반환"""
    cat_color = CATEGORY_COLORS.get(category, CATEGORY_COLORS["기술"])
    return f"""
    background: {cat_color['bg']};
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    display: inline-block;
    """

def apply_theme():
    """Streamlit 앱에 테마 적용"""
    import streamlit as st
    st.markdown(BASE_CSS, unsafe_allow_html=True)

# HTML 템플릿
CARD_TEMPLATE = """
<div class="news-card" onclick="{onclick}">
    <span class="card-category" style="{category_style}">{category}</span>
    <h3 class="card-title" style="color: {text_primary};">{title}</h3>
    <p class="card-summary" style="color: {text_secondary};">{summary}</p>
    <div class="card-meta" style="color: {text_muted};">
        <span>{date}</span>
        <a href="#" class="read-more">자세히 보기 →</a>
    </div>
</div>
"""

def render_card(card_data):
    """카드 렌더링"""
    return CARD_TEMPLATE.format(
        onclick=f"window.location.href='{card_data['link']}'",
        category_style=get_category_style(card_data['category']),
        category=card_data['category'],
        title=card_data['title'],
        summary=card_data['summary'],
        date=card_data['date'],
        text_primary=COLORS['text_primary'],
        text_secondary=COLORS['text_secondary'],
        text_muted=COLORS['text_muted']
    )
