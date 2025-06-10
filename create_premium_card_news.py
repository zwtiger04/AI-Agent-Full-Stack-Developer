#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 프리미엄 카드뉴스 생성 - OpenAI GPT 활용
"""

import os
import sys
import shutil
import openai
import re
from datetime import datetime
from typing import List, Dict, Tuple

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# OpenAI API 설정
openai.api_key = os.getenv('OPENAI_API_KEY')

def analyze_article_with_gpt(article: Dict) -> Dict:
    """GPT-4를 사용해 기사를 깊이 있게 분석"""
    
    prompt = f"""
    다음 전력산업 기사를 분석해주세요:
    
    제목: {article.get('title', '')}
    요약: {article.get('summary', '')}
    핵심내용: {article.get('key_points', '')}
    
    다음 형식으로 분석해주세요:
    
    1. 한줄 핵심 (30자 이내, 가장 중요한 메시지)
    2. 핵심 수치 (기사에서 중요한 숫자들: MW, 억원, %, 날짜 등)
    3. 주요 분석 (3-4개 포인트, 각 50자 이내)
    4. 시사점 (이 기사가 전력산업에 미치는 영향)
    5. 향후 전망 (예상되는 변화나 트렌드)
    6. 연관 키워드 (5개)
    
    답변은 JSON 형식으로 해주세요.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 또는 gpt-4
            messages=[
                {"role": "system", "content": "당신은 전력산업 전문 분석가입니다. 기사를 깊이 있게 분석하고 인사이트를 제공합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # 응답 파싱
        content = response.choices[0].message.content
        
        # JSON 파싱 시도
        import json
        try:
            analysis = json.loads(content)
        except:
            # JSON 파싱 실패시 텍스트 파싱
            analysis = parse_text_response(content)
            
        return analysis
        
    except Exception as e:
        print(f"GPT 분석 실패: {e}")
        # 폴백: 기본 분석
        return fallback_analysis(article)


def parse_text_response(content: str) -> Dict:
    """텍스트 응답을 구조화된 데이터로 파싱"""
    analysis = {
        "한줄핵심": "",
        "핵심수치": [],
        "주요분석": [],
        "시사점": "",
        "향후전망": "",
        "연관키워드": []
    }
    
    lines = content.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if '한줄 핵심' in line or '한줄핵심' in line:
            current_section = '한줄핵심'
        elif '핵심 수치' in line or '핵심수치' in line:
            current_section = '핵심수치'
        elif '주요 분석' in line or '주요분석' in line:
            current_section = '주요분석'
        elif '시사점' in line:
            current_section = '시사점'
        elif '향후 전망' in line or '향후전망' in line:
            current_section = '향후전망'
        elif '연관 키워드' in line or '연관키워드' in line:
            current_section = '연관키워드'
        elif line and current_section:
            if current_section in ['핵심수치', '주요분석', '연관키워드']:
                if line.startswith(('-', '•', '*', '·')) or line[0].isdigit():
                    cleaned = line.lstrip('-•*·0123456789. ')
                    if cleaned:
                        analysis[current_section].append(cleaned)
            else:
                analysis[current_section] = line
                
    return analysis


def fallback_analysis(article: Dict) -> Dict:
    """GPT 실패시 규칙 기반 분석"""
    
    # 핵심 수치 추출
    text = article.get('title', '') + ' ' + article.get('summary', '') + ' ' + article.get('key_points', '')
    
    numbers = []
    # MW, GW 추출
    power_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(MW|GW|kW)', text)
    for value, unit in power_matches:
        numbers.append(f"{value}{unit}")
    
    # 금액 추출
    money_matches = re.findall(r'(\d+(?:,\d+)?(?:\.\d+)?)\s*(억원|만원)', text)
    for value, unit in money_matches:
        numbers.append(f"{value}{unit}")
    
    # 퍼센트 추출
    percent_matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
    for value in percent_matches:
        numbers.append(f"{value}%")
    
    # 주요 분석 포인트 생성
    key_points_list = []
    if article.get('key_points'):
        points = article['key_points'].split('\n')
        for point in points[:4]:
            point = point.strip()
            if point and len(point) > 10:
                key_points_list.append(point[:100])
    
    return {
        "한줄핵심": article.get('summary', '')[:50] + "...",
        "핵심수치": numbers[:5],
        "주요분석": key_points_list,
        "시사점": "전력산업의 변화와 혁신이 가속화되고 있음",
        "향후전망": "지속적인 기술 발전과 정책 지원이 예상됨",
        "연관키워드": article.get('keywords', [])
    }


def create_premium_summary(articles: List[Dict], analyses: List[Dict]) -> str:
    """프리미엄 요약 페이지 생성"""
    
    # 카테고리별 분류
    categories = {
        '정책/제도': [],
        '기술/혁신': [],
        '시장/투자': [],
        '기타': []
    }
    
    for i, article in enumerate(articles):
        article['analysis'] = analyses[i]
        
        keywords = article.get('keywords', [])
        title = article.get('title', '')
        
        if any(k in str(keywords) + title for k in ['정책', '제도', '법', '규제', '정부']):
            categories['정책/제도'].append(article)
        elif any(k in str(keywords) + title for k in ['기술', 'AI', 'ESS', '배터리', '혁신']):
            categories['기술/혁신'].append(article)
        elif any(k in str(keywords) + title for k in ['투자', '시장', '계약', 'MW', '매출']):
            categories['시장/투자'].append(article)
        else:
            categories['기타'].append(article)
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>전력산업 프리미엄 뉴스 분석 - {datetime.now().strftime('%Y년 %m월 %d일')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
            background: #0a0a0a;
            color: #ffffff;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 60px;
            padding-top: 40px;
        }}
        
        .header h1 {{
            font-size: 3.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            font-weight: 800;
        }}
        
        .subtitle {{
            font-size: 1.3rem;
            color: #888;
            margin-bottom: 40px;
        }}
        
        .insights-section {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 60px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .insights-title {{
            font-size: 2rem;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .insights-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}
        
        .insight-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }}
        
        .insight-card:hover {{
            background: rgba(255, 255, 255, 0.08);
            transform: translateY(-5px);
        }}
        
        .insight-number {{
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .insight-label {{
            color: #888;
            margin-top: 10px;
        }}
        
        .category-section {{
            margin-bottom: 60px;
        }}
        
        .category-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .category-title {{
            font-size: 2rem;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .article-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 30px;
        }}
        
        .article-card {{
            background: #1a1a1a;
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
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
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .article-card:hover {{
            background: #222;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        }}
        
        .article-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .article-title {{
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 15px;
            line-height: 1.4;
        }}
        
        .core-message {{
            background: rgba(102, 126, 234, 0.1);
            border-left: 3px solid #667eea;
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
            font-size: 1.1rem;
            color: #e0e0e0;
        }}
        
        .key-numbers {{
            display: flex;
            gap: 15px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        
        .number-badge {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.95rem;
        }}
        
        .analysis-points {{
            margin: 20px 0;
        }}
        
        .analysis-point {{
            padding: 8px 0;
            color: #ccc;
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }}
        
        .analysis-point::before {{
            content: '▸';
            color: #667eea;
            font-weight: bold;
        }}
        
        .article-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .keyword-tags {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .keyword-tag {{
            background: rgba(255, 255, 255, 0.1);
            color: #888;
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2.5rem; }}
            .article-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ 전력산업 프리미엄 뉴스 분석</h1>
            <p class="subtitle">{datetime.now().strftime('%Y년 %m월 %d일')} | AI 기반 심층 분석</p>
        </div>
        
        <div class="insights-section">
            <h2 class="insights-title">
                <span>🎯</span> 오늘의 핵심 인사이트
            </h2>
            <div class="insights-grid">
                <div class="insight-card">
                    <div class="insight-number">{len(articles)}</div>
                    <div class="insight-label">분석된 기사</div>
                </div>
                <div class="insight-card">
                    <div class="insight-number">{sum(1 for a in analyses if a.get('핵심수치'))}</div>
                    <div class="insight-label">핵심 데이터 포인트</div>
                </div>
                <div class="insight-card">
                    <div class="insight-number">{len(set(k for a in articles for k in a.get('keywords', [])))}</div>
                    <div class="insight-label">주요 트렌드 키워드</div>
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
                    <span style="font-size: 2.5rem;">{category_icons.get(category, '📄')}</span>
                    <span>{category}</span>
                </h2>
                <span style="color: #667eea; font-weight: 700;">{len(category_articles)}건</span>
            </div>
            <div class="article-grid">
"""
        
        for article in category_articles:
            analysis = article.get('analysis', {})
            
            # 파일명 생성
            safe_title = article.get('title', '').replace(' ', '-')
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '-_')[:50]
            detail_filename = f"detail_{safe_title}_{article.get('page_id', '')[:8]}.html"
            
            # 핵심 수치 배지
            numbers_html = ''
            for num in analysis.get('핵심수치', [])[:3]:
                numbers_html += f'<span class="number-badge">{num}</span>'
            
            # 주요 분석 포인트
            analysis_html = ''
            for point in analysis.get('주요분석', [])[:3]:
                analysis_html += f'<div class="analysis-point">{point}</div>'
            
            # 키워드 태그
            keywords_html = ''
            for keyword in article.get('keywords', [])[:4]:
                keywords_html += f'<span class="keyword-tag">{keyword}</span>'
            
            html += f"""
                <div class="article-card" onclick="window.location.href='detailed/{detail_filename}'">
                    <h3 class="article-title">{article.get('title', '제목 없음')}</h3>
                    
                    <div class="core-message">
                        💡 {analysis.get('한줄핵심', article.get('summary', '')[:80])}
                    </div>
                    
                    {f'<div class="key-numbers">{numbers_html}</div>' if numbers_html else ''}
                    
                    {f'<div class="analysis-points">{analysis_html}</div>' if analysis_html else ''}
                    
                    <div class="article-footer">
                        <div class="keyword-tags">{keywords_html}</div>
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


def create_premium_detail(article: Dict, analysis: Dict) -> str:
    """프리미엄 상세 페이지 생성"""
    
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
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
            background: #0a0a0a;
            color: #ffffff;
            line-height: 1.8;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
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
        }}
        
        .header {{
            text-align: center;
            padding: 60px 0;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 20px;
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
            background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
            padding: 0 40px;
        }}
        
        .header-meta {{
            position: relative;
            z-index: 1;
            display: flex;
            justify-content: center;
            gap: 40px;
            color: #888;
        }}
        
        .section {{
            background: #1a1a1a;
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .section-title {{
            font-size: 1.8rem;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 15px;
            color: #667eea;
        }}
        
        .core-insight {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
            border-left: 4px solid #667eea;
            padding: 25px;
            border-radius: 10px;
            font-size: 1.3rem;
            line-height: 1.8;
            margin-bottom: 30px;
        }}
        
        .data-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .data-card {{
            background: rgba(102, 126, 234, 0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(102, 126, 234, 0.3);
        }}
        
        .data-value {{
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .data-label {{
            color: #888;
            margin-top: 5px;
            font-size: 0.9rem;
        }}
        
        .analysis-list {{
            list-style: none;
        }}
        
        .analysis-item {{
            padding: 20px;
            margin-bottom: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            border-left: 3px solid #667eea;
            transition: all 0.3s;
        }}
        
        .analysis-item:hover {{
            background: rgba(255, 255, 255, 0.08);
            transform: translateX(10px);
        }}
        
        .implications {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
        }}
        
        .implications-content {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #e0e0e0;
        }}
        
        .outlook {{
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
            border: 1px solid rgba(102, 126, 234, 0.3);
        }}
        
        .keyword-cloud {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 20px;
        }}
        
        .keyword-bubble {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
            border: 1px solid rgba(102, 126, 234, 0.5);
            color: #fff;
            padding: 12px 24px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s;
        }}
        
        .keyword-bubble:hover {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            transform: scale(1.1);
        }}
        
        .footer {{
            text-align: center;
            padding: 40px;
            color: #888;
        }}
        
        .source-button {{
            display: inline-block;
            margin-top: 20px;
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 700;
            transition: all 0.3s;
        }}
        
        .source-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
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
                <span>🤖 AI 분석 완료</span>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">
                <span>💡</span> 핵심 인사이트
            </h2>
            <div class="core-insight">
                {analysis.get('한줄핵심', article.get('summary', ''))}
            </div>
        </div>
"""
    
    # 핵심 수치가 있으면 표시
    if analysis.get('핵심수치'):
        html += """
        <div class="section">
            <h2 class="section-title">
                <span>📊</span> 핵심 데이터
            </h2>
            <div class="data-grid">
"""
        for num in analysis.get('핵심수치', []):
            # 숫자와 단위 분리 시도
            import re
            match = re.match(r'([\d,.]+)(.+)', num)
            if match:
                value, unit = match.groups()
                html += f"""
                <div class="data-card">
                    <div class="data-value">{value}</div>
                    <div class="data-label">{unit}</div>
                </div>
"""
            else:
                html += f"""
                <div class="data-card">
                    <div class="data-value">{num}</div>
                    <div class="data-label">핵심 지표</div>
                </div>
"""
        html += """
            </div>
        </div>
"""
    
    # 주요 분석
    if analysis.get('주요분석'):
        html += """
        <div class="section">
            <h2 class="section-title">
                <span>🔍</span> 심층 분석
            </h2>
            <ul class="analysis-list">
"""
        for point in analysis.get('주요분석', []):
            html += f"""
                <li class="analysis-item">{point}</li>
"""
        html += """
            </ul>
        </div>
"""
    
    # 시사점
    if analysis.get('시사점'):
        html += f"""
        <div class="implications">
            <h2 class="section-title" style="color: white;">
                <span>🎯</span> 산업 시사점
            </h2>
            <p class="implications-content">
                {analysis.get('시사점')}
            </p>
        </div>
"""
    
    # 향후 전망
    if analysis.get('향후전망'):
        html += f"""
        <div class="outlook">
            <h2 class="section-title">
                <span>🔮</span> 향후 전망
            </h2>
            <p class="implications-content">
                {analysis.get('향후전망')}
            </p>
        </div>
"""
    
    # 연관 키워드
    keywords = analysis.get('연관키워드', article.get('keywords', []))
    if keywords:
        html += """
        <div class="section">
            <h2 class="section-title">
                <span>🏷️</span> 관련 키워드
            </h2>
            <div class="keyword-cloud">
"""
        for keyword in keywords:
            html += f"""
                <span class="keyword-bubble">{keyword}</span>
"""
        html += """
            </div>
        </div>
"""
    
    html += f"""
        <div class="footer">
            <p>이 분석은 AI 기반으로 생성되었습니다.</p>
            <a href="{article.get('url', '#')}" target="_blank" class="source-button">원문 보기 →</a>
        </div>
    </div>
</body>
</html>
"""
    
    return html


# 전역 변수
summary_filename = ""

def main():
    print("🎯 프리미엄 카드뉴스 생성 - OpenAI GPT 활용")
    print("=" * 60)
    
    try:
        from notion.notion_client import NotionClient
        
        notion = NotionClient()
        
        # 기사 수집
        print("\n📰 노션에서 기사 수집 중...")
        databases = notion.get_all_weekly_databases()
        all_articles = []
        
        for db_id in databases[:2]:  # 최근 2주
            articles = notion.get_all_articles_from_database(db_id)
            if articles:
                all_articles.extend(articles)
        
        # 필터링
        filtered = [a for a in all_articles if a.get('ai_recommend') or a.get('interest')][:8]
        
        if not filtered:
            filtered = all_articles[:8]
            
        print(f"✅ {len(filtered)}개 기사 선택")
        
        # GPT 분석
        print("\n🤖 AI 분석 시작...")
        analyses = []
        
        for i, article in enumerate(filtered):
            print(f"  분석 중 ({i+1}/{len(filtered)}): {article.get('title', '')[:40]}...")
            analysis = analyze_article_with_gpt(article)
            analyses.append(analysis)
        
        # 출력 디렉토리
        output_dir = "./premium_card_news_output"
        os.makedirs(output_dir, exist_ok=True)
        detail_dir = os.path.join(output_dir, "detailed")
        os.makedirs(detail_dir, exist_ok=True)
        
        # 요약 페이지 생성
        print("\n📋 프리미엄 요약 페이지 생성 중...")
        global summary_filename
        summary_filename = f"premium_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        summary_path = os.path.join(output_dir, summary_filename)
        
        summary_html = create_premium_summary(filtered, analyses)
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_html)
        
        # 상세 페이지들 생성
        print("\n📄 프리미엄 상세 페이지 생성 중...")
        for i, article in enumerate(filtered):
            safe_title = article.get('title', '').replace(' ', '-')
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '-_')[:50]
            detail_filename = f"detail_{safe_title}_{article.get('page_id', '')[:8]}.html"
            detail_path = os.path.join(detail_dir, detail_filename)
            
            detail_html = create_premium_detail(article, analyses[i])
            with open(detail_path, 'w', encoding='utf-8') as f:
                f.write(detail_html)
        
        # Windows로 복사
        windows_dir = "/mnt/c/Users/KJ/Desktop/PremiumCardNews"
        if os.path.exists(windows_dir):
            shutil.rmtree(windows_dir)
        shutil.copytree(output_dir, windows_dir)
        
        print(f"\n🎉 프리미엄 카드뉴스 생성 완료!")
        print(f"📁 위치: C:\\Users\\KJ\\Desktop\\PremiumCardNews\\")
        print(f"📋 요약: {summary_filename}")
        print(f"\n✨ 프리미엄 기능:")
        print("  - GPT 기반 심층 분석")
        print("  - 핵심 인사이트 도출")
        print("  - 데이터 시각화")
        print("  - 시사점 및 전망")
        print("  - 연관 키워드 분석")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
