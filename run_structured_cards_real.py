#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 구조화된 카드뉴스 실제 데이터 테스트
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
        
        # 5-1. 향상된 요약 카드
        print("\n📋 요약 카드 생성...")
        summary_card = create_enhanced_summary_card(generator, analysis)
        cards.append(('summary', summary_card))
        
        # 5-2. 카테고리 통계 카드
        if analysis['categories']:
            print("📊 카테고리 통계 카드 생성...")
            stats_card = generator.create_stats_card(all_articles)  # 기존 메서드 활용
            cards.append(('stats', stats_card))
        
        # 5-3. 트렌드 카드
        if analysis['trends']:
            print("📈 트렌드 카드 생성...")
            trend_card = create_trend_card(generator, analysis['trends'])
            cards.append(('trends', trend_card))
        
        # 5-4. 주요 기사 카드
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
            
        # 7. 노션에 결과 페이지 생성 (선택사항)
        print("\n📝 노션에 분석 결과 페이지 생성 중...")
        
        try:
            create_notion_report(generator.notion, analysis, saved_files)
            print("✅ 노션 페이지 생성 완료!")
        except Exception as e:
            print(f"⚠️ 노션 페이지 생성 실패: {str(e)}")
            
        print("\n" + "="*60)
        print("🎉 구조화된 카드뉴스 생성 완료!")
        print(f"📁 저장 위치: {output_dir}")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

def create_enhanced_summary_card(generator, analysis):
    """향상된 요약 카드 생성"""
    img = Image.new('RGB', (generator.width, generator.height), generator.colors['background'])
    draw = ImageDraw.Draw(img)
    
    # 헤더
    generator._draw_header(draw, "📊 전력산업 위클리 리포트")
    
    # 요약 정보
    y_pos = 200
    
    # 기간과 기사 수
    period_font = generator._get_font('regular', generator.font_sizes['body'])
    draw.text((80, y_pos), f"📅 {analysis['summary']['period']}", 
              font=period_font, fill=generator.colors['text'])
    y_pos += 60
    
    count_font = generator._get_font('bold', generator.font_sizes['sub_title'])
    draw.text((80, y_pos), f"총 {analysis['summary']['total_articles']}건의 주요 뉴스", 
              font=count_font, fill=generator.colors['primary'])
    y_pos += 100
    
    # 주요 테마
    theme_font = generator._get_font('regular', generator.font_sizes['body'])
    lines = generator._wrap_text(analysis['summary']['main_theme'], theme_font, generator.width - 160, draw)
    for line in lines:
        draw.text((80, y_pos), line, font=theme_font, fill=generator.colors['text'])
        y_pos += 50
    y_pos += 50
    
    # 핵심 인사이트
    draw.text((80, y_pos), "💡 핵심 인사이트", 
              font=generator._get_font('bold', generator.font_sizes['sub_title']), 
              fill=generator.colors['accent'])
    y_pos += 80
    
    insight_font = generator._get_font('regular', generator.font_sizes['body'])
    for insight in analysis['key_insights'][:4]:
        lines = generator._wrap_text(f"• {insight}", insight_font, generator.width - 160, draw)
        for line in lines:
            draw.text((100, y_pos), line, font=insight_font, fill=generator.colors['text'])
            y_pos += 50
        y_pos += 20
        
    # 통계 요약 (하단)
    stats = analysis['statistics']
    y_pos = generator.height - 250
    
    stats_text = []
    if stats['ai_recommended'] > 0:
        stats_text.append(f"🤖 AI 추천: {stats['ai_recommended']}건")
    if stats['user_interested'] > 0:
        stats_text.append(f"⭐ 관심 표시: {stats['user_interested']}건")
        
    for text in stats_text:
        draw.text((80, y_pos), text, 
                  font=period_font, fill=generator.colors['text_light'])
        y_pos += 40
    
    # 푸터
    generator._draw_footer(draw)
    
    return img

def create_trend_card(generator, trends):
    """트렌드 분석 카드 생성"""
    img = Image.new('RGB', (generator.width, generator.height), generator.colors['background'])
    draw = ImageDraw.Draw(img)
    
    # 헤더
    generator._draw_header(draw, "🔥 이번 주 핫 키워드")
    
    y_pos = 250
    
    # 상위 5개 트렌드 시각화
    max_count = trends[0]['count'] if trends else 1
    
    for i, trend in enumerate(trends[:5], 1):
        # 순위 번호
        rank_font = generator._get_font('bold', 48)
        rank_color = generator.colors['accent'] if i <= 3 else generator.colors['text_light']
        draw.text((80, y_pos), str(i), font=rank_font, fill=rank_color)
        
        # 키워드
        keyword_font = generator._get_font('bold', generator.font_sizes['article_title'])
        draw.text((150, y_pos + 5), trend['keyword'], 
                  font=keyword_font, fill=generator.colors['text'])
        
        # 막대 그래프
        bar_width = int((trend['count'] / max_count) * 600)
        bar_color = generator.colors['primary'] if i <= 3 else generator.colors['border']
        draw.rectangle([(150, y_pos + 55), (150 + bar_width, y_pos + 85)], 
                      fill=bar_color)
        
        # 카운트
        count_font = generator._get_font('regular', generator.font_sizes['body'])
        draw.text((150 + bar_width + 20, y_pos + 60), 
                  f"{trend['count']}회", 
                  font=count_font, fill=generator.colors['text_light'])
        
        y_pos += 140
    
    # 설명
    desc_font = generator._get_font('regular', generator.font_sizes['caption'])
    draw.text((80, generator.height - 200), 
              "* 키워드는 기사 제목과 내용에서 추출됨", 
              font=desc_font, fill=generator.colors['text_light'])
    
    # 푸터
    generator._draw_footer(draw)
    
    return img

def create_notion_report(notion_client, analysis, card_files):
    """노션에 분석 결과 페이지 생성"""
    
    # 페이지 내용 구성
    content = f"""# 📊 전력산업 위클리 리포트

## 📅 기간
{analysis['summary']['period']}

## 📰 요약
- **총 기사 수**: {analysis['summary']['total_articles']}건
- **주요 테마**: {analysis['summary']['main_theme']}

## 📂 카테고리별 분포
"""
    
    for category, count in analysis['categories'].items():
        content += f"- **{category}**: {count}건\n"
        
    content += "\n## 🔥 핫 키워드 TOP 5\n"
    for i, trend in enumerate(analysis['trends'][:5], 1):
        content += f"{i}. **{trend['keyword']}** - {trend['count']}회 언급\n"
        
    content += "\n## 💡 핵심 인사이트\n"
    for insight in analysis['key_insights']:
        content += f"- {insight}\n"
        
    content += "\n## 📊 통계\n"
    stats = analysis['statistics']
    content += f"- AI 추천 기사: {stats['ai_recommended']}건\n"
    content += f"- 사용자 관심 기사: {stats['user_interested']}건\n"
    content += f"- 평균 키워드 수: {stats['avg_keywords']:.1f}개\n"
    
    content += "\n## 🎨 생성된 카드뉴스\n"
    content += f"총 {len(card_files)}장의 카드가 생성되었습니다.\n\n"
    
    # 카드 파일 목록
    for filepath in card_files:
        filename = os.path.basename(filepath)
        content += f"- ✅ {filename}\n"
    
    # 노션 페이지 생성
    parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')
    
    page_data = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": f"위클리 리포트 - {datetime.now().strftime('%Y.%m.%d')}"
                        }
                    }
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": content}
                        }
                    ]
                }
            }
        ]
    }
    
    notion_client.client.pages.create(**page_data)

if __name__ == "__main__":
    main()
