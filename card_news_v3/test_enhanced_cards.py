#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 향상된 카드 뉴스 테스트
"""

import sys
import os
sys.path.append('/home/zwtiger/AI-Agent-Full-Stack-Developer')
sys.path.append('/home/zwtiger/AI-Agent-Full-Stack-Developer/card_news_v3')

from enhanced_card_generator import EnhancedCardNewsGenerator
from structured_content_generator import StructuredContentGenerator
from datetime import datetime, timedelta

def test_enhanced_cards():
    """향상된 카드 뉴스 테스트"""
    
    # 테스트 데이터 준비
    test_articles = [
        {
            'title': '재생에너지 발전량 40% 돌파, 석탄발전 첫 역전',
            'content': '''국내 재생에너지 발전량이 처음으로 전체 발전량의 40%를 넘어서며 
            석탄발전을 역전했다. 전력거래소에 따르면 6월 첫째 주 재생에너지 발전 비중은 
            42.3%를 기록했으며, 석탄발전은 38.5%에 그쳤다. 
            
            특히 태양광 발전이 25.3%, 풍력이 12.1%를 차지하며 재생에너지 확대를 주도했다.
            이는 정부의 재생에너지 3020 정책과 민간 투자 확대가 결실을 맺은 것으로 평가된다.
            
            전문가들은 ESS 확충과 스마트그리드 구축이 재생에너지 비중 확대의 핵심이라고 분석했다.''',
            'keywords': ['재생에너지', '태양광', '풍력', '에너지전환'],
            'summary': '재생에너지 발전 비중이 42.3%로 석탄발전(38.5%)을 처음 추월',
            'ai_recommend': True,
            'published_date': datetime.now()
        },
        {
            'title': 'K-배터리, 미국 IRA 보조금 1조원 확보',
            'content': '''국내 배터리 3사가 미국 인플레이션 감축법(IRA) 보조금으로 
            총 1조원을 확보했다. LG에너지솔루션이 5000억원, SK온이 3000억원, 
            삼성SDI가 2000억원을 각각 받게 됐다.
            
            이는 북미 전기차 시장 확대와 함께 K-배터리의 경쟁력을 입증한 결과로 해석된다.
            3사는 확보한 보조금을 미국 현지 생산시설 확충에 재투자할 계획이다.''',
            'keywords': ['배터리', 'IRA', '전기차', 'ESS'],
            'summary': 'K-배터리 3사, 미국 IRA 보조금 총 1조원 확보로 북미 시장 공략 가속화',
            'ai_recommend': True,
            'published_date': datetime.now() - timedelta(days=1)
        },
        {
            'title': 'AI 데이터센터 전력 수요 급증... 2030년 원전 10기 필요',
            'content': '''AI 기술 발전으로 데이터센터 전력 수요가 급증하면서 
            2030년까지 원전 10기 규모의 추가 전력이 필요할 것으로 전망됐다.
            
            한국전력거래소 분석에 따르면 국내 데이터센터 전력 소비는 
            2023년 3GW에서 2030년 15GW로 5배 증가할 것으로 예상된다.''',
            'keywords': ['AI', '데이터센터', '전력수요', '원전'],
            'summary': 'AI 데이터센터 전력 수요 5배 증가 전망, 2030년까지 원전 10기 규모 필요',
            'ai_recommend': False,
            'published_date': datetime.now() - timedelta(days=2)
        }
    ]
    
    print("🚀 향상된 카드 뉴스 생성 시작...")
    
    # 1. 구조화된 콘텐츠 생성
    content_gen = StructuredContentGenerator()
    print("\n📝 구조화된 콘텐츠 생성 중...")
    
    for i, article in enumerate(test_articles):
        print(f"\n기사 {i+1}: {article['title']}")
        
        # 구조화된 요약 생성 (폴백 모드로 테스트)
        structured = content_gen._fallback_summary(article['content'])
        article['structured_summary'] = structured
        
        print(f"  핵심 주제: {structured['core_topic'][:50]}...")
        print(f"  주요 포인트: {len(structured['main_points'])}개")
        print(f"  핵심 데이터: {structured['key_data']}")
    
    # 2. 시각화 데이터 추출
    viz_data = content_gen.extract_visualization_data(test_articles)
    print(f"\n📊 시각화 데이터 추출 완료:")
    print(f"  카테고리: {list(viz_data['categories'].keys())}")
    print(f"  AI 추천 비율: {viz_data['comparisons']}")
    
    # 3. 카드 생성
    card_gen = EnhancedCardNewsGenerator()
    print("\n🎨 카드 이미지 생성 중...")
    
    # 인사이트 분석
    insights = card_gen.analyze_articles_for_insights(test_articles)
    
    # 요약 카드
    summary_card = card_gen.create_enhanced_summary_card(test_articles, insights)
    summary_card.save('card_news_v3/test_enhanced_summary.png')
    print("✅ 향상된 요약 카드 생성 완료")
    
    # 데이터 시각화 카드
    data_card = card_gen.create_data_visualization_card(test_articles)
    data_card.save('card_news_v3/test_data_visualization.png')
    print("✅ 데이터 시각화 카드 생성 완료")
    
    print("\n🎉 테스트 완료! card_news_v3 폴더에서 결과를 확인하세요.")
    
    # 개선 사항 요약
    print("\n📋 개선된 기능:")
    print("1. 구조화된 콘텐츠: 핵심 주제 + 소주제 + 데이터 포인트")
    print("2. 데이터 시각화: 트렌드 차트, 키워드 분석, AI 추천 통계")
    print("3. 인사이트 도출: 주요 트렌드와 시사점 자동 분석")
    print("4. 현대적 디자인: 그라데이션, 카드 UI, 다크 테마")

if __name__ == "__main__":
    test_enhanced_cards()
