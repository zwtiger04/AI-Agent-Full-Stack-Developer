#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 개선된 카드뉴스 생성 - 전체 버전
"""

import os
import sys
import shutil
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_improved_summary(articles):
    """개선된 요약 페이지 생성"""
    
    # 카테고리별로 기사 분류
    categories = {
        '정책/제도': [],
        '기술/혁신': [],
        '시장/투자': [],
        '기타': []
    }
    
    for article in articles:
        keywords = article.get('keywords', [])
        title = article.get('title', '')
        
        if any(k in str(keywords) + title for k in ['정책', '제도', '법', '규제', '정부', '기후에너지부']):
            categories['정책/제도'].append(article)
        elif any(k in str(keywords) + title for k in ['기술', 'AI', 'ESS', '배터리', '혁신', '개발', 'VPP']):
            categories['기술/혁신'].append(article)
        elif any(k in str(keywords) + title for k in ['투자', '시장', '계약', 'MW', '매출', '수익', '태양광']):
            categories['시장/투자'].append(article)
        else:
            categories['기타'].append(article)
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>전력산업 주요 뉴스 - {datetime.now().strftime('%Y년 %m월 %d일')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 50px;
        }}
        
        h1 {{
            font-size: 3rem;
            margin-bottom: 20px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
            animation: fadeInDown 1s ease;
        }}
        
        .subtitle {{
            font-size: 1.3rem;
            opacity: 0.9;
            animation: fadeInUp 1s ease 0.3s both;
        }}
        
        .stats-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 50px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            animation: fadeIn 1s ease 0.5s both;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            text-align: center;
        }}
        
        .stat-item {{
            padding: 25px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            transition: transform 0.3s ease;
        }}
        
        .stat-item:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            color: #555;
            font-size: 1.1rem;
        }}
        
        .category-section {{
            margin-bottom: 60px;
            animation: fadeInUp 1s ease;
        }}
        
        .category-header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px 30px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .category-title {{
            font-size: 2rem;
            color: #2c3e50;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .category-icon {{
            font-size: 2.5rem;
        }}
        
        .category-count {{
            background: #667eea;
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: bold;
        }}
        
        .articles-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 30px;
        }}
        
        .article-card {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}
        
        .article-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transform: scaleX(0);
            transition: transform 0.3s ease;
            transform-origin: left;
        }}
        
        .article-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }}
        
        .article-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .article-title {{
            font-size: 1.3rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .article-summary {{
            color: #555;
            line-height: 1.7;
            margin-bottom: 20px;
            font-size: 1rem;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .article-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #f0f0f0;
        }}
        
        .keywords {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .keyword {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .recommendation {{
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.95rem;
            font-weight: bold;
            padding: 6px 15px;
            border-radius: 20px;
            background: #f0f0f0;
        }}
        
        .recommendation.ai {{
            background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
            color: white;
        }}
        
        .recommendation.interest {{
            background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
            color: white;
        }}
        
        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
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
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @media (max-width: 768px) {{
            h1 {{ font-size: 2rem; }}
            .articles-grid {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            .category-header {{
                flex-direction: column;
                gap: 15px;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ 전력산업 주요 뉴스</h1>
            <p class="subtitle">{datetime.now().strftime('%Y년 %m월 %d일')} | AI가 선별한 핵심 소식</p>
        </div>
        
        <div class="stats-section">
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{len(articles)}</div>
                    <div class="stat-label">전체 기사</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{sum(1 for a in articles if a.get('ai_recommend'))}</div>
                    <div class="stat-label">AI 추천</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{sum(1 for a in articles if a.get('interest'))}</div>
                    <div class="stat-label">관심 기사</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(set(k for a in articles for k in a.get('keywords', [])))}</div>
                    <div class="stat-label">핵심 키워드</div>
                </div>
            </div>
        </div>
"""
    
    # 카테고리별 기사 표시
    category_icons = {
        '정책/제도': '📋',
        '기술/혁신': '🔬',
        '시장/투자': '💰',
        '기타': '📰'
    }
    
    for category, category_articles in categories.items():
        if not category_articles:
            continue
            
        html += f"""
        <div class="category-section">
            <div class="category-header">
                <h2 class="category-title">
                    <span class="category-icon">{category_icons.get(category, '📄')}</span>
                    <span>{category}</span>
                </h2>
                <span class="category-count">{len(category_articles)}건</span>
            </div>
            <div class="articles-grid">
"""
        
        for i, article in enumerate(category_articles):
            # 파일명 생성
            safe_title = article.get('title', '').replace(' ', '-')
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '-_')[:50]
            detail_filename = f"detail_{safe_title}_{article.get('page_id', '')[:8]}.html"
            
            keywords_html = ' '.join([f'<span class="keyword">{k}</span>' for k in article.get('keywords', [])])
            
            ai_badge = ""
            if article.get('ai_recommend'):
                ai_badge = '<div class="recommendation ai">🤖 AI 추천</div>'
            elif article.get('interest'):
                ai_badge = '<div class="recommendation interest">⭐ 관심</div>'
            
            html += f"""
                <div class="article-card" onclick="window.location.href='detailed/{detail_filename}'">
                    <h3 class="article-title">{article.get('title', '제목 없음')}</h3>
                    <p class="article-summary">{article.get('summary', '요약 없음')}</p>
                    <div class="article-meta">
                        <div class="keywords">{keywords_html}</div>
                        {ai_badge}
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
"""
    
    html += """
    </div>
</body>
</html>"""
    
    return html


