#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 향상된 카드 뉴스 생성기 V3
- 구조화된 콘텐츠
- 향상된 시각화
- 데이터 기반 인사이트
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from datetime import datetime
import textwrap

class EnhancedCardNewsGenerator:
    def __init__(self):
        self.width = 1080
        self.height = 1920
        
        # 색상 팔레트 (더 현대적으로)
        self.colors = {
            'background': '#0F0F0F',
            'card_bg': '#1A1A1A',
            'primary': '#00E5FF',
            'secondary': '#FF6B6B',
            'accent': '#FFE66D',
            'success': '#4ECDC4',
            'text': '#FFFFFF',
            'text_light': '#B0B0B0',
            'gradient_start': '#2563EB',
            'gradient_end': '#7C3AED'
        }
        
        # 폰트 설정
        self.font_path = self._find_korean_font()
        self.font_sizes = {
            'title': 72,
            'subtitle': 48,
            'heading': 40,
            'body': 32,
            'caption': 24,
            'small': 20
        }
        
    def _find_korean_font(self):
        """한글 폰트 찾기"""
        font_candidates = [
            '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf',
            '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
            'C:/Windows/Fonts/malgun.ttf',
            'C:/Windows/Fonts/malgunbd.ttf',
        ]
        
        for font in font_candidates:
            if os.path.exists(font):
                return font
                
        # matplotlib 폰트 검색
        for font in fm.findSystemFonts(fontpaths=None):
            if 'nanum' in font.lower() or 'malgun' in font.lower():
                return font
                
        return None
        
    def _get_font(self, style='regular', size=24):
        """폰트 객체 반환"""
        if self.font_path:
            return ImageFont.truetype(self.font_path, size)
        return ImageFont.load_default()
        
    def create_enhanced_summary_card(self, articles, insights):
        """향상된 요약 카드 - 핵심 인사이트 포함"""
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # 그라데이션 헤더
        for y in range(300):
            ratio = y / 300
            r1, g1, b1 = int(self.colors['gradient_start'][1:3], 16), int(self.colors['gradient_start'][3:5], 16), int(self.colors['gradient_start'][5:7], 16)
            r2, g2, b2 = int(self.colors['gradient_end'][1:3], 16), int(self.colors['gradient_end'][3:5], 16), int(self.colors['gradient_end'][5:7], 16)
            r = int(r1 * (1 - ratio) + r2 * ratio)
            g = int(g1 * (1 - ratio) + g2 * ratio)
            b = int(b1 * (1 - ratio) + b2 * ratio)
            draw.rectangle([(0, y), (self.width, y+1)], fill=f'#{r:02x}{g:02x}{b:02x}')
            
        # 제목
        title_font = self._get_font('bold', self.font_sizes['title'])
        draw.text((80, 80), "⚡ 전력산업 위클리", font=title_font, fill='#FFFFFF')
        
        # 부제목
        subtitle_font = self._get_font('regular', self.font_sizes['subtitle'])
        week = datetime.now().strftime("%Y년 %m월 %d주차")
        draw.text((80, 180), week, font=subtitle_font, fill=self.colors['text_light'])
        
        # 핵심 인사이트 섹션
        y_pos = 400
        heading_font = self._get_font('bold', self.font_sizes['heading'])
        draw.text((80, y_pos), "🎯 이번 주 핵심 트렌드", font=heading_font, fill=self.colors['primary'])
        
        y_pos += 80
        body_font = self._get_font('regular', self.font_sizes['body'])
        
        # 인사이트 카드들
        for i, insight in enumerate(insights[:3]):
            # 인사이트 카드 배경
            card_y = y_pos + (i * 200)
            draw.rounded_rectangle(
                [(60, card_y), (self.width - 60, card_y + 160)],
                radius=20,
                fill=self.colors['card_bg']
            )
            
            # 인사이트 아이콘과 텍스트
            icon = ["📈", "💡", "🔋"][i]
            draw.text((100, card_y + 30), icon, font=self._get_font('regular', 60), fill=self.colors['accent'])
            
            # 인사이트 제목
            draw.text((200, card_y + 40), insight['title'], font=self._get_font('bold', 36), fill='#FFFFFF')
            
            # 인사이트 내용
            content = self._wrap_text(insight['content'], body_font, self.width - 240, draw)
            draw.text((200, card_y + 90), content[0] if content else "", font=self._get_font('regular', 28), fill=self.colors['text_light'])
            
        # 통계 요약
        stats_y = self.height - 400
        draw.text((80, stats_y), "📊 주간 통계", font=heading_font, fill=self.colors['primary'])
        
        stats_text = f"총 {len(articles)}개 기사 | AI 추천 {sum(1 for a in articles if a.get('ai_recommend'))}개"
        draw.text((80, stats_y + 60), stats_text, font=body_font, fill=self.colors['text_light'])
        
        return img
        
    def create_data_visualization_card(self, articles):
        """데이터 시각화 전용 카드"""
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        
        # matplotlib 설정
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(10, 18), facecolor=self.colors['background'])
        
        # 1. 일별 기사 수 추이
        ax1 = plt.subplot(3, 1, 1)
        dates = [a.get('published_date') for a in articles if a.get('published_date')]
        date_counts = {}
        for date in dates:
            date_str = date.strftime('%m/%d') if hasattr(date, 'strftime') else str(date)
            date_counts[date_str] = date_counts.get(date_str, 0) + 1
            
        ax1.bar(date_counts.keys(), date_counts.values(), color=self.colors['primary'])
        ax1.set_title('일별 기사 수 추이', fontsize=20, color='white', pad=20)
        ax1.set_xlabel('날짜', fontsize=14)
        ax1.set_ylabel('기사 수', fontsize=14)
        
        # 2. 키워드 빈도 분석
        ax2 = plt.subplot(3, 1, 2)
        keyword_counts = {}
        for article in articles:
            for keyword in article.get('keywords', []):
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
                
        top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        keywords, counts = zip(*top_keywords) if top_keywords else ([], [])
        
        ax2.barh(keywords, counts, color=self.colors['secondary'])
        ax2.set_title('핫 키워드 TOP 8', fontsize=20, color='white', pad=20)
        ax2.set_xlabel('언급 횟수', fontsize=14)
        
        # 3. AI 추천 vs 비추천 비율
        ax3 = plt.subplot(3, 1, 3)
        ai_recommend = sum(1 for a in articles if a.get('ai_recommend'))
        non_recommend = len(articles) - ai_recommend
        
        colors = [self.colors['success'], self.colors['text_light']]
        ax3.pie([ai_recommend, non_recommend], 
                labels=['AI 추천', '일반'],
                colors=colors,
                autopct='%1.1f%%',
                startangle=90)
        ax3.set_title('AI 추천 비율', fontsize=20, color='white', pad=20)
        
        plt.tight_layout()
        
        # matplotlib 그래프를 이미지로 변환
        fig.savefig('temp_chart.png', facecolor=self.colors['background'], dpi=100)
        plt.close()
        
        # PIL 이미지로 불러오기
        chart_img = Image.open('temp_chart.png')
        img.paste(chart_img, (40, 200))
        
        # 제목 추가
        draw = ImageDraw.Draw(img)
        title_font = self._get_font('bold', self.font_sizes['title'])
        draw.text((80, 80), "📊 데이터 인사이트", font=title_font, fill='#FFFFFF')
        
        # 임시 파일 삭제
        os.remove('temp_chart.png')
        
        return img
        
    def _wrap_text(self, text, font, max_width, draw):
        """텍스트 줄바꿈"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
        
    def analyze_articles_for_insights(self, articles):
        """기사 분석하여 인사이트 도출"""
        insights = []
        
        # 1. 가장 많이 언급된 키워드 트렌드
        keyword_counts = {}
        for article in articles:
            for keyword in article.get('keywords', []):
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
                
        if keyword_counts:
            top_keyword = max(keyword_counts, key=keyword_counts.get)
            insights.append({
                'title': '주목받는 키워드',
                'content': f'"{top_keyword}"가 {keyword_counts[top_keyword]}회 언급되며 화제'
            })
            
        # 2. AI 추천 기사 비율
        ai_recommend_count = sum(1 for a in articles if a.get('ai_recommend'))
        if articles:
            ai_ratio = (ai_recommend_count / len(articles)) * 100
            insights.append({
                'title': 'AI 추천도',
                'content': f'전체 기사의 {ai_ratio:.0f}%가 AI 추천 기사로 선정'
            })
            
        # 3. 주요 이슈
        if articles and articles[0].get('title'):
            insights.append({
                'title': '헤드라인 이슈',
                'content': articles[0]['title'][:50] + '...' if len(articles[0]['title']) > 50 else articles[0]['title']
            })
            
        return insights

# 사용 예시
if __name__ == "__main__":
    generator = EnhancedCardNewsGenerator()
    
    # 테스트 데이터
    test_articles = [
        {
            'title': '재생에너지 발전량 사상 최대 기록',
            'keywords': ['재생에너지', '태양광', '풍력'],
            'ai_recommend': True,
            'published_date': datetime.now()
        }
    ]
    
    # 인사이트 분석
    insights = generator.analyze_articles_for_insights(test_articles)
    
    # 카드 생성
    summary_card = generator.create_enhanced_summary_card(test_articles, insights)
    summary_card.save('enhanced_summary.png')
    
    data_card = generator.create_data_visualization_card(test_articles)
    data_card.save('data_visualization.png')
    
    print("✅ 향상된 카드 뉴스 생성 완료!")
