#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 개선된 카드뉴스 생성 (비교 없이 개선 버전만)
"""

import os
import sys
import shutil
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_improved_summary(articles):
    """개선된 요약 페이지 생성 (비교 없이)"""
    
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
        
        # 키워드나 제목으로 카테고리 분류
        if any(k in str(keywords) + title for k in ['정책', '제도', '법', '규제', '정부']):
            categories['정책/제도'].append(article)
        elif any(k in str(keywords) + title for k in ['기술', 'AI', 'ESS', '배터리', '혁신', '개발']):
            categories['기술/혁신'].append(article)
        elif any(k in str(keywords) + title for k in ['투자', '시장', '계약', 'MW', '매출', '수익']):
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
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        h1 {{
            text-align: center;
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        
        .subtitle {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 40px;
            font-size: 1.1rem;
        }}
        
        .category-section {{
            margin-bottom: 50px;
        }}
        
        .category-title {{
            font-size: 1.8rem;
            color: #34495e;
            margin-bottom: 20px;
            padding-left: 15px;
            border-left: 5px solid #3498db;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .category-icon {{
            font-size: 1.5rem;
        }}
        
        .articles-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }}
        
        .article-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}
        
        .article-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }}
        
        .article-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3498db, #2ecc71);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .article-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .article-title {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            line-height: 1.4;
        }}
        
        .article-summary {{
            color: #555;
            line-height: 1.6;
            margin-bottom: 15px;
            font-size: 0.95rem;
        }}
        
        .article-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid #ecf0f1;
        }}
        
        .keywords {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        
        .keyword {{
            background: #e8f4f8;
            color: #2980b9;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .recommendation {{
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.9rem;
            color: #27ae60;
            font-weight: bold;
        }}
        
        .stats-section {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            text-align: center;
        }}
        
        .stat-item {{
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #3498db;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        
        @media (max-width: 768px) {{
            .articles-grid {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ 전력산업 주요 뉴스</h1>
        <p class="subtitle">{datetime.now().strftime('%Y년 %m월 %d일')} 주요 소식</p>
        
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
            <h2 class="category-title">
                <span class="category-icon">{category_icons.get(category, '📄')}</span>
                {category} ({len(category_articles)}건)
            </h2>
            <div class="articles-grid">
"""
        
        for i, article in enumerate(category_articles):
            # 파일명 생성 (상세 페이지와 동일한 규칙)
            safe_title = article.get('title', '').replace(' ', '-')
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '-_')[:50]
            detail_filename = f"detail_{safe_title}_{article.get('page_id', '')[:8]}.html"
            
            keywords_html = ' '.join([f'<span class="keyword">{k}</span>' for k in article.get('keywords', [])])
            
            ai_badge = ""
            if article.get('ai_recommend'):
                ai_badge = '<div class="recommendation">🤖 AI 추천</div>'
            elif article.get('interest'):
                ai_badge = '<div class="recommendation">⭐ 관심</div>'
            
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
    
    # 데이터 추출 (숫자, 용량 등)
    import re
    data_points = []
    text = article.get('title', '') + ' ' + article.get('summary', '') + ' ' + article.get('key_points', '')
    
    # MW, GW 추출
    power_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(MW|GW|kW)', text)
    for value, unit in power_matches:
        data_points.append(f"{value} {unit}")
    
    # 금액 추출
    money_matches = re.findall(r'(\d+(?:,\d+)?(?:\.\d+)?)\s*(억원|만원|원)', text)
    for value, unit in money_matches:
        data_points.append(f"{value} {unit}")
    
    # 퍼센트 추출
    percent_matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
    for value in percent_matches:
        data_points.append(f"{value}%")
    
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
            max-width: 800px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
        }}
        
        /* 홈 버튼 */
        .home-button {{
            position: fixed;
            top: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            background: #3498db;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 24px;
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
            transition: all 0.3s;
            z-index: 100;
        }}
        
        .home-button:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
        }}
        
        /* 헤더 섹션 */
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.2rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header-meta {{
            display: flex;
            justify-content: center;
            gap: 30px;
            font-size: 1rem;
            opacity: 0.9;
        }}
        
        /* 핵심 요약 섹션 */
        .summary-section {{
            background: #e8f4f8;
            padding: 40px;
            margin: 30px;
            border-radius: 15px;
            border-left: 5px solid #3498db;
        }}
        
        .summary-title {{
            font-size: 1.5rem;
            color: #2c3e50;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .summary-content {{
            font-size: 1.1rem;
            color: #34495e;
            line-height: 1.8;
        }}
        
        /* 데이터 시각화 */
        .data-visualization {{
            padding: 30px;
            margin: 30px;
            background: #f8f9fa;
            border-radius: 15px;
        }}
        
        .data-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .data-item {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }}
        
        .data-value {{
            font-size: 1.8rem;
            font-weight: bold;
            color: #3498db;
        }}
        
        .data-label {{
            color: #7f8c8d;
            margin-top: 5px;
            font-size: 0.9rem;
        }}
        
        /* 주요 내용 섹션 */
        .key-points {{
            padding: 30px;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            color: #2c3e50;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .point-list {{
            list-style: none;
        }}
        
        .point-item {{
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            border-left: 4px solid #2ecc71;
            transition: all 0.3s;
        }}
        
        .point-item:hover {{
            transform: translateX(5px);
            box-shadow: 0 3px 15px rgba(0,0,0,0.1);
        }}
        
        /* 키워드 섹션 */
        .keywords-section {{
            padding: 30px;
            background: #ecf0f1;
            margin: 30px;
            border-radius: 15px;
            text-align: center;
        }}
        
        .keyword-list {{
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 15px;
        }}
        
        .keyword-tag {{
            background: #3498db;
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 500;
            transition: all 0.3s;
        }}
        
        .keyword-tag:hover {{
            background: #2980b9;
            transform: scale(1.05);
        }}
        
        /* 푸터 */
        .footer {{
            background: #34495e;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .source-link {{
            display: inline-block;
            margin-top: 15px;
            padding: 10px 25px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s;
        }}
        
        .source-link:hover {{
            background: #2980b9;
            transform: translateY(-2px);
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.6rem;
            }}
            
            .data-grid {{
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            }}
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
    
    # 데이터 시각화 섹션 (데이터가 있을 때만)
    if data_points:
        html += """
        <div class="data-visualization">
            <h2 class="section-title">
                <span>📊</span> 주요 수치
            </h2>
            <div class="data-grid">
"""
        for i, data in enumerate(data_points[:4]):  # 최대 4개만 표시
            html += f"""
                <div class="data-item">
                    <div class="data-value">{data}</div>
                    <div class="data-label">핵심 지표</div>
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
                <span>📌</span> 주요 내용
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
            <h2 class="section-title" style="justify-content: center;">
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
            <p>📚 전력산업 뉴스 카드</p>
            <a href="{article.get('url', '#')}" target="_blank" class="source-link">원문 보기 →</a>
        </div>
    </div>
</body>
</html>
"""
    
    return html


