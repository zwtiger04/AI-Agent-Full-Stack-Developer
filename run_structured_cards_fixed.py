#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 구조화된 카드뉴스 실제 데이터 테스트 (수정판)
"""

import sys
import os
from datetime import datetime
from PIL import Image, ImageDraw

# 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 필요한 모듈 import
from card_news_generator_v2 import CardNewsGeneratorV2
from structured_content_generator import StructuredContentGenerator
from notion.notion_client import NotionClient

def main():
    """메인 실행 함수"""
    print("🚀 구조화된 카드뉴스 생성 (실제 데이터)")
    print("=" * 60)
    
    try:
        # 1. 생성기 초기화
        print("📌 생성기 초기화 중...")
        generator = CardNewsGeneratorV2()
        generator.content_generator = StructuredContentGenerator()
        
        # 2. 노션에서 이번 주 데이터 가져오기
        print("\n📊 노션에서 이번 주 데이터 가져오는 중...")
        database_id = generator.notion.get_weekly_database_id()
        
        if not database_id:
            print("❌ 데이터베이스를 찾을 수 없습니다.")
            return
            
        all_articles = generator.notion.get_all_articles_from_db(database_id)
        
        if not all_articles:
            print("❌ 이번 주 기사가 없습니다.")
            return
            
        print(f"✅ 총 {len(all_articles)}개 기사 발견")
        
        # 3. 구조화된 분석 수행
        print("\n📈 구조화된 분석 수행 중...")
        analysis = generator.content_generator.analyze_articles(all_articles)
        
        # 4. 분석 결과 출력
        print("\n" + "="*60)
        print("📊 분석 결과")
        print("="*60)
        
        print(f"\n📅 기간: {analysis['summary']['period']}")
        print(f"📰 총 기사 수: {analysis['summary']['total_articles']}건")
        print(f"🎯 주요 테마: {analysis['summary']['main_theme']}")
        
        print("\n📂 카테고리별 분포:")
        for category, count in analysis['categories'].items():
            print(f"  - {category}: {count}건")
            
        print("\n🔥 핫 키워드 TOP 5:")
        for i, trend in enumerate(analysis['trends'][:5], 1):
            print(f"  {i}. {trend['keyword']} ({trend['count']}회)")
            
        print("\n💡 핵심 인사이트:")
        for insight in analysis['key_insights']:
            print(f"  • {insight}")
            
        print("\n📊 통계:")
        stats = analysis['statistics']
        print(f"  - AI 추천: {stats['ai_recommended']}건")
        print(f"  - 사용자 관심: {stats['user_interested']}건")
        print(f"  - 평균 키워드 수: {stats['avg_keywords']:.1f}개")
        
        print("\n🏆 주요 기사 TOP 3:")
        for i, article in enumerate(analysis['top_articles'][:3], 1):
            print(f"\n  [{i}] {article['title']}")
            print(f"      📝 {article.get('summary', 'N/A')[:100]}...")
            if article.get('interest'):
                print("      ⭐ 사용자 관심")
            if article.get('ai_recommend'):
                print("      🤖 AI 추천")
                
        # 5. 카드 생성
        print("\n" + "="*60)
        print("🎨 카드 생성 중...")
        print("="*60)
        
        cards = []
        
        # 5-1. 기존 요약 카드 스타일로 구조화된 데이터 표시
        print("\n📋 요약 카드 생성...")
        # 관심 기사만 필터링 (기존 v2 스타일 유지)
        interested_articles = [a for a in all_articles if a.get('interest', False)]
        if interested_articles:
            summary_card = generator.create_summary_card(interested_articles[:5])
        else:
            # 관심 기사가 없으면 상위 5개 기사로 대체
            summary_card = generator.create_summary_card(analysis['top_articles'][:5])
        cards.append(('summary', summary_card))
        
        # 5-2. 통계 카드 (구조화된 데이터 활용)
        print("📊 통계 카드 생성...")
        stats_card = create_structured_stats_card(generator, analysis)
        cards.append(('stats', stats_card))
        
        # 5-3. 트렌드 카드
        if analysis['trends']:
            print("📈 트렌드 카드 생성...")
            trend_card = create_trend_card(generator, analysis['trends'])
            cards.append(('trends', trend_card))
        
        # 5-4. 주요 기사 카드 (상위 3개)
        for i, article in enumerate(analysis['top_articles'][:3], 1):
            print(f"📰 주요 기사 카드 {i} 생성...")
            article_card = generator.create_article_card(article, i)
            cards.append((f'article_{i}', article_card))
            
        # 6. 카드 저장
        print(f"\n💾 총 {len(cards)}장의 카드 저장 중...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(os.getcwd(), 'structured_cards_output')
        os.makedirs(output_dir, exist_ok=True)
        
        saved_files = []
        for card_type, card_img in cards:
            filename = f"{timestamp}_{card_type}.png"
            filepath = os.path.join(output_dir, filename)
            card_img.save(filepath)
            saved_files.append(filepath)
            print(f"  ✅ {filename}")
            
        # 7. 메타데이터 저장
        metadata = {
            'timestamp': timestamp,
            'total_articles': len(all_articles),
            'analysis': {
                'period': analysis['summary']['period'],
                'main_theme': analysis['summary']['main_theme'],
                'categories': analysis['categories'],
                'top_keywords': [t['keyword'] for t in analysis['trends'][:5]],
                'insights': analysis['key_insights']
            },
            'cards_generated': len(cards)
        }
        
        import json
        metadata_file = os.path.join(output_dir, f"{timestamp}_metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"\n📄 메타데이터 저장: {os.path.basename(metadata_file)}")
            
        print("\n" + "="*60)
        print("🎉 구조화된 카드뉴스 생성 완료!")
        print(f"📁 저장 위치: {output_dir}")
        print("="*60)
        
        # 8. 노션 업로드 옵션
        print("\n📤 노션에 업로드하시겠습니까?")
        print("(이 기능은 아직 구현되지 않았습니다)")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

def create_structured_stats_card(generator, analysis):
    """구조화된 통계 카드 생성"""
    img = Image.new('RGB', (generator.width, generator.height), generator.colors['background'])
    draw = ImageDraw.Draw(img)
    
    # 배경 그라데이션
    for y in range(generator.height):
        ratio = y / generator.height
        r = int(245 * (1 - ratio * 0.1))
        g = int(245 * (1 - ratio * 0.1))
        b = int(250 * (1 - ratio * 0.1))
        draw.rectangle([(0, y), (generator.width, y+1)], fill=f'#{r:02x}{g:02x}{b:02x}')
    
    # 제목
    title_font = generator._get_font('bold', generator.font_sizes['main_title'])
    draw.text((80, 80), "📊 이번 주 전력산업 통계", 
              font=title_font, fill=generator.colors['primary'])
    
    # 기간
    period_font = generator._get_font('regular', generator.font_sizes['body'])
    draw.text((80, 160), f"📅 {analysis['summary']['period']}", 
              font=period_font, fill=generator.colors['text_light'])
    
    # 카테고리별 분포
    y_pos = 250
    subtitle_font = generator._get_font('bold', generator.font_sizes['sub_title'])
    draw.text((80, y_pos), "카테고리별 기사 분포", 
              font=subtitle_font, fill=generator.colors['text'])
    y_pos += 80
    
    # 카테고리 막대 그래프
    categories = list(analysis['categories'].items())[:5]  # 상위 5개만
    if categories:
        max_count = max(count for _, count in categories)
        
        for category, count in categories:
            # 카테고리명
            cat_font = generator._get_font('regular', generator.font_sizes['body'])
            draw.text((100, y_pos), category, font=cat_font, fill=generator.colors['text'])
            
            # 막대
            bar_width = int((count / max_count) * 600)
            color = generator.category_colors.get(category, generator.colors['primary'])
            draw.rectangle([(250, y_pos), (250 + bar_width, y_pos + 30)], fill=color)
            
            # 수치
            draw.text((250 + bar_width + 20, y_pos + 5), f"{count}건", 
                     font=cat_font, fill=generator.colors['text_light'])
            
            y_pos += 60
    
    # 핵심 인사이트
    y_pos += 50
    draw.text((80, y_pos), "💡 핵심 인사이트", 
              font=subtitle_font, fill=generator.colors['accent'])
    y_pos += 60
    
    insight_font = generator._get_font('regular', generator.font_sizes['caption'])
    for insight in analysis['key_insights'][:3]:
        lines = generator._wrap_text(insight, insight_font, generator.width - 160, draw)
        for line in lines:
            draw.text((100, y_pos), line, font=insight_font, fill=generator.colors['text'])
            y_pos += 40
        y_pos += 20
    
    # 하단 통계
    bottom_y = generator.height - 200
    stats = analysis['statistics']
    stats_text = f"총 {stats['total']}건 | AI 추천 {stats['ai_recommended']}건 | 관심 표시 {stats['user_interested']}건"
    draw.text((80, bottom_y), stats_text, 
              font=period_font, fill=generator.colors['text_light'])
    
    # 푸터
    footer_font = generator._get_font('regular', generator.font_sizes['small'])
    draw.text((80, generator.height - 80), 
              "Powered by AI 전력산업 뉴스 분석 시스템", 
              font=footer_font, fill=generator.colors['text_light'])
    
    return img

def create_trend_card(generator, trends):
    """트렌드 분석 카드 생성"""
    img = Image.new('RGB', (generator.width, generator.height), generator.colors['background'])
    draw = ImageDraw.Draw(img)
    
    # 제목
    title_font = generator._get_font('bold', generator.font_sizes['main_title'])
    draw.text((80, 80), "🔥 이번 주 핫 키워드", 
              font=title_font, fill=generator.colors['accent'])
    
    # 부제목
    subtitle_font = generator._get_font('regular', generator.font_sizes['body'])
    draw.text((80, 160), "기사에서 가장 많이 언급된 키워드", 
              font=subtitle_font, fill=generator.colors['text_light'])
    
    y_pos = 280
    
    # 상위 5개 트렌드
    for i, trend in enumerate(trends[:5], 1):
        # 순위
        rank_font = generator._get_font('bold', 60)
        rank_color = generator.colors['accent'] if i <= 3 else generator.colors['text_light']
        draw.text((80, y_pos), str(i), font=rank_font, fill=rank_color)
        
        # 키워드
        keyword_font = generator._get_font('bold', generator.font_sizes['article_title'])
        draw.text((180, y_pos + 10), trend['keyword'], 
                  font=keyword_font, fill=generator.colors['text'])
        
        # 언급 횟수
        count_font = generator._get_font('regular', generator.font_sizes['body'])
        count_text = f"{trend['count']}회 언급"
        # 텍스트 크기 계산
        bbox = draw.textbbox((0, 0), count_text, font=count_font)
        text_width = bbox[2] - bbox[0]
        draw.text((generator.width - text_width - 100, y_pos + 15), 
                  count_text, font=count_font, fill=generator.colors['primary'])
        
        # 구분선
        if i < 5:
            draw.line([(100, y_pos + 80), (generator.width - 100, y_pos + 80)], 
                     fill=generator.colors['border'], width=1)
        
        y_pos += 100
    
    # 설명
    desc_font = generator._get_font('regular', generator.font_sizes['caption'])
    draw.text((80, generator.height - 150), 
              "* 키워드는 기사 제목, 요약, 본문에서 추출", 
              font=desc_font, fill=generator.colors['text_light'])
    
    return img

if __name__ == "__main__":
    main()