def create_improved_detail(article):
    """개선된 상세 페이지 생성"""
    
    # 핵심 내용을 구조화
    key_points_list = []
    if article.get('key_points'):
        points = article['key_points'].split('\n')
        for point in points:
            point = point.strip()
            if point and (point.startswith('•') or point.startswith('-') or point.startswith('*')):
                key_points_list.append(point[1:].strip())
            elif point:
                key_points_list.append(point)
    
    # 데이터 추출
    import re
    data_points = []
    text = article.get('title', '') + ' ' + article.get('summary', '') + ' ' + article.get('key_points', '')
    
    # MW, GW 추출
    power_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(MW|GW|kW)', text)
    for value, unit in power_matches:
        data_points.append({'value': value, 'unit': unit, 'type': '전력 용량'})
    
    # 금액 추출
    money_matches = re.findall(r'(\d+(?:,\d+)?(?:\.\d+)?)\s*(억원|만원|원)', text)
    for value, unit in money_matches:
        data_points.append({'value': value, 'unit': unit, 'type': '투자 규모'})
    
    # 퍼센트 추출
    percent_matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
    for value in percent_matches:
        data_points.append({'value': value, 'unit': '%', 'type': '변화율'})
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article.get('title', '제목 없음')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 50px rgba(0,0,0,0.1);
        }}
        
        .home-button {{
            position: fixed;
            top: 30px;
            right: 30px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 28px;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            transition: all 0.3s;
            z-index: 100;
        }}
        
        .home-button:hover {{
            transform: scale(1.1) rotate(10deg);
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 20px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
        }}
        
        .header-meta {{
            display: flex;
            justify-content: center;
            gap: 40px;
            font-size: 1.1rem;
            opacity: 0.95;
            position: relative;
            z-index: 1;
        }}
        
        .summary-section {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 50px;
            margin: 40px;
            border-radius: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            position: relative;
        }}
        
        .summary-title {{
            font-size: 1.8rem;
            color: #1976d2;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .summary-content {{
            font-size: 1.2rem;
            color: #333;
            line-height: 1.8;
        }}
        
        .data-visualization {{
            padding: 40px;
            margin: 40px;
            background: #fafafa;
            border-radius: 20px;
        }}
        
        .data-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }}
        
        .data-item {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            transition: all 0.3s;
            border: 2px solid transparent;
        }}
        
        .data-item:hover {{
            transform: translateY(-5px);
            border-color: #667eea;
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
        }}
        
        .data-value {{
            font-size: 2.2rem;
            font-weight: bold;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .data-label {{
            color: #666;
            margin-top: 10px;
            font-size: 1rem;
        }}
        
        .key-points {{
            padding: 40px;
        }}
        
        .section-title {{
            font-size: 1.8rem;
            color: #2c3e50;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .point-list {{
            list-style: none;
        }}
        
        .point-item {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            transition: all 0.3s;
            font-size: 1.1rem;
            line-height: 1.8;
        }}
        
        .point-item:hover {{
            transform: translateX(10px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .keywords-section {{
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 40px;
            border-radius: 20px;
            text-align: center;
            color: white;
        }}
        
        .keywords-section .section-title {{
            color: white;
            justify-content: center;
        }}
        
        .keyword-list {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 25px;
        }}
        
        .keyword-tag {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            color: white;
            padding: 12px 25px;
            border-radius: 30px;
            font-weight: 600;
            transition: all 0.3s;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }}
        
        .keyword-tag:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.1);
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 50px;
            text-align: center;
        }}
        
        .source-link {{
            display: inline-block;
            margin-top: 20px;
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        }}
        
        .source-link:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .data-grid {{ grid-template-columns: 1fr; }}
            .home-button {{ top: 20px; right: 20px; width: 50px; height: 50px; }}
        }}
    </style>
</head>
<body>
    <a href="../{os.path.basename(summary_filename)}" class="home-button">🏠</a>
    
    <div class="container">
        <div class="header">
            <h1>{article.get('title', '제목 없음')}</h1>
            <div class="header-meta">
                <span>📰 {article.get('source', '출처 없음')}</span>
                <span>📅 {datetime.now().strftime('%Y년 %m월 %d일')}</span>
            </div>
        </div>
        
        <div class="summary-section">
            <h2 class="summary-title">
                <span>💡</span> 핵심 요약
            </h2>
            <p class="summary-content">{article.get('summary', '요약 없음')}</p>
        </div>
"""
    
    # 데이터 시각화
    if data_points:
        html += """
        <div class="data-visualization">
            <h2 class="section-title">
                <span>📊</span> 주요 데이터
            </h2>
            <div class="data-grid">