# 전역 변수로 요약 파일명 저장
summary_filename = ""

def main():
    print("🎯 개선된 카드뉴스 생성 (개선 버전만)")
    print("=" * 60)
    
    try:
        # 1. 노션에서 데이터 가져오기
        from notion.notion_client import NotionClient
        
        notion = NotionClient()
        database_id = notion.get_weekly_database_id()
        
        if not database_id:
            print("❌ 데이터베이스를 찾을 수 없습니다!")
            return
            
        # 기사 가져오기
        articles = notion.get_all_articles_from_database(database_id)
        
        # AI 추천 또는 관심 기사 필터링
        filtered = [a for a in articles if a.get('ai_recommend') or a.get('interest')][:10]
        
        if not filtered:
            print("⚠️ AI 추천/관심 기사가 없어 최신 기사 5개를 사용합니다.")
            filtered = articles[:5]
            
        print(f"✅ {len(filtered)}개 기사 선택")
        
        # 2. 출력 디렉토리 생성
        output_dir = "./improved_card_news_output"
        os.makedirs(output_dir, exist_ok=True)
        detail_dir = os.path.join(output_dir, "detailed")
        os.makedirs(detail_dir, exist_ok=True)
        
        # 3. 요약 페이지 생성
        print("\n📋 요약 페이지 생성 중...")
        global summary_filename
        summary_filename = f"improved_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        summary_path = os.path.join(output_dir, summary_filename)
        
        summary_html = create_improved_summary(filtered)
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_html)
        print(f"✅ 요약 페이지 생성 완료: {summary_filename}")
        
        # 4. 상세 페이지들 생성
        print("\n📄 상세 페이지 생성 중...")
        for i, article in enumerate(filtered):
            # 파일명 생성
            safe_title = article.get('title', '').replace(' ', '-')
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '-_')[:50]
            detail_filename = f"detail_{safe_title}_{article.get('page_id', '')[:8]}.html"
            detail_path = os.path.join(detail_dir, detail_filename)
            
            detail_html = create_improved_detail(article)
            with open(detail_path, 'w', encoding='utf-8') as f:
                f.write(detail_html)
            print(f"  ✅ ({i+1}/{len(filtered)}) {article.get('title', '')[:30]}...")
        
        # 5. Windows로 복사
        print("\n📁 Windows로 복사 중...")
        windows_dir = "/mnt/c/Users/KJ/Desktop/ImprovedCardNews"
        
        if os.path.exists(windows_dir):
            shutil.rmtree(windows_dir)
        shutil.copytree(output_dir, windows_dir)
        
        print(f"\n🎉 개선된 카드뉴스 생성 완료!")
        print(f"📁 위치: C:\\Users\\KJ\\Desktop\\ImprovedCardNews\\")
        print(f"📋 요약: {summary_filename}")
        print(f"📄 상세: detailed 폴더 ({len(filtered)}개 파일)")
        print(f"\n💡 브라우저에서 요약 페이지를 열어 카드를 클릭하면 상세 페이지로 이동합니다!")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
