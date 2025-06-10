#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카드 뉴스 생성기 테스트
"""

import sys
import os

# 프로젝트 경로 추가
sys.path.append('/home/zwtiger/AI-Agent-Full-Stack-Developer')

from card_news_generator import CardNewsGenerator

def test_card_creation():
    """카드 생성 테스트"""
    print("🧪 카드 뉴스 생성 테스트 시작...")
    
    # 테스트용 기사 데이터
    test_articles = [
        {
            'title': '태양광 발전 효율 30% 향상 신기술 개발',
            'summary': '한국에너지기술연구원이 페로브스카이트 태양전지 효율을 30%까지 끌어올리는 신기술을 개발했다.',
            'key_points': '* 페로브스카이트 태양전지 효율 30% 달성\n* 기존 실리콘 대비 제조비용 50% 절감\n* 2025년 상용화 목표',
            'keywords': ['태양광', '재생에너지', '기술개발'],
            'source': '전기신문'
        },
        {
            'title': 'ESS 화재 안전기준 대폭 강화',
            'summary': '정부가 ESS 화재 예방을 위해 배터리 간격 확대 등 새로운 안전기준을 발표했다.',
            'key_points': '* 배터리 모듈 간격 기존 10cm에서 30cm로 확대\n* 열감지 센서 의무화\n* 자동 소화설비 설치 의무화',
            'keywords': ['ESS', '안전', '정책'],
            'source': '전기신문'
        }
    ]
    
    try:
        # 생성기 초기화
        generator = CardNewsGenerator()
        
        # 요약 카드 생성
        print("📄 요약 카드 생성 중...")
        summary_card = generator.create_summary_card(test_articles)
        summary_card.save('test_summary_card.png')
        print("✅ 요약 카드 저장 완료: test_summary_card.png")
        
        # 개별 기사 카드 생성
        print("📄 개별 기사 카드 생성 중...")
        article_card = generator.create_article_card(test_articles[0], card_number=1)
        article_card.save('test_article_card.png')
        print("✅ 기사 카드 저장 완료: test_article_card.png")
        
        # 통계 카드 생성
        print("📊 통계 카드 생성 중...")
        stats_card = generator.create_statistics_card(test_articles)
        stats_card.save('test_stats_card.png')
        print("✅ 통계 카드 저장 완료: test_stats_card.png")
        
        print("🎉 테스트 완료! 생성된 이미지를 확인하세요.")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_card_creation()