"""
        for data in data_points[:6]:
            html += f"""
                <div class="data-item">
                    <div class="data-value">{data['value']}{data['unit']}</div>
                    <div class="data-label">{data['type']}</div>
                </div>
"""
        html += """
            </div>
        </div>
"""
    
    # 주요 내용
    if key_points_list:
        html += """
        <div class="key-points">
            <h2 class="section-title">
                <span>📌</span> 상세 내용
            </h2>
            <ul class="point-list">
"""
        for point in key_points_list:
            html += f"""
                <li class="point-item">{point}</li>
"""
        html += """
            </ul>
        </div>
"""
    
    # 키워드
    if article.get('keywords'):
        html += """
        <div class="keywords-section">
            <h2 class="section-title">
                <span>🏷️</span> 관련 키워드
            </h2>
            <div class="keyword-list">
"""
        for keyword in article.get('keywords', []):
            html += f"""
                <span class="keyword-tag">{keyword}</span>
"""
        html += """
            </div>
        </div>
"""
    
    # 푸터
    html += f"""
        <div class="footer">
            <p style="font-size: 1.2rem; margin-bottom: 10px;">📚 전력산업 뉴스 상세 정보</p>
            <p style="opacity: 0.8;">더 자세한 내용은 원문을 확인해주세요</p>
            <a href="{article.get('url', '#')}" target="_blank" class="source-link">원문 보기 →</a>
        </div>
    </div>
</body>
</html>
"""
    
    return html


# 전역 변수
summary_filename = ""

def main():
    print("🎯 개선된 카드뉴스 생성 - 전체 버전")
    print("=" * 60)
    
    try:
        from notion.notion_client import NotionClient
        
        notion = NotionClient()
        
        # 여러 주차의 데이터베이스에서 기사 수집
        print("\n📰 여러 주차의 기사를 수집 중...")
        databases = notion.get_all_weekly_databases()
        all_articles = []
        
        for db_id in databases[:3]:  # 최근 3주치
            articles = notion.get_all_articles_from_database(db_id)
            if articles:
                all_articles.extend(articles)
                print(f"  ✅ 데이터베이스에서 {len(articles)}개 기사 수집")
        
        # 필터링
        filtered = [a for a in all_articles if a.get('ai_recommend') or a.get('interest')]
        
        # 없으면 최신 기사 중에서 키워드 매칭
        if not filtered:
            print("\n⚠️ AI 추천/관심 기사가 없어 키워드 기반으로 선택합니다.")
            important_keywords = ['ESS', 'VPP', '재생에너지', '태양광', '전력감독원', '기후에너지부']
            filtered = []
            
            for article in all_articles:
                if any(k in article.get('title', '') + ' '.join(article.get('keywords', [])) 
                      for k in important_keywords):
                    filtered.append(article)
                    if len(filtered) >= 10:
                        break
        
        # 최종적으로 최신 기사 사용
        if not filtered:
            filtered = all_articles[:10]
            
        print(f"\n✅ 총 {len(filtered)}개 기사 선택")
        
        # 출력 디렉토리
        output_dir = "./improved_card_news_output"
        os.makedirs(output_dir, exist_ok=True)
        detail_dir = os.path.join(output_dir, "detailed")
        os.makedirs(detail_dir, exist_ok=True)
        
        # 요약 페이지 생성
        print("\n📋 요약 페이지 생성 중...")
        global summary_filename
        summary_filename = f"improved_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        summary_path = os.path.join(output_dir, summary_filename)
        
        summary_html = create_improved_summary(filtered)
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_html)
        
        # 상세 페이지들 생성
        print("\n📄 상세 페이지 생성 중...")
        for i, article in enumerate(filtered):
            safe_title = article.get('title', '').replace(' ', '-')
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '-_')[:50]
            detail_filename = f"detail_{safe_title}_{article.get('page_id', '')[:8]}.html"
            detail_path = os.path.join(detail_dir, detail_filename)
            
            detail_html = create_improved_detail(article)
            with open(detail_path, 'w', encoding='utf-8') as f:
                f.write(detail_html)
            print(f"  ✅ ({i+1}/{len(filtered)}) {article.get('title', '')[:40]}...")
        
        # Windows로 복사
        windows_dir = "/mnt/c/Users/KJ/Desktop/ImprovedCardNews"
        if os.path.exists(windows_dir):
            shutil.rmtree(windows_dir)
        shutil.copytree(output_dir, windows_dir)
        
        print(f"\n🎉 개선된 카드뉴스 생성 완료!")
        print(f"📁 위치: C:\\Users\\KJ\\Desktop\\ImprovedCardNews\\")
        print(f"📋 요약: {summary_filename}")
        print(f"📄 상세: detailed 폴더 ({len(filtered)}개 파일)")
        print(f"\n💡 브라우저에서 요약 페이지를 열어보세요!")
        print(f"   각 카드를 클릭하면 상세 페이지로 이동합니다.")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
