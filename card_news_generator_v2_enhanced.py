#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전력산업 카드뉴스 생성기 V2 - 한글 지원 + 자동 업로드
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime
import io
import base64
import requests
from notion.notion_client import NotionClient
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import json
from structured_content_generator import StructuredContentGenerator

# 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 한글 폰트 설정 (D2Coding 사용)
FONT_REGULAR = os.path.expanduser('~/.fonts/D2Coding-Ver1.3.2-20180524.ttf')
FONT_BOLD = os.path.expanduser('~/.fonts/D2CodingBold-Ver1.3.2-20180524.ttf')

# matplotlib 한글 폰트 설정
font_path = FONT_REGULAR
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

class CardNewsGeneratorV2:
    def __init__(self):
        """카드 뉴스 생성기 초기화"""
        self.width = 1080
        self.height = 1080
        
        # 색상 팔레트
        self.colors = {
            'background': '#FFFFFF',
            'primary': '#2563EB',
            'secondary': '#10B981',  
            'accent': '#F59E0B',
            'danger': '#EF4444',
            'text': '#1F2937',
            'text_light': '#6B7280',
            'border': '#E5E7EB',
            'gradient_start': '#2563EB',
            'gradient_end': '#10B981'
        }
        
        self.category_colors = {
            '태양광': '#F59E0B',
            'ESS': '#3B82F6',
            '전력망': '#8B5CF6',
            '재생에너지': '#10B981',
            'VPP': '#EC4899',
            '정책': '#6B7280',
            '기타': '#1F2937'
        }
        
        self.font_sizes = {
            'main_title': 48,
            'sub_title': 36,
            'article_title': 32,
            'body': 24,
            'caption': 20,
            'small': 18
        }
        
        
        self.notion = NotionClient()
        self.content_generator = StructuredContentGenerator()
        
    def _get_font(self, font_type='regular', size=24):
        """한글 폰트 로드"""
        font_path = FONT_BOLD if font_type == 'bold' else FONT_REGULAR
        try:
            return ImageFont.truetype(font_path, size)
        except Exception as e:
            print(f"❌ 폰트 로드 실패: {e}")
            return ImageFont.load_default()
    
    def _wrap_text(self, text, font, max_width, draw=None):
        """한글 텍스트 줄바꿈 처리"""
        if not draw:
            img = Image.new('RGB', (1, 1))
            draw = ImageDraw.Draw(img)
            
        lines = []
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            if not paragraph:
                lines.append('')
                continue
                
            words = list(paragraph)  # 한글은 글자 단위로 분리
            current_line = ''
            
            for char in words:
                test_line = current_line + char
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = char
            
            if current_line:
                lines.append(current_line)
        
        return lines
    
    def upload_to_imgur(self, image):
        """이미지를 Imgur에 업로드하고 URL 반환"""
        # Imgur Client ID (익명 업로드용)
        CLIENT_ID = "20a5a9cf0715571"  # 공개 Client ID
        
        # 이미지를 bytes로 변환
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_data = img_buffer.getvalue()
        
        # base64 인코딩
        b64_image = base64.b64encode(img_data).decode()
        
        # Imgur API 호출
        headers = {'Authorization': f'Client-ID {CLIENT_ID}'}
        data = {'image': b64_image, 'type': 'base64'}
        
        try:
            response = requests.post('https://api.imgur.com/3/image', headers=headers, data=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['link']
            else:
                print(f"❌ Imgur 업로드 실패: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Imgur 업로드 오류: {e}")
            return None
    
    def create_summary_card(self, articles):
        """주간 요약 카드 생성 (한글 지원)"""
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # 헤더 그라데이션
        for y in range(200):
            ratio = y / 200
            r = int(37 * (1 - ratio) + 16 * ratio)
            g = int(99 * (1 - ratio) + 185 * ratio)
            b = int(235 * (1 - ratio) + 129 * ratio)
            draw.rectangle([(0, y), (self.width, y+1)], fill=f'#{r:02x}{g:02x}{b:02x}')
        
        # 제목
        title_font = self._get_font('bold', self.font_sizes['main_title'])
        title_text = "📊 전력산업 주간 뉴스"
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        x = (self.width - (bbox[2] - bbox[0])) // 2
        draw.text((x, 50), title_text, font=title_font, fill='#FFFFFF')
        
        # 날짜
        now = datetime.now()
        subtitle_font = self._get_font('regular', self.font_sizes['sub_title'])
        subtitle_text = f"{now.year}년 {now.isocalendar()[1]}주차"
        bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        x = (self.width - (bbox[2] - bbox[0])) // 2
        draw.text((x, 120), subtitle_text, font=subtitle_font, fill='#FFFFFF')
        
        # TOP 3 기사
        y_pos = 250
        section_font = self._get_font('bold', self.font_sizes['article_title'])
        draw.text((80, y_pos), "🏆 이번 주 TOP 3", font=section_font, fill=self.colors['primary'])
        y_pos += 60
        
        article_font = self._get_font('regular', self.font_sizes['body'])
        medals = ['🥇', '🥈', '🥉']
        
        for i, article in enumerate(articles[:3]):
            if i >= len(medals):
                break
            
            medal = medals[i]
            title = article.get('title', '')
            
            # 제목이 너무 길면 줄임
            if len(title) > 35:
                title = title[:35] + '...'
            
            category = self._get_category_from_keywords(article.get('keywords', []))
            color = self.category_colors.get(category, self.colors['text'])
            
            draw.text((80, y_pos), medal, font=article_font, fill=self.colors['text'])
            draw.text((130, y_pos), title, font=article_font, fill=color)
            y_pos += 50
        
        # 카테고리 통계
        y_pos += 50
        draw.text((80, y_pos), "📈 카테고리별 관심 기사", font=section_font, fill=self.colors['primary'])
        y_pos += 60
        
        # 카테고리별 카운트
        category_counts = {}
        for article in articles:
            category = self._get_category_from_keywords(article.get('keywords', []))
            category_counts[category] = category_counts.get(category, 0) + 1
        
        stat_font = self._get_font('regular', self.font_sizes['caption'])
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            color = self.category_colors.get(category, self.colors['text'])
            
            # 카테고리 박스
            draw.rounded_rectangle([(80, y_pos), (200, y_pos + 40)], radius=20, fill=color)
            
            # 텍스트
            text = f"{category} ({count})"
            bbox = draw.textbbox((0, 0), text, font=stat_font)
            text_x = 140 - (bbox[2] - bbox[0]) // 2
            text_y = y_pos + 10
            draw.text((text_x, text_y), text, font=stat_font, fill='#FFFFFF')
            
            y_pos += 50
        
        # 푸터
        footer_font = self._get_font('regular', self.font_sizes['small'])
        footer_text = "AI 전력산업 뉴스 크롤러"
        bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
        x = (self.width - (bbox[2] - bbox[0])) // 2
        draw.text((x, self.height - 50), footer_text, font=footer_font, fill=self.colors['text_light'])
        
        return img
    
    def create_article_card(self, article, card_number=1):
        """개별 기사 카드 생성 (한글 지원)"""
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # 카테고리 색상
        category = self._get_category_from_keywords(article.get('keywords', []))
        category_color = self.category_colors.get(category, self.colors['primary'])
        
        # 상단 바
        draw.rectangle([(0, 0), (self.width, 100)], fill=category_color)
        
        # 카드 번호
        number_font = self._get_font('bold', 60)
        draw.text((50, 20), str(card_number), font=number_font, fill='#FFFFFF')
        
        # 카테고리
        cat_font = self._get_font('regular', self.font_sizes['body'])
        draw.text((150, 40), category, font=cat_font, fill='#FFFFFF')
        
        # 제목
        title_font = self._get_font('bold', self.font_sizes['article_title'])
        title = article.get('title', '')
        title_lines = self._wrap_text(title, title_font, self.width - 160, draw)
        
        y_pos = 150
        for line in title_lines[:3]:
            draw.text((80, y_pos), line, font=title_font, fill=self.colors['text'])
            y_pos += 40
        
        # 구분선
        y_pos += 20
        draw.line([(80, y_pos), (self.width - 80, y_pos)], fill=self.colors['border'], width=2)
        y_pos += 30
        
        # 한줄요약
        summary_font = self._get_font('regular', self.font_sizes['body'])
        summary = article.get('summary', '')
        
        draw.text((80, y_pos), "💡 핵심 요약", font=self._get_font('bold', self.font_sizes['body']), fill=category_color)
        y_pos += 40
        
        summary_lines = self._wrap_text(summary, summary_font, self.width - 160, draw)
        for line in summary_lines[:3]:
            draw.text((80, y_pos), line, font=summary_font, fill=self.colors['text'])
            y_pos += 35
        
        # 키워드 태그
        if article.get('keywords'):
            y_pos = self.height - 150
            tag_font = self._get_font('regular', self.font_sizes['small'])
            
            x_pos = 80
            for keyword in article.get('keywords', [])[:5]:
                tag_text = f"#{keyword}"
                bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
                tag_width = bbox[2] - bbox[0] + 20
                
                if x_pos + tag_width > self.width - 80:
                    break
                
                draw.rounded_rectangle([(x_pos, y_pos), (x_pos + tag_width, y_pos + 30)], 
                                     radius=15, outline=category_color, width=2)
                draw.text((x_pos + 10, y_pos + 5), tag_text, font=tag_font, fill=category_color)
                x_pos += tag_width + 10
        
        # 출처와 날짜
        footer_font = self._get_font('regular', self.font_sizes['small'])
        footer_text = f"출처: {article.get('source', '전기신문')} | {datetime.now().strftime('%Y.%m.%d')}"
        bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
        x = (self.width - (bbox[2] - bbox[0])) // 2
        draw.text((x, self.height - 50), footer_text, font=footer_font, fill=self.colors['text_light'])
        
        return img
    
    def _get_category_from_keywords(self, keywords):
        """키워드에서 카테고리 추출"""
        if not keywords:
            return '기타'
        
        priority_categories = ['태양광', 'ESS', '재생에너지', 'VPP', '전력망']
        for category in priority_categories:
            if category in keywords:
                return category
        
        return '정책'
    
    def create_statistics_card(self, articles):
        """통계 카드 생성"""
        # 카테고리별 통계
        category_counts = {}
        for article in articles:
            category = self._get_category_from_keywords(article.get('keywords', []))
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # matplotlib 차트 생성
        fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
        
        categories = list(category_counts.keys())
        values = list(category_counts.values())
        colors_list = [self.category_colors.get(cat, '#1F2937') for cat in categories]
        
        # 파이 차트
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=categories,
            colors=colors_list,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontproperties': font_prop, 'fontsize': 14}
        )
        
        ax.set_title('카테고리별 관심 기사 분포', fontproperties=font_prop, fontsize=20, pad=20)
        
        # 이미지로 변환
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=135, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close()
        
        # PIL 이미지로 변환
        chart_img = Image.open(buf)
        
        # 카드 크기에 맞게 조정
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        
        # 차트 이미지 중앙에 배치
        chart_width, chart_height = chart_img.size
        if chart_width > self.width or chart_height > self.height:
            chart_img.thumbnail((self.width - 100, self.height - 100), Image.Resampling.LANCZOS)
            chart_width, chart_height = chart_img.size
        
        x = (self.width - chart_width) // 2
        y = (self.height - chart_height) // 2
        img.paste(chart_img, (x, y))
        
        # 추가 정보
        draw = ImageDraw.Draw(img)
        stat_font = self._get_font('regular', self.font_sizes['body'])
        total_text = f"총 {len(articles)}개 기사 분석"
        bbox = draw.textbbox((0, 0), total_text, font=stat_font)
        x = (self.width - (bbox[2] - bbox[0])) // 2
        draw.text((x, self.height - 50), total_text, font=stat_font, fill=self.colors['text'])
        
        return img
    
    def save_cards_to_notion_auto(self, cards, page_title="주간 전력산업 카드뉴스"):
        """카드를 Imgur에 업로드하고 노션에 자동 추가"""
        try:
            print("🚀 자동 업로드 시작...")
            
            # 1. 이미지들을 Imgur에 업로드
            uploaded_images = []
            for card_name, card_img in cards:
                print(f"📤 Imgur 업로드 중: {card_name}")
                img_url = self.upload_to_imgur(card_img)
                
                if img_url:
                    uploaded_images.append({
                        'name': card_name,
                        'url': img_url
                    })
                    print(f"✅ 업로드 성공: {img_url}")
                else:
                    print(f"❌ 업로드 실패: {card_name}")
            
            if not uploaded_images:
                print("❌ 업로드된 이미지가 없습니다.")
                return None
            
            # 2. 노션 페이지 생성
            parent_page_id = "2002360b26038007a59fcda976552022"
            
            new_page = self.notion.client.pages.create(
                parent={
                    "type": "page_id",
                    "page_id": parent_page_id
                },
                properties={
                    "title": {
                        "title": [{
                            "text": {
                                "content": f"{page_title} - {datetime.now().strftime('%Y년 %m월 %d일')}"
                            }
                        }]
                    }
                },
                children=[]
            )
            
            page_id = new_page['id']
            print(f"✅ 노션 페이지 생성 완료: {page_id}")
            
            # 3. 이미지 블록 추가
            children_blocks = [
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "🗞️ 전력산업 주간 카드뉴스"}
                        }]
                    }
                }
            ]
            
            # 각 이미지 추가
            for img_info in uploaded_images:
                # 구분선
                children_blocks.append({
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                })
                
                # 이미지 제목
                children_blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": img_info['name']}
                        }]
                    }
                })
                
                # 이미지
                children_blocks.append({
                    "object": "block",
                    "type": "image",
                    "image": {
                        "type": "external",
                        "external": {
                            "url": img_info['url']
                        }
                    }
                })
            
            # 블록 추가
            self.notion.client.blocks.children.append(
                block_id=page_id,
                children=children_blocks
            )
            
            print(f"✅ 노션 자동 업로드 완료!")
            print(f"📍 페이지 URL: https://notion.so/{page_id.replace('-', '')}")
            
            return page_id
            
        except Exception as e:
            print(f"❌ 자동 업로드 중 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    

    def generate_structured_card_news(self):
        """구조화된 콘텐츠를 활용한 카드뉴스 생성"""
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
        """향상된 요약 카드 생성"""
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
        """트렌드 분석 카드 생성"""
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
    
    def generate_card_news(self):
        """전체 카드뉴스 생성 프로세스"""
        print("🚀 카드뉴스 생성 시작...")
        
        try:
            # 1. 관심 기사 가져오기
            print("📰 관심 표시된 기사 가져오는 중...")
            interested_articles = self.notion.get_interested_articles()
            
            if not interested_articles:
                print("⚠️ 관심 표시된 기사가 없습니다.")
                return
            
            print(f"✅ {len(interested_articles)}개의 관심 기사 발견")
            
            # 2. 카드 생성
            cards = []
            
            # 요약 카드
            print("🎨 요약 카드 생성 중...")
            summary_card = self.create_summary_card(interested_articles)
            cards.append(("1. 주간 요약", summary_card))
            
            # 개별 기사 카드 (상위 5개)
            for i, article in enumerate(interested_articles[:5]):
                print(f"🎨 기사 카드 {i+1} 생성 중...")
                article_card = self.create_article_card(article, card_number=i+1)
                title = article.get('title', '')[:40] + '...' if len(article.get('title', '')) > 40 else article.get('title', '')
                cards.append((f"{i+2}. {title}", article_card))
            
            # 통계 카드
            print("📊 통계 카드 생성 중...")
            stats_card = self.create_statistics_card(interested_articles)
            cards.append((f"{len(cards)+1}. 카테고리별 통계", stats_card))
            
            # 3. 로컬 저장
            output_dir = os.path.join(os.path.dirname(__file__), 'card_news_output')
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for card_name, card_img in cards:
                filename = f"{timestamp}_{card_name.replace(' ', '_').replace('.', '')}.png"
                filepath = os.path.join(output_dir, filename)
                card_img.save(filepath)
                print(f"💾 로컬 저장: {filepath}")
            
            # 4. 자동 업로드
            page_id = self.save_cards_to_notion_auto(cards)
            
            print("🎉 카드뉴스 생성 및 자동 업로드 완료!")
            
            return cards
            
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🎨 전력산업 카드뉴스 생성기 V2")
    print("📊 한글 지원 + 자동 업로드")
    print("=" * 60)
    
    generator = CardNewsGeneratorV2()
    generator.generate_card_news()


if __name__ == "__main__":
    main()
