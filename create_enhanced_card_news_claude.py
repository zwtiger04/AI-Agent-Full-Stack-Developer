#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 향상된 카드뉴스 생성 - Claude 스타일 심층 분석
"""

import os
import sys
import shutil
import re
from datetime import datetime
from typing import List, Dict, Tuple
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def analyze_article_deeply(article: Dict) -> Dict:
    """기사를 심층 분석하여 풍부한 콘텐츠 생성"""
    
    # 텍스트 통합
    full_text = f"{article.get('title', '')} {article.get('summary', '')} {article.get('key_points', '')}"
    
    # 1. 핵심 수치 추출 (고급)
    numbers = extract_key_numbers(full_text)
    
    # 2. 핵심 메시지 도출
    core_message = generate_core_message(article)
    
    # 3. 주요 분석 포인트 생성
    analysis_points = generate_analysis_points(article)
    
    # 4. 시사점 도출
    implications = generate_implications(article)
    
    # 5. 미래 전망
    outlook = generate_outlook(article)
    
    # 6. 연관 주제
    related_topics = generate_related_topics(article)
    
    return {
        "핵심메시지": core_message,
        "핵심수치": numbers,
        "주요분석": analysis_points,
        "시사점": implications,
        "미래전망": outlook,
        "연관주제": related_topics,
        "영향도": calculate_impact_score(article)
    }


def extract_key_numbers(text: str) -> List[Dict]:
    """핵심 수치를 추출하고 의미 부여"""
    numbers = []
    
    # MW/GW/kW 전력 용량
    power_patterns = [
        (r'(\d+(?:,\d+)?(?:\.\d+)?)\s*(GW)', '기가와트', 1000),
        (r'(\d+(?:,\d+)?(?:\.\d+)?)\s*(MW)', '메가와트', 1),
        (r'(\d+(?:,\d+)?(?:\.\d+)?)\s*(kW)', '킬로와트', 0.001)
    ]
    
    for pattern, unit_name, multiplier in power_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for value, unit in matches:
            clean_value = value.replace(',', '')
            mw_equivalent = float(clean_value) * multiplier
            
            # 규모 판단
            if mw_equivalent >= 1000:
                scale = "대규모"
            elif mw_equivalent >= 100:
                scale = "중규모"
            else:
                scale = "소규모"
                
            numbers.append({
                'value': value,
                'unit': unit,
                'type': '발전용량',
                'meaning': f"{scale} {unit_name} 프로젝트",
                'mw_equivalent': mw_equivalent
            })
    
    # 금액
    money_matches = re.findall(r'(\d+(?:,\d+)?(?:\.\d+)?)\s*(조원|억원|만원)', text)
    for value, unit in money_matches:
        clean_value = float(value.replace(',', ''))
        
        if unit == '조원':
            billion_won = clean_value * 10000
        elif unit == '억원':
            billion_won = clean_value
        else:  # 만원
            billion_won = clean_value / 10000
            
        if billion_won >= 10000:
            scale = "초대형"
        elif billion_won >= 1000:
            scale = "대형"
        elif billion_won >= 100:
            scale = "중형"
        else:
            scale = "소형"
            
        numbers.append({
            'value': value,
            'unit': unit,
            'type': '투자규모',
            'meaning': f"{scale} 투자",
            'billion_won': billion_won
        })
    
    # 퍼센트
    percent_matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
    for value in percent_matches:
        float_value = float(value)
        
        if float_value >= 50:
            meaning = "절반 이상"
        elif float_value >= 30:
            meaning = "상당한 비중"
        elif float_value >= 10:
            meaning = "의미있는 수준"
        else:
            meaning = "소폭"
            
        numbers.append({
            'value': value,
            'unit': '%',
            'type': '비율',
            'meaning': meaning
        })
    
    # 연도/기간
    year_matches = re.findall(r'(20\d{2})년', text)
    for year in year_matches[:2]:  # 최대 2개
        numbers.append({
            'value': year,
            'unit': '년',
            'type': '시점',
            'meaning': f"{int(year) - 2025}년 {'후' if int(year) > 2025 else '전'}"
        })
    
    return numbers[:6]  # 최대 6개


def generate_core_message(article: Dict) -> str:
    """핵심 메시지 생성"""
    title = article.get('title', '')
    summary = article.get('summary', '')
    
    # 키워드 기반 핵심 메시지 템플릿
    templates = {
        'ESS': "에너지 저장 시스템이 {action}하며 전력 안정성 {impact}",
        'VPP': "가상발전소가 {action}하여 분산에너지 {impact}",
        '태양광': "태양광 발전이 {action}하며 재생에너지 {impact}",
        '재생에너지': "재생에너지가 {action}하여 에너지 전환 {impact}",
        '정책': "정부 정책이 {action}하며 전력산업 {impact}",
        '투자': "대규모 투자가 {action}하여 시장 {impact}"
    }
    
    # 액션과 임팩트 추출
    action_words = {
        '확대': '확대되고',
        '증가': '증가하고',
        '구축': '구축되고',
        '시작': '시작되며',
        '체결': '체결되어',
        '운영': '운영되며',
        '전환': '전환되고'
    }
    
    impact_words = {
        '긍정': '향상에 기여',
        '성장': '성장을 가속화',
        '혁신': '혁신을 주도',
        '안정': '안정화에 기여',
        '확대': '확대를 견인'
    }
    
    # 기본 메시지
    for keyword, template in templates.items():
        if keyword in title or keyword in str(article.get('keywords', [])):
            action = '추진되고'
            impact = '발전에 기여'
            
            for act_key, act_val in action_words.items():
                if act_key in title + summary:
                    action = act_val
                    break
                    
            for imp_key, imp_val in impact_words.items():
                if imp_key in summary:
                    impact = imp_val
                    break
                    
            return template.format(action=action, impact=impact)
    
    # 폴백: 요약 첫 문장 활용
    if summary:
        first_sentence = summary.split('.')[0]
        if len(first_sentence) > 30:
            return first_sentence[:80] + "..."
        return first_sentence
    
    return "전력산업의 새로운 변화가 시작되고 있습니다"


def generate_analysis_points(article: Dict) -> List[str]:
    """주요 분석 포인트 생성"""
    points = []
    
    # 키포인트에서 추출
    if article.get('key_points'):
        key_points = article['key_points'].split('\n')
        for point in key_points:
            point = point.strip()
            if point and len(point) > 10:
                # 불필요한 기호 제거
                clean_point = re.sub(r'^[•\-\*\s]+', '', point)
                if clean_point:
                    # 포인트 개선
                    enhanced = enhance_point(clean_point, article)
                    points.append(enhanced)
    
    # 키워드 기반 추가 분석
    keywords = article.get('keywords', [])
    if 'ESS' in keywords and len(points) < 4:
        points.append("ESS 도입으로 재생에너지 출력 변동성 대응력 향상")
    if 'VPP' in keywords and len(points) < 4:
        points.append("분산자원 통합 관리로 전력 시스템 효율성 증대")
    if '태양광' in keywords and len(points) < 4:
        points.append("태양광 발전 확대로 탄소중립 목표 달성 가속화")
    
    return points[:5]  # 최대 5개


def enhance_point(point: str, article: Dict) -> str:
    """분석 포인트를 더 구체적으로 개선"""
    
    # 숫자가 있으면 강조
    numbers = re.findall(r'\d+(?:\.\d+)?', point)
    if numbers:
        for num in numbers:
            point = point.replace(num, f"**{num}**")
    
    # 주요 키워드 강조
    important_terms = ['AI', 'ESS', 'VPP', 'MW', 'GW', '재생에너지', '탄소중립']
    for term in important_terms:
        if term in point:
            point = point.replace(term, f"**{term}**")
    
    # 의미 보강
    if len(point) < 50:
        if '증가' in point:
            point += " 예상"
        elif '감소' in point:
            point += " 전망"
        elif '도입' in point:
            point += "으로 효율성 향상"
        elif '구축' in point:
            point += "을 통한 인프라 강화"
    
    return point


def generate_implications(article: Dict) -> str:
    """산업 시사점 도출"""
    
    keywords = article.get('keywords', [])
    title = article.get('title', '')
    
    implications_map = {
        'ESS': [
            "ESS 시장의 급속한 성장과 함께 안전성 확보가 핵심 과제로 부상",
            "에너지 저장 기술의 발전이 재생에너지 확대의 핵심 동력",
            "ESS를 통한 전력 수급 안정화로 계통 운영 효율성 대폭 개선"
        ],
        'VPP': [
            "가상발전소 활성화로 프로슈머 시대 본격 개막",
            "분산에너지 자원의 통합 관리가 미래 전력시장의 핵심",
            "VPP 플랫폼이 새로운 전력 거래 생태계 조성"
        ],
        '태양광': [
            "태양광 발전 확대로 전통 발전원과의 경쟁 심화",
            "자가소비형 태양광이 기업 RE100 달성의 주요 수단",
            "태양광 기술 혁신으로 그리드 패리티 달성 가속화"
        ],
        '정책': [
            "정부 정책 변화가 전력산업 구조 재편의 촉매제",
            "규제 개선으로 신산업 육성과 투자 활성화 기대",
            "에너지 전환 정책이 전력시장의 새로운 기회 창출"
        ]
    }
    
    # 키워드 매칭
    for keyword, implications in implications_map.items():
        if keyword in keywords or keyword in title:
            # 기사 내용에 맞는 시사점 선택
            for imp in implications:
                if any(term in imp for term in article.get('keywords', [])):
                    return imp
            return implications[0]
    
    # 일반적 시사점
    return "전력산업의 디지털 전환과 탈탄소화가 동시에 진행되며 새로운 비즈니스 기회 창출"


def generate_outlook(article: Dict) -> str:
    """미래 전망 생성"""
    
    # 숫자 추출해서 전망에 활용
    text = article.get('title', '') + ' ' + article.get('summary', '')
    years = re.findall(r'20(\d{2})', text)
    
    if years:
        latest_year = max(int(y) for y in years)
        if latest_year > 25:  # 2025년 이후
            timeframe = f"20{latest_year}년까지"
        else:
            timeframe = "향후 3~5년간"
    else:
        timeframe = "중장기적으로"
    
    outlooks = {
        'ESS': f"{timeframe} ESS 시장 연평균 20% 이상 성장하며 GWh급 대형 프로젝트 본격화",
        'VPP': f"{timeframe} VPP 참여 자원 10배 증가, 전력거래 규모 수조원대 형성",
        '태양광': f"{timeframe} 태양광 누적 설치용량 50GW 돌파, 주력 전원으로 자리매김",
        '재생에너지': f"{timeframe} 재생에너지 발전 비중 40% 달성, 화석연료 의존도 획기적 감소",
        '투자': f"{timeframe} 민간 투자 100조원 유치로 에너지 신산업 생태계 완성"
    }
    
    # 키워드 기반 전망 선택
    for keyword, outlook in outlooks.items():
        if keyword in str(article.get('keywords', [])):
            return outlook
    
    return f"{timeframe} 전력산업 패러다임 전환 완성, 탄소중립 전력시스템 구축"


def generate_related_topics(article: Dict) -> List[str]:
    """연관 주제 생성"""
    
    keywords = article.get('keywords', [])
    
    topic_map = {
        'ESS': ['배터리 기술', '안전 규제', '전력시장 제도', 'RE100'],
        'VPP': ['분산자원', 'P2P 거래', '블록체인', '스마트그리드'],
        '태양광': ['신재생에너지', 'REC', 'PPA', '탄소중립'],
        '재생에너지': ['에너지전환', '그린뉴딜', '탄소배출권', '수소경제'],
        '정책': ['전기사업법', '분산에너지법', '탄소중립기본법', '그린택소노미']
    }
    
    related = set()
    for keyword in keywords:
        if keyword in topic_map:
            related.update(topic_map[keyword])
    
    # 기본 키워드도 추가
    related.update(keywords)
    
    # 중복 제거하고 최대 6개 반환
    return list(related)[:6]


def calculate_impact_score(article: Dict) -> Dict:
    """기사의 영향도 점수 계산"""
    
    score = 0
    factors = []
    
    # 1. 숫자 규모 (MW, 억원 등)
    text = article.get('title', '') + ' ' + article.get('summary', '')
    
    # MW 체크
    mw_matches = re.findall(r'(\d+(?:\.\d+)?)\s*MW', text)
    if mw_matches:
        max_mw = max(float(m) for m in mw_matches)
        if max_mw >= 100:
            score += 30
            factors.append("대규모 프로젝트")
        elif max_mw >= 10:
            score += 20
            factors.append("중규모 프로젝트")
        else:
            score += 10
            factors.append("소규모 프로젝트")
    
    # 금액 체크
    money_matches = re.findall(r'(\d+(?:,\d+)?)\s*억원', text)
    if money_matches:
        max_money = max(float(m.replace(',', '')) for m in money_matches)
        if max_money >= 1000:
            score += 30
            factors.append("대규모 투자")
        elif max_money >= 100:
            score += 20
            factors.append("중규모 투자")
        else:
            score += 10
            factors.append("소규모 투자")
    
    # 2. 키워드 중요도
    important_keywords = ['정부', '정책', '법', '제도', '국가', '대통령']
    if any(k in text for k in important_keywords):
        score += 20
        factors.append("정책적 중요성")
    
    # 3. AI 추천 여부
    if article.get('ai_recommend'):
        score += 15
        factors.append("AI 추천")
    
    # 4. 관심 표시
    if article.get('interest'):
        score += 15
        factors.append("높은 관심도")
    
    # 영향도 레벨 결정
    if score >= 80:
        level = "매우 높음"
        color = "#ff4444"
    elif score >= 60:
        level = "높음"
        color = "#ff8800"
    elif score >= 40:
        level = "보통"
        color = "#ffbb00"
    else:
        level = "낮음"
        color = "#44aa44"
    
    return {
        'score': score,
        'level': level,
        'color': color,
        'factors': factors
    }


def create_enhanced_summary(articles: List[Dict], analyses: List[Dict]) -> str:
    """향상된 요약 페이지 생성"""
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>전력산업 프리미엄 뉴스 - {datetime.now().strftime('%Y년 %m월 %d일')}</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0f0f0f;
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
            padding: 60px 0;
            background: linear-gradient(180deg, #1a1a2e 0%, #0f0f0f 100%);
            border-radius: 30px;
            margin-bottom: 60px;
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
            background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 50%);
            animation: rotate 20s linear infinite;
        }}
        
        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        .header h1 {{
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
        }}
        
        .subtitle {{
            font-size: 1.5rem;
            color: #888;
            position: relative;
            z-index: 1;
        }}
        
        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 60px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #1a1a2e 0%, #232345 100%);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            border: 1px solid rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        }}
        
        .metric-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .metric-value {{
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .metric-label {{
            font-size: 1.1rem;
            color: #aaa;
        }}
        
        .section {{
            margin-bottom: 80px;
        }}
        
        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #333;
        }}
        
        .section-title {{
            font-size: 2.5rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .section-icon {{
            font-size: 3rem;
        }}
        
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
            gap: 40px;
        }}
        
        .article-card {{
            background: #1a1a1a;
            border-radius: 25px;
            padding: 35px;
            border: 1px solid #333;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}
        
        .article-card::after {{
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
            border-radius: 25px;
            opacity: 0;
            z-index: -1;
            transition: opacity 0.3s ease;
        }}
        
        .article-card:hover {{
            transform: translateY(-5px) scale(1.02);
            border-color: transparent;
        }}
        
        .article-card:hover::after {{
            opacity: 1;
        }}
        
        .card-header {{
            margin-bottom: 20px;
        }}
        
        .impact-indicator {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 700;
            margin-bottom: 15px;
        }}
        
        .article-title {{
            font-size: 1.4rem;
            font-weight: 700;
            line-height: 1.5;
            margin-bottom: 20px;
            color: #fff;
        }}
        
        .core-insight {{
            background: rgba(102, 126, 234, 0.1);
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            font-size: 1.05rem;
            line-height: 1.7;
        }}
        
        .key-metrics {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin: 20px 0;
        }}
        
        .metric-badge {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 700;
            font-size: 0.95rem;
            position: relative;
            overflow: hidden;
        }}
        
        .metric-badge::before {{
            content: attr(data-meaning);
            position: absolute;
            bottom: -100%;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.9);
            padding: 5px;
            font-size: 0.8rem;
            font-weight: 400;
            transition: bottom 0.3s ease;
        }}
        
        .metric-badge:hover::before {{
            bottom: 0;
        }}
        
        .analysis-preview {{
            margin: 20px 0;
        }}
        
        .analysis-item {{
            padding: 12px 0;
            color: #ccc;
            font-size: 0.95rem;
            line-height: 1.6;
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }}
        
        .analysis-item::before {{
            content: '▸';
            color: #667eea;
            font-weight: bold;
            flex-shrink: 0;
        }}
        
        .card-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #333;
        }}
        
        .tags {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .tag {{
            background: rgba(255, 255, 255, 0.1);
            color: #aaa;
            padding: 6px 14px;
            border-radius: 15px;
            font-size: 0.85rem;
            transition: all 0.3s ease;
        }}
        
        .tag:hover {{
            background: rgba(102, 126, 234, 0.3);
            color: #fff;
        }}
        
        .read-more {{
            color: #667eea;
            font-weight: 700;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: gap 0.3s ease;
        }}
        
        .read-more:hover {{
            gap: 10px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2.5rem; }}
            .cards-grid {{ grid-template-columns: 1fr; }}
            .dashboard {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ 전력산업 인사이트</h1>
            <p class="subtitle">{datetime.now().strftime('%Y년 %m월 %d일')} | Claude AI 심층 분석</p>
        </div>
        
        <div class="dashboard">
            <div class="metric-card">
                <div class="metric-value">{len(articles)}</div>
                <div class="metric-label">분석 기사</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{sum(len(a.get('핵심수치', [])) for a in analyses)}</div>
                <div class="metric-label">핵심 데이터</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{len(set(t for a in analyses for t in a.get('연관주제', [])))}</div>
                <div class="metric-label">트렌드 키워드</div>
            </div>
        </div>
"""
    
    # 영향도별로 기사 분류
    high_impact = []
    medium_impact = []
    low_impact = []
    
    for i, article in enumerate(articles):
        article['analysis'] = analyses[i]
        impact = analyses[i].get('영향도', {})
        if impact.get('score', 0) >= 60:
            high_impact.append(article)
        elif impact.get('score', 0) >= 40:
            medium_impact.append(article)
        else:
            low_impact.append(article)
    
    # 섹션별 표시
    sections = [
        ("🔥 핵심 이슈", high_impact, "영향도 높은 주요 뉴스"),
        ("📈 주목할 동향", medium_impact, "업계 주목 소식"),
        ("📰 기타 소식", low_impact, "참고할 만한 뉴스")
    ]
    
    for section_title, section_articles, section_desc in sections:
        if not section_articles:
            continue
            
        html += f"""
        <div class="section">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="section-icon">{section_title.split()[0]}</span>
                    <span>{section_title}</span>
                </h2>
                <span style="color: #888;">{len(section_articles)}건 | {section_desc}</span>
            </div>
            <div class="cards-grid">
"""
        
        for article in section_articles:
            analysis = article.get('analysis', {})
            impact = analysis.get('영향도', {})
            
            # 파일명 생성
            safe_title = article.get('title', '').replace(' ', '-')
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '-_')[:50]
            detail_filename = f"detail_{safe_title}_{article.get('page_id', '')[:8]}.html"
            
            # 핵심 수치 HTML
            metrics_html = ''
            for metric in analysis.get('핵심수치', [])[:3]:
                metrics_html += f'''<span class="metric-badge" data-meaning="{metric.get('meaning', '')}">{metric['value']}{metric['unit']}</span>'''
            
            # 분석 포인트 HTML
            analysis_html = ''
            for point in analysis.get('주요분석', [])[:2]:
                # **text** 형식을 <strong>으로 변환
                formatted_point = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', point)
                analysis_html += f'<div class="analysis-item">{formatted_point}</div>'
            
            # 태그 HTML
            tags_html = ''
            for tag in article.get('keywords', [])[:4]:
                tags_html += f'<span class="tag">{tag}</span>'
            
            # 영향도 색상
            impact_style = f"background: {impact.get('color', '#667eea')}; color: white;"
            
            html += f"""
                <div class="article-card" onclick="window.location.href='detailed/{detail_filename}'">
                    <div class="card-header">
                        <span class="impact-indicator" style="{impact_style}">
                            영향도: {impact.get('level', '보통')}
                        </span>
                        <h3 class="article-title">{article.get('title', '제목 없음')}</h3>
                    </div>
                    
                    <div class="core-insight">
                        💡 {analysis.get('핵심메시지', '')}
                    </div>
                    
                    {f'<div class="key-metrics">{metrics_html}</div>' if metrics_html else ''}
                    
                    {f'<div class="analysis-preview">{analysis_html}</div>' if analysis_html else ''}
                    
                    <div class="card-footer">
                        <div class="tags">{tags_html}</div>
                        <a href="#" class="read-more" onclick="event.stopPropagation();">
                            자세히 보기 →
                        </a>
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


def create_enhanced_detail(article: Dict, analysis: Dict) -> str:
    """향상된 상세 페이지 생성"""
    
    # 키포인트 구조화
    key_points_html = ''
    if article.get('key_points'):
        points = article['key_points'].split('\n')
        for point in points:
            point = point.strip()
            if point:
                clean_point = re.sub(r'^[•\-\*\s]+', '', point)
                if clean_point:
                    # 강조 처리
                    formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', clean_point)
                    key_points_html += f'<li class="point-item">{formatted}</li>'
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article.get('title', '제목 없음')}</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Pretendard', -apple-system, sans-serif;
            background: #0a0a0a;
            color: #ffffff;
            line-height: 1.8;
        }}
        
        .container {{
            max-width: 1000px;
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
            transform: scale(1.1) rotate(360deg);
        }}
        
        .hero {{
            background: linear-gradient(135deg, #1a1a2e 0%, #232345 100%);
            border-radius: 30px;
            padding: 60px;
            margin-bottom: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(102, 126, 234, 0.15) 0%, transparent 50%);
            animation: pulse 4s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
        }}
        
        .hero h1 {{
            font-size: 2.8rem;
            font-weight: 900;
            margin-bottom: 30px;
            position: relative;
            z-index: 1;
            line-height: 1.3;
        }}
        
        .hero-meta {{
            display: flex;
            justify-content: center;
            gap: 40px;
            position: relative;
            z-index: 1;
            color: #aaa;
            font-size: 1.1rem;
        }}
        
        .section {{
            background: #1a1a1a;
            border-radius: 25px;
            padding: 50px;
            margin-bottom: 40px;
            border: 1px solid #333;
            position: relative;
        }}
        
        .section-header {{
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 15px;
            color: #667eea;
        }}
        
        .core-message {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
            border-left: 5px solid #667eea;
            padding: 30px;
            border-radius: 15px;
            font-size: 1.3rem;
            line-height: 1.8;
            margin-bottom: 40px;
            font-weight: 500;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        
        .metric-card {{
            background: rgba(102, 126, 234, 0.1);
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            border-color: #667eea;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .metric-label {{
            color: #888;
            font-size: 0.95rem;
        }}
        
        .metric-meaning {{
            color: #667eea;
            font-size: 0.9rem;
            margin-top: 5px;
            font-weight: 600;
        }}
        
        .analysis-list {{
            list-style: none;
            margin: 30px 0;
        }}
        
        .analysis-item {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
            font-size: 1.1rem;
            line-height: 1.8;
        }}
        
        .analysis-item:hover {{
            background: rgba(255, 255, 255, 0.08);
            transform: translateX(10px);
        }}
        
        .analysis-item strong {{
            color: #667eea;
            font-weight: 700;
        }}
        
        .implications-box {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
        }}
        
        .implications-content {{
            font-size: 1.2rem;
            line-height: 1.8;
            color: #e0e0e0;
        }}
        
        .outlook-box {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
        }}
        
        .topics-cloud {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 30px;
        }}
        
        .topic-bubble {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
            border: 2px solid rgba(102, 126, 234, 0.5);
            color: #fff;
            padding: 15px 30px;
            border-radius: 30px;
            font-weight: 700;
            font-size: 1.05rem;
            transition: all 0.3s;
        }}
        
        .topic-bubble:hover {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            transform: scale(1.1);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }}
        
        .original-content {{
            background: #0f0f0f;
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
        }}
        
        .point-list {{
            list-style: none;
        }}
        
        .point-item {{
            padding: 20px;
            margin-bottom: 15px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            border-left: 3px solid #444;
            transition: all 0.3s;
            line-height: 1.8;
        }}
        
        .point-item:hover {{
            background: rgba(255, 255, 255, 0.05);
            border-left-color: #667eea;
            transform: translateX(5px);
        }}
        
        .footer {{
            text-align: center;
            padding: 60px 20px;
            color: #888;
        }}
        
        .source-button {{
            display: inline-block;
            margin-top: 30px;
            padding: 18px 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 700;
            font-size: 1.1rem;
            transition: all 0.3s;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        }}
        
        .source-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.5);
        }}
    </style>
</head>
<body>
    <a href="../{os.path.basename(summary_filename)}" class="home-button">🏠</a>
    
    <div class="container">
        <div class="hero">
            <h1>{article.get('title', '제목 없음')}</h1>
            <div class="hero-meta">
                <span>📰 {article.get('source', '출처 없음')}</span>
                <span>📅 {datetime.now().strftime('%Y년 %m월 %d일')}</span>
                <span>🤖 Claude AI 분석</span>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-header">
                <span>💡</span> 핵심 인사이트
            </h2>
            <div class="core-message">
                {analysis.get('핵심메시지', article.get('summary', ''))}
            </div>
        </div>
"""
    
    # 핵심 수치 섹션
    if analysis.get('핵심수치'):
        html += """
        <div class="section">
            <h2 class="section-header">
                <span>📊</span> 핵심 데이터 분석
            </h2>
            <div class="metrics-grid">
"""
        for metric in analysis.get('핵심수치', []):
            html += f"""
                <div class="metric-card">
                    <div class="metric-value">{metric.get('value', '')}{metric.get('unit', '')}</div>
                    <div class="metric-label">{metric.get('type', '데이터')}</div>
                    <div class="metric-meaning">{metric.get('meaning', '')}</div>
                </div>
"""
        html += """
            </div>
        </div>
"""
    
    # 심층 분석
    if analysis.get('주요분석'):
        html += """
        <div class="section">
            <h2 class="section-header">
                <span>🔍</span> 심층 분석
            </h2>
            <ul class="analysis-list">
"""
        for point in analysis.get('주요분석', []):
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', point)
            html += f"""
                <li class="analysis-item">{formatted}</li>
"""
        html += """
            </ul>
        </div>
"""
    
    # 산업 시사점
    if analysis.get('시사점'):
        html += f"""
        <div class="implications-box">
            <h2 class="section-header" style="color: white;">
                <span>🎯</span> 산업 시사점
            </h2>
            <p class="implications-content">
                {analysis.get('시사점')}
            </p>
        </div>
"""
    
    # 미래 전망
    if analysis.get('미래전망'):
        html += f"""
        <div class="outlook-box">
            <h2 class="section-header">
                <span>🔮</span> 미래 전망
            </h2>
            <p class="implications-content">
                {analysis.get('미래전망')}
            </p>
        </div>
"""
    
    # 원본 핵심 내용
    if key_points_html:
        html += """
        <div class="original-content">
            <h2 class="section-header">
                <span>📋</span> 상세 내용
            </h2>
            <ul class="point-list">
"""
        html += key_points_html
        html += """
            </ul>
        </div>
"""
    
    # 연관 주제
    if analysis.get('연관주제'):
        html += """
        <div class="section">
            <h2 class="section-header">
                <span>🏷️</span> 연관 주제
            </h2>
            <div class="topics-cloud">
"""
        for topic in analysis.get('연관주제', []):
            html += f"""
                <span class="topic-bubble">{topic}</span>
"""
        html += """
            </div>
        </div>
"""
    
    html += f"""
        <div class="footer">
            <p style="font-size: 1.2rem; margin-bottom: 10px;">이 분석은 Claude AI가 생성한 심층 분석입니다.</p>
            <p>더 자세한 내용은 원문을 확인해주세요.</p>
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
    print("🎯 향상된 카드뉴스 생성 - Claude 스타일 심층 분석")
    print("=" * 60)
    
    try:
        from notion.notion_client import NotionClient
        
        notion = NotionClient()
        
        # 기사 수집
        print("\n📰 노션에서 기사 수집 중...")
        databases = notion.get_all_weekly_databases()
        all_articles = []
        
        for db_id in databases[:3]:  # 최근 3주
            articles = notion.get_all_articles_from_database(db_id)
            if articles:
                all_articles.extend(articles)
        
        # 필터링
        filtered = [a for a in all_articles if a.get('ai_recommend') or a.get('interest')][:10]
        
        if not filtered:
            # 키워드 기반 선택
            important_keywords = ['ESS', 'VPP', '재생에너지', '태양광', '정책']
            filtered = []
            for article in all_articles:
                if any(k in article.get('title', '') + ' '.join(article.get('keywords', [])) 
                      for k in important_keywords):
                    filtered.append(article)
                    if len(filtered) >= 10:
                        break
        
        if not filtered:
            filtered = all_articles[:10]
            
        print(f"✅ {len(filtered)}개 기사 선택")
        
        # 심층 분석
        print("\n🤖 Claude 스타일 심층 분석 시작...")
        analyses = []
        
        for i, article in enumerate(filtered):
            print(f"  분석 중 ({i+1}/{len(filtered)}): {article.get('title', '')[:40]}...")
            analysis = analyze_article_deeply(article)
            analyses.append(analysis)
        
        # 출력 디렉토리
        output_dir = "./enhanced_card_news_output"
        os.makedirs(output_dir, exist_ok=True)
        detail_dir = os.path.join(output_dir, "detailed")
        os.makedirs(detail_dir, exist_ok=True)
        
        # 요약 페이지 생성
        print("\n📋 향상된 요약 페이지 생성 중...")
        global summary_filename
        summary_filename = f"enhanced_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        summary_path = os.path.join(output_dir, summary_filename)
        
        summary_html = create_enhanced_summary(filtered, analyses)
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_html)
        
        # 상세 페이지들 생성
        print("\n📄 향상된 상세 페이지 생성 중...")
        for i, article in enumerate(filtered):
            safe_title = article.get('title', '').replace(' ', '-')
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '-_')[:50]
            detail_filename = f"detail_{safe_title}_{article.get('page_id', '')[:8]}.html"
            detail_path = os.path.join(detail_dir, detail_filename)
            
            detail_html = create_enhanced_detail(article, analyses[i])
            with open(detail_path, 'w', encoding='utf-8') as f:
                f.write(detail_html)
        
        # Windows로 복사
        windows_dir = "/mnt/c/Users/KJ/Desktop/EnhancedCardNews"
        if os.path.exists(windows_dir):
            shutil.rmtree(windows_dir)
        shutil.copytree(output_dir, windows_dir)
        
        print(f"\n🎉 향상된 카드뉴스 생성 완료!")
        print(f"📁 위치: C:\\Users\\KJ\\Desktop\\EnhancedCardNews\\")
        print(f"📋 요약: {summary_filename}")
        print(f"\n✨ 주요 특징:")
        print("  - 핵심 메시지 자동 도출")
        print("  - 데이터 의미 분석 (규모, 영향도)")
        print("  - 심층 분석 포인트 생성")
        print("  - 산업 시사점 및 미래 전망")
        print("  - 영향도 기반 우선순위")
        print("  - 연관 주제 자동 매핑")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
