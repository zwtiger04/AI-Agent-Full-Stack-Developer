#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 카드 뉴스 생성기 V2 개선 패치
- 구조화된 콘텐츠 생성 통합
- 전체 기사 분석 기능 추가
"""

import sys
import os

# 기존 import 유지하면서 새로운 모듈 추가
from structured_content_generator import StructuredContentGenerator

def patch_card_news_generator():
    """기존 CardNewsGeneratorV2에 새로운 메서드 추가"""
    
    # 파일 읽기
    with open('card_news_generator_v2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # import 섹션에 구조화된 콘텐츠 생성기 추가
    import_section = """from notion.notion_client import NotionClient
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import json
from structured_content_generator import StructuredContentGenerator"""
    
    content = content.replace(
        """from notion.notion_client import NotionClient
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import json""",
        import_section
    )
    
    # __init__ 메서드에 구조화된 콘텐츠 생성기 추가
    init_addition = """        
        self.notion = NotionClient()
        self.content_generator = StructuredContentGenerator()"""
    
    content = content.replace(
        """        self.notion = NotionClient()""",
        init_addition
    )
    
    # 새로운 메서드 추가 (generate_card_news 메서드 앞에)
    new_methods = """
    def generate_structured_card_news(self):
        \"\"\"구조화된 콘텐츠를 활용한 카드뉴스 생성\"\"\"
        print("🚀 구조화된 카드뉴스 생성 시작...")
        
        try:
            # 1. 이번 주 전체 기사 가져오기
            print("📰 이번 주 전체 기사 가져오는 중...")
            database_id = self.notion.get_weekly_database_id()
            all_articles = self.notion.get_all_articles_from_db(database_id)
            
            if not all_articles:
                print("⚠️ 이번 주 기사가 없습니다.")
                return None
                
            print(f"✅ 총 {len(all_articles)}개 기사 발견")
            
            # 2. 구조화된 분석 수행
            print("📊 기사 분석 중...")
            analysis = self.content_generator.analyze_articles(all_articles)
            
            print(f"  - 카테고리: {list(analysis['categories'].keys())}")
            print(f"  - 트렌드: {len(analysis['trends'])}개 발견")
            print(f"  - 인사이트: {len(analysis['key_insights'])}개 추출")
            
            # 3. 카드 생성
            cards = []
            
            # 3-1. 요약 카드 (구조화된 데이터 활용)
            print("🎨 요약 카드 생성 중...")
            summary_card = self._create_enhanced_summary_card(analysis)
            cards.append(('summary', summary_card))
            
            # 3-2. 카테고리별 통계 카드
            print("📊 통계 카드 생성 중...")
            stats_card = self._create_category_stats_card(analysis['categories'])
            cards.append(('stats', stats_card))
            
            # 3-3. 주요 기사 카드들
            print("📰 주요 기사 카드 생성 중...")
            for i, article in enumerate(analysis['top_articles'], 1):
                article_card = self.create_article_card(article, i)
                cards.append((f'article_{i}', article_card))
                
            # 3-4. 트렌드 카드
            if analysis['trends']:
                print("📈 트렌드 카드 생성 중...")
                trend_card = self._create_trend_card(analysis['trends'])
                cards.append(('trends', trend_card))
            
            print(f"✅ 총 {len(cards)}장의 카드 생성 완료!")
            return cards
            
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_enhanced_summary_card(self, analysis):
        \"\"\"향상된 요약 카드 생성\"\"\"
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # 헤더
        self._draw_header(draw, "📊 이번 주 전력산업 동향")
        
        # 요약 정보
        summary = analysis['summary']
        y_pos = 200
        
        # 기간
        period_font = self._get_font('regular', self.font_sizes['body'])
        draw.text((80, y_pos), f"📅 {summary['period']}", 
                  font=period_font, fill=self.colors['text'])
        y_pos += 60
        
        # 전체 기사 수
        count_font = self._get_font('bold', self.font_sizes['sub_title'])
        draw.text((80, y_pos), f"총 {summary['total_articles']}건의 주요 뉴스", 
                  font=count_font, fill=self.colors['primary'])
        y_pos += 100
        
        # 주요 테마
        theme_font = self._get_font('regular', self.font_sizes['body'])
        draw.text((80, y_pos), summary['main_theme'], 
                  font=theme_font, fill=self.colors['text'])
        y_pos += 100
        
        # 핵심 인사이트
        draw.text((80, y_pos), "💡 핵심 인사이트", 
                  font=self._get_font('bold', self.font_sizes['sub_title']), 
                  fill=self.colors['accent'])
        y_pos += 80
        
        insight_font = self._get_font('regular', self.font_sizes['body'])
        for insight in analysis['key_insights'][:3]:
            lines = self._wrap_text(insight, insight_font, self.width - 160, draw)
            for line in lines:
                draw.text((100, y_pos), line, font=insight_font, fill=self.colors['text'])
                y_pos += 50
            y_pos += 20
            
        # 통계 요약
        stats = analysis['statistics']
        y_pos = self.height - 300
        
        # AI 추천 비율
        if stats['total'] > 0:
            ai_ratio = stats['ai_recommended'] / stats['total'] * 100
            draw.text((80, y_pos), 
                      f"🤖 AI 추천: {stats['ai_recommended']}건 ({ai_ratio:.0f}%)", 
                      font=period_font, fill=self.colors['secondary'])
            
        # 푸터
        self._draw_footer(draw)
        
        return img
    
    def _create_trend_card(self, trends):
        \"\"\"트렌드 분석 카드 생성\"\"\"
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # 헤더
        self._draw_header(draw, "📈 이번 주 핫 키워드")
        
        y_pos = 200
        
        # 트렌드 시각화
        for i, trend in enumerate(trends[:5], 1):
            # 순위
            rank_font = self._get_font('bold', self.font_sizes['sub_title'])
            draw.text((80, y_pos), f"{i}", 
                      font=rank_font, fill=self.colors['accent'])
            
            # 키워드
            keyword_font = self._get_font('bold', self.font_sizes['article_title'])
            draw.text((150, y_pos), trend['keyword'], 
                      font=keyword_font, fill=self.colors['primary'])
            
            # 언급 횟수 바
            bar_width = int((trend['count'] / trends[0]['count']) * 600)
            draw.rectangle([(150, y_pos + 50), (150 + bar_width, y_pos + 80)], 
                          fill=self.colors['secondary'])
            
            # 횟수 텍스트
            count_font = self._get_font('regular', self.font_sizes['body'])
            draw.text((150 + bar_width + 20, y_pos + 55), 
                      f"{trend['count']}건", 
                      font=count_font, fill=self.colors['text_light'])
            
            y_pos += 120
            
        # 푸터
        self._draw_footer(draw)
        
        return img
    
"""
    
    # generate_card_news 메서드 찾기
    method_start = content.find("    def generate_card_news(self):")
    if method_start > 0:
        # 메서드 앞에 새로운 메서드들 삽입
        content = content[:method_start] + new_methods + content[method_start:]
    
    # 파일 저장
    with open('card_news_generator_v2_enhanced.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 패치 완료! card_news_generator_v2_enhanced.py 생성됨")

if __name__ == "__main__":
    patch_card_news_generator()
