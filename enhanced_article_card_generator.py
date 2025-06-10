#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 개선된 개별 기사 카드뉴스 생성기
- 대주제/소주제 구조화
- 시각적 계층 구조
- 핵심 정보 강조
"""

import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from article_content_analyzer import ArticleContentAnalyzer

class EnhancedArticleCardGenerator:
    """개선된 기사 카드뉴스 생성기"""
    
    def __init__(self):
        self.width = 1080
        self.height = 1350  # 세로로 조금 더 길게
        self.analyzer = ArticleContentAnalyzer()
        
        # 색상 팔레트 (더 현대적으로)
        self.colors = {
            'background': '#FFFFFF',
            'header_bg': '#1E40AF',  # 진한 파란색
            'main_theme_bg': '#EFF6FF',  # 연한 파란색 배경
            'accent': '#F59E0B',  # 주황색 포인트
            'text_primary': '#111827',
            'text_secondary': '#6B7280',
            'border': '#E5E7EB',
            'success': '#10B981',
            'number_highlight': '#DC2626'  # 빨간색 (숫자 강조용)
        }
        
        # 폰트 설정
        self.font_path = os.path.expanduser('~/.fonts/D2Coding-Ver1.3.2-20180524.ttf')
        self.font_bold_path = os.path.expanduser('~/.fonts/D2CodingBold-Ver1.3.2-20180524.ttf')
        
        self.font_sizes = {
            'header': 24,
            'main_theme': 42,
            'sub_theme_title': 28,
            'sub_theme_content': 22,
            'body': 20,
            'caption': 18,
            'source': 16
        }
        
    def create_structured_article_card(self, article: dict) -> Image:
        """구조화된 기사 카드 생성"""
        
        # 기사 분석
        analysis = self.analyzer.analyze_article(article)
        
        # 이미지 생성
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        y_pos = 0
        
        # 1. 헤더 (출처, 날짜)
        y_pos = self._draw_header(draw, article, y_pos)
        
        # 2. 대주제 섹션
        y_pos = self._draw_main_theme(draw, analysis['main_theme'], y_pos)
        
        # 3. 핵심 수치 (있는 경우)
        if analysis['numbers']:
            y_pos = self._draw_key_numbers(draw, analysis['numbers'][:3], y_pos)
        
        # 4. 소주제들
        y_pos = self._draw_sub_themes(draw, analysis['sub_themes'][:3], y_pos)
        
        # 5. 핵심 포인트
        if analysis['key_facts']:
            y_pos = self._draw_key_points(draw, analysis['key_facts'][:3], y_pos)
        
        # 6. 푸터
        self._draw_footer(draw, analysis)
        
        return img
    
    def _get_font(self, style='regular', size=20):
        """폰트 객체 반환"""
        font_path = self.font_bold_path if style == 'bold' else self.font_path
        try:
            return ImageFont.truetype(font_path, size)
        except:
            return ImageFont.load_default()
    
    def _draw_header(self, draw, article, y_pos):
        """헤더 그리기"""
        # 상단 색상 바
        draw.rectangle([(0, 0), (self.width, 80)], fill=self.colors['header_bg'])
        
        # 출처와 날짜
        header_font = self._get_font('regular', self.font_sizes['header'])
        source = article.get('source', '전력산업뉴스')
        date = article.get('published_date', datetime.now().strftime('%Y-%m-%d'))
        
        draw.text((40, 25), source, font=header_font, fill='#FFFFFF')
        draw.text((self.width - 200, 25), str(date)[:10], font=header_font, fill='#FFFFFF')
        
        return 80
    
    def _draw_main_theme(self, draw, main_theme, y_pos):
        """대주제 섹션"""
        y_pos += 40
        
        # 대주제 배경
        theme_bg_height = 180
        draw.rectangle([(40, y_pos), (self.width - 40, y_pos + theme_bg_height)], 
                      fill=self.colors['main_theme_bg'])
        
        # 카테고리 태그
        category_font = self._get_font('regular', self.font_sizes['caption'])
        category = main_theme['category']
        draw.rectangle([(60, y_pos + 20), (60 + 100, y_pos + 50)], 
                      fill=self.colors['accent'])
        draw.text((70, y_pos + 25), category, font=category_font, fill='#FFFFFF')
        
        # 대주제 텍스트
        theme_font = self._get_font('bold', self.font_sizes['main_theme'])
        theme_text = main_theme['theme']
        
        # 텍스트 줄바꿈
        words = theme_text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=theme_font)
            if bbox[2] > self.width - 120:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(test_line)
                    current_line = []
        if current_line:
            lines.append(' '.join(current_line))
        
        # 대주제 그리기
        text_y = y_pos + 70
        for line in lines[:2]:  # 최대 2줄
            draw.text((60, text_y), line, font=theme_font, fill=self.colors['text_primary'])
            text_y += 50
        
        return y_pos + theme_bg_height + 20
    
    def _draw_key_numbers(self, draw, numbers, y_pos):
        """핵심 수치 표시"""
        if not numbers:
            return y_pos
            
        y_pos += 20
        
        # 수치 섹션 제목
        section_font = self._get_font('bold', self.font_sizes['sub_theme_title'])
        draw.text((60, y_pos), "📊 핵심 수치", font=section_font, fill=self.colors['text_primary'])
        y_pos += 50
        
        # 수치들을 가로로 배치
        x_positions = [60, 360, 660]
        number_font = self._get_font('bold', 36)
        unit_font = self._get_font('regular', self.font_sizes['body'])
        
        for i, num_info in enumerate(numbers[:3]):
            if i < len(x_positions):
                x = x_positions[i]
                
                # 수치 강조
                draw.text((x, y_pos), num_info['value'], 
                         font=number_font, fill=self.colors['number_highlight'])
                
                # 단위
                value_width = draw.textbbox((0, 0), num_info['value'], font=number_font)[2]
                draw.text((x + value_width + 5, y_pos + 10), num_info['unit'], 
                         font=unit_font, fill=self.colors['text_secondary'])
        
        return y_pos + 80
    
    def _draw_sub_themes(self, draw, sub_themes, y_pos):
        """소주제 섹션"""
        if not sub_themes:
            return y_pos
            
        y_pos += 30
        
        # 소주제 섹션 제목
        section_font = self._get_font('bold', self.font_sizes['sub_theme_title'])
        draw.text((60, y_pos), "📌 주요 내용", font=section_font, fill=self.colors['text_primary'])
        y_pos += 60
        
        # 각 소주제
        for i, sub_theme in enumerate(sub_themes):
            # 번호 원
            circle_x = 80
            circle_y = y_pos + 15
            draw.ellipse([(circle_x - 20, circle_y - 20), (circle_x + 20, circle_y + 20)], 
                        fill=self.colors['accent'])
            
            number_font = self._get_font('bold', 20)
            draw.text((circle_x - 5, circle_y - 10), str(i + 1), 
                     font=number_font, fill='#FFFFFF')
            
            # 소주제 제목
            title_font = self._get_font('bold', self.font_sizes['sub_theme_title'])
            draw.text((130, y_pos), sub_theme['title'], 
                     font=title_font, fill=self.colors['text_primary'])
            
            # 소주제 내용 (있는 경우)
            if len(sub_theme['content']) > len(sub_theme['title']) + 5:
                content_font = self._get_font('regular', self.font_sizes['sub_theme_content'])
                content_lines = self._wrap_text(sub_theme['content'], content_font, 
                                              self.width - 180, draw)
                content_y = y_pos + 40
                for line in content_lines[:2]:  # 최대 2줄
                    draw.text((130, content_y), line, 
                             font=content_font, fill=self.colors['text_secondary'])
                    content_y += 30
                y_pos = content_y + 20
            else:
                y_pos += 70
        
        return y_pos
    
    def _draw_key_points(self, draw, key_facts, y_pos):
        """핵심 포인트"""
        if not key_facts or y_pos > self.height - 300:
            return y_pos
            
        y_pos += 30
        
        # 배경 박스
        box_height = min(len(key_facts) * 50 + 40, 200)
        draw.rectangle([(40, y_pos), (self.width - 40, y_pos + box_height)], 
                      fill='#F3F4F6', outline=self.colors['border'])
        
        point_font = self._get_font('regular', self.font_sizes['body'])
        text_y = y_pos + 20
        
        for fact in key_facts[:3]:
            if text_y > y_pos + box_height - 30:
                break
                
            # 체크 아이콘
            draw.text((60, text_y), "✓", font=point_font, fill=self.colors['success'])
            
            # 포인트 텍스트
            fact_lines = self._wrap_text(fact, point_font, self.width - 160, draw)
            draw.text((90, text_y), fact_lines[0], 
                     font=point_font, fill=self.colors['text_primary'])
            text_y += 50
        
        return y_pos + box_height + 20
    
    def _draw_footer(self, draw, analysis):
        """푸터"""
        footer_y = self.height - 80
        
        # 구분선
        draw.line([(40, footer_y), (self.width - 40, footer_y)], 
                 fill=self.colors['border'], width=1)
        
        # 포커스 태그
        focus = analysis['main_theme']['focus']
        tag_font = self._get_font('regular', self.font_sizes['caption'])
        
        focus_colors = {
            '미래전망': '#3B82F6',
            '문제해결': '#DC2626',
            '성과발표': '#10B981',
            '신규도입': '#F59E0B',
            '현황보고': '#6B7280'
        }
        
        tag_color = focus_colors.get(focus, self.colors['text_secondary'])
        draw.text((60, footer_y + 20), f"#{focus}", 
                 font=tag_font, fill=tag_color)
        
        # 제작 정보
        draw.text((self.width - 300, footer_y + 20), 
                 "AI 전력산업 뉴스 분석", 
                 font=tag_font, fill=self.colors['text_secondary'])
    
    def _wrap_text(self, text, font, max_width, draw):
        """텍스트 줄바꿈"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] > max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(test_line)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines


# 테스트
if __name__ == "__main__":
    generator = EnhancedArticleCardGenerator()
    
    # 샘플 기사
    sample_article = {
        'title': '한전, 제주 재생에너지 출력제어 해결 위한 ESS 300MW 구축 추진',
        'summary': '한국전력공사가 제주도의 재생에너지 출력제어 문제 해결을 위해 300MW 규모의 ESS를 구축한다고 발표했다.',
        'key_points': '• 2026년까지 300MW ESS 구축\n• 총 사업비 5000억원 투입\n• 출력제어율 30%에서 10%로 감소 기대\n• 지역 주민 일자리 500개 창출',
        'source': '전기신문',
        'published_date': '2025-06-07'
    }
    
    # 카드 생성
    card = generator.create_structured_article_card(sample_article)
    card.save('enhanced_article_card_sample.png')
    print("✅ 개선된 기사 카드 생성 완료: enhanced_article_card_sample.png")
