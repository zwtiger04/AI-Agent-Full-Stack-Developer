#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 구조화된 카드 뉴스 테스트
"""

import sys
sys.path.append('.')

# 필요한 import 추가
from PIL import Image, ImageDraw, ImageFont
import os

# 기존 v2 코드에서 필요한 부분 복사
exec(open('card_news_generator_v2.py').read())

# 구조화된 콘텐츠 생성기 import
from structured_content_generator import StructuredContentGenerator

def test_structured_card_news():
    """구조화된 카드 뉴스 생성 테스트"""
    
    print("🧪 구조화된 카드 뉴스 테스트 시작...")
    
    # 1. 생성기 초기화
    generator = CardNewsGeneratorV2()
    generator.content_generator = StructuredContentGenerator()
    
    # 2. 노션에서 데이터 가져오기 시뮬레이션
    # 실제로는 generator.notion.get_all_articles_from_db()를 사용
    sample_articles = [
        {
            'page_id': '1',
            'title': '한전, 태양광 발전 효율 20% 향상 신기술 개발',
            'summary': '한국전력공사가 차세대 태양광 패널 기술을 개발하여 발전 효율을 크게 개선했다고 발표',
            'keywords': ['태양광', '한전', '신기술', '효율성'],
            'ai_recommend': True,
            'interest': False,
            'published_date': '2025-06-05',
            'source': '전기신문',
            'key_points': '• 기존 대비 20% 효율 향상\n• 2026년 상용화 목표\n• 연간 1조원 시장 예상'
        },
        {
            'page_id': '2',
            'title': 'ESS 화재 안전 기준 대폭 강화, 새로운 규제 시행',
            'summary': '정부가 ESS 설치 및 운영에 대한 안전 규정을 대폭 강화하는 새로운 정책을 발표',
            'keywords': ['ESS', '안전', '정책', '규제'],
            'ai_recommend': False,
            'interest': True,
            'published_date': '2025-06-04',
            'source': '에너지신문',
            'key_points': '• 화재 감지 시스템 의무화\n• 월 1회 안전 점검 필수\n• 위반 시 과태료 부과'
        },
        {
            'page_id': '3',
            'title': 'VPP 시장 본격 개방, 소규모 사업자 참여 확대',
            'summary': '가상발전소(VPP) 시장이 소규모 사업자에게도 개방되어 시장 활성화가 기대됨',
            'keywords': ['VPP', '전력시장', '분산자원'],
            'ai_recommend': True,
            'interest': False,
            'published_date': '2025-06-03',
            'source': '전력경제',
            'key_points': '• 100kW 이상 참여 가능\n• 수익 배분 체계 개선\n• 2025년 하반기 시행'
        }
    ]
    
    # 3. 구조화된 분석 수행
    print("\n📊 기사 분석 중...")
    analysis = generator.content_generator.analyze_articles(sample_articles)
    
    # 4. 분석 결과 출력
    print("\n📈 분석 결과:")
    print(f"  - 총 기사 수: {analysis['summary']['total_articles']}")
    print(f"  - 기간: {analysis['summary']['period']}")
    print(f"  - 주요 테마: {analysis['summary']['main_theme']}")
    print(f"  - 카테고리: {analysis['categories']}")
    print(f"  - 트렌드: {[t['keyword'] for t in analysis['trends'][:3]]}")
    print(f"  - 인사이트: {analysis['key_insights']}")
    
    # 5. 간단한 요약 카드 생성 테스트
    print("\n🎨 요약 카드 생성 테스트...")
    
    # 카드 생성을 위한 간단한 메서드
    def create_test_summary_card(analysis):
        img = Image.new('RGB', (generator.width, generator.height), generator.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # 제목
        title_font = generator._get_font('bold', generator.font_sizes['main_title'])
        draw.text((80, 80), "📊 전력산업 위클리", font=title_font, fill=generator.colors['primary'])
        
        # 요약 정보
        y_pos = 200
        body_font = generator._get_font('regular', generator.font_sizes['body'])
        
        summary_text = f"""
📅 기간: {analysis['summary']['period']}
📰 총 기사: {analysis['summary']['total_articles']}건
🎯 주요 테마: {analysis['summary']['main_theme']}

💡 핵심 인사이트:
"""
        
        for line in summary_text.strip().split('\n'):
            draw.text((80, y_pos), line, font=body_font, fill=generator.colors['text'])
            y_pos += 50
            
        # 인사이트 추가
        for insight in analysis['key_insights'][:3]:
            draw.text((100, y_pos), f"• {insight}", font=body_font, fill=generator.colors['text'])
            y_pos += 50
            
        return img
    
    # 카드 생성
    summary_card = create_test_summary_card(analysis)
    
    # 6. 카드 저장
    output_path = "test_structured_summary_card.png"
    summary_card.save(output_path)
    print(f"\n✅ 테스트 카드 저장됨: {output_path}")
    
    # 7. 카테고리 통계 시각화 테스트
    print("\n📊 카테고리 통계 시각화...")
    import matplotlib.pyplot as plt
    
    # 카테고리별 기사 수 차트
    categories = list(analysis['categories'].keys())
    counts = list(analysis['categories'].values())
    
    plt.figure(figsize=(8, 6))
    plt.bar(categories, counts, color=['#F59E0B', '#3B82F6', '#8B5CF6', '#10B981'])
    plt.title('카테고리별 기사 분포', fontsize=16, pad=20)
    plt.xlabel('카테고리', fontsize=12)
    plt.ylabel('기사 수', fontsize=12)
    plt.tight_layout()
    plt.savefig('test_category_stats.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✅ 카테고리 통계 차트 저장됨: test_category_stats.png")
    
    print("\n🎉 구조화된 카드 뉴스 테스트 완료!")
    print("\n💡 다음 단계:")
    print("  1. 실제 노션 데이터와 연동")
    print("  2. 더 많은 카드 타입 추가 (트렌드, 상세 기사 등)")
    print("  3. 시각화 개선 (차트, 그래프 등)")

if __name__ == "__main__":
    test_structured_card_news()
