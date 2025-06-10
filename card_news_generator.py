# card_news_generator.py
"""
전력산업 관심 뉴스 카드 뉴스 생성기
이미지 기반 카드 뉴스를 생성하여 노션에 업로드
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

# 한글 폰트 경로 설정
FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
FONT_REGULAR = os.path.join(FONT_DIR, 'NotoSansKR-Regular.otf')
FONT_BOLD = os.path.join(FONT_DIR, 'NotoSansKR-Bold.otf')

class CardNewsGenerator:
    def __init__(self):
        """카드 뉴스 생성기 초기화"""
        # 카드 크기 설정 (인스타그램 정사각형)
        self.width = 1080
        self.height = 1080
        
        # 색상 팔레트 (전력산업 테마)
        self.colors = {
            'background': '#FFFFFF',      # 깨끗한 흰색 배경
            'primary': '#2563EB',        # 전기 파란색
            'secondary': '#10B981',      # 재생에너지 초록색  
            'accent': '#F59E0B',         # 태양광 노란색
            'danger': '#EF4444',         # 위험/경고 빨간색
            'text': '#1F2937',           # 진한 회색 텍스트
            'text_light': '#6B7280',     # 연한 회색 텍스트
            'border': '#E5E7EB',         # 테두리 회색
            'gradient_start': '#2563EB', # 그라데이션 시작
            'gradient_end': '#10B981'    # 그라데이션 끝
        }
        
        # 카테고리별 색상
        self.category_colors = {
            '태양광': '#F59E0B',      # 노란색
            'ESS': '#3B82F6',         # 파란색
            '전력망': '#8B5CF6',      # 보라색
            '재생에너지': '#10B981',  # 초록색
            'VPP': '#EC4899',         # 핑크색
            '정책': '#6B7280',        # 회색
            '기타': '#1F2937'         # 진한 회색
        }
        
        # 폰트 크기 설정
        self.font_sizes = {
            'main_title': 48,
            'sub_title': 36,
            'article_title': 32,
            'body': 24,
            'caption': 20,
            'small': 18
        }
        
        # 노션 클라이언트
        self.notion = NotionClient()
        
    def _get_font(self, font_type='regular', size=24):
        """폰트 객체 반환"""
        font_path = FONT_BOLD if font_type == 'bold' else FONT_REGULAR
        try:
            return ImageFont.truetype(font_path, size)
        except:
            print(f"폰트 로드 실패: {font_path}")
            return ImageFont.load_default()
    
    def _wrap_text(self, text, font, max_width):
        """텍스트를 주어진 너비에 맞게 줄바꿈"""
        lines = []
        words = text.split()
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _draw_gradient_background(self, img):
        """그라데이션 배경 그리기"""
        draw = ImageDraw.Draw(img)
        
        # 위에서 아래로 그라데이션
        for y in range(self.height):
            # 선형 보간으로 색상 계산
            ratio = y / self.height
            r1, g1, b1 = int(self.colors['gradient_start'][1:3], 16), int(self.colors['gradient_start'][3:5], 16), int(self.colors['gradient_start'][5:7], 16)
            r2, g2, b2 = int(self.colors['gradient_end'][1:3], 16), int(self.colors['gradient_end'][3:5], 16), int(self.colors['gradient_end'][5:7], 16)
            
            r = int(r1 * (1 - ratio) + r2 * ratio)
            g = int(g1 * (1 - ratio) + g2 * ratio)  
            b = int(b1 * (1 - ratio) + b2 * ratio)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            draw.line([(0, y), (self.width, y)], fill=color, width=1)
    
    def _get_category_from_keywords(self, keywords):
        """키워드에서 카테고리 추출"""
        if not keywords:
            return '기타'
        
        # 우선순위 순서대로 확인
        priority_categories = ['태양광', 'ESS', '재생에너지', 'VPP', '전력망']
        for category in priority_categories:
            if category in keywords:
                return category
        
        return '정책'  # 기본값
    
    def create_summary_card(self, articles):
        """주간 요약 카드 생성"""
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # 헤더 영역 (그라데이션 배경)
        header_height = 200
        header_img = Image.new('RGB', (self.width, header_height))
        self._draw_gradient_background(header_img)
        img.paste(header_img, (0, 0))
        
        # 제목
        title_font = self._get_font('bold', self.font_sizes['main_title'])
        title_text = f"📊 전력산업 주간 뉴스"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_x = (self.width - (title_bbox[2] - title_bbox[0])) // 2
        draw.text((title_x, 50), title_text, font=title_font, fill='#FFFFFF')
        
        # 부제목 (날짜)
        now = datetime.now()
        subtitle_font = self._get_font('regular', self.font_sizes['sub_title'])
        subtitle_text = f"{now.year}년 {now.isocalendar()[1]}주차"
        subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        subtitle_x = (self.width - (subtitle_bbox[2] - subtitle_bbox[0])) // 2
        draw.text((subtitle_x, 120), subtitle_text, font=subtitle_font, fill='#FFFFFF')
        
        # TOP 3 섹션
        y_pos = 250
        section_font = self._get_font('bold', self.font_sizes['article_title'])
        draw.text((80, y_pos), "🏆 이번 주 TOP 3", font=section_font, fill=self.colors['primary'])
        y_pos += 60
        
        # TOP 3 기사
        article_font = self._get_font('regular', self.font_sizes['body'])
        medals = ['🥇', '🥈', '🥉']
        
        for i, article in enumerate(articles[:3]):
            if i >= len(medals):
                break
                
            # 메달과 제목
            medal_text = medals[i]
            title = article.get('title', '')[:40] + '...' if len(article.get('title', '')) > 40 else article.get('title', '')
            
            # 카테고리 색상 적용
            category = self._get_category_from_keywords(article.get('keywords', []))
            category_color = self.category_colors.get(category, self.colors['text'])
            
            draw.text((80, y_pos), medal_text, font=article_font, fill=self.colors['text'])
            draw.text((120, y_pos), title, font=article_font, fill=category_color)
            y_pos += 50
        
        # 카테고리별 통계
        y_pos += 50
        draw.text((80, y_pos), "📈 카테고리별 관심 기사", font=section_font, fill=self.colors['primary'])
        y_pos += 60
        
        # 카테고리별 카운트
        category_counts = {}
        for article in articles:
            category = self._get_category_from_keywords(article.get('keywords', []))
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # 카테고리별 표시
        stat_font = self._get_font('regular', self.font_sizes['caption'])
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            color = self.category_colors.get(category, self.colors['text'])
            
            # 카테고리 박스
            box_width = 120
            box_height = 40
            draw.rounded_rectangle(
                [(80, y_pos), (80 + box_width, y_pos + box_height)],
                radius=20,
                fill=color
            )
            
            # 카테고리 텍스트
            text = f"{category} ({count})"
            text_bbox = draw.textbbox((0, 0), text, font=stat_font)
            text_x = 80 + (box_width - (text_bbox[2] - text_bbox[0])) // 2
            text_y = y_pos + (box_height - (text_bbox[3] - text_bbox[1])) // 2
            draw.text((text_x, text_y), text, font=stat_font, fill='#FFFFFF')
            
            y_pos += 50
        
        # 푸터
        footer_font = self._get_font('regular', self.font_sizes['small'])
        footer_text = "Generated by AI Power News Crawler"
        footer_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
        footer_x = (self.width - (footer_bbox[2] - footer_bbox[0])) // 2
        draw.text((footer_x, self.height - 50), footer_text, font=footer_font, fill=self.colors['text_light'])
        
        return img
    
    def create_article_card(self, article, card_number=1):
        """개별 기사 카드 생성"""
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # 카테고리 추출
        category = self._get_category_from_keywords(article.get('keywords', []))
        category_color = self.category_colors.get(category, self.colors['primary'])
        
        # 상단 색상 바
        draw.rectangle([(0, 0), (self.width, 100)], fill=category_color)
        
        # 카드 번호
        number_font = self._get_font('bold', 60)
        draw.text((50, 20), f"{card_number}", font=number_font, fill='#FFFFFF')
        
        # 카테고리 표시
        category_font = self._get_font('regular', self.font_sizes['body'])
        draw.text((150, 40), category, font=category_font, fill='#FFFFFF')
        
        # 제목 영역
        title_font = self._get_font('bold', self.font_sizes['article_title'])
        title = article.get('title', '')
        title_lines = self._wrap_text(title, title_font, self.width - 160)
        
        y_pos = 150
        for line in title_lines[:3]:  # 최대 3줄
            draw.text((80, y_pos), line, font=title_font, fill=self.colors['text'])
            y_pos += 40
        
        # 구분선
        y_pos += 20
        draw.line([(80, y_pos), (self.width - 80, y_pos)], fill=self.colors['border'], width=2)
        y_pos += 30
        
        # 한줄요약
        summary_font = self._get_font('regular', self.font_sizes['body'])
        summary = article.get('summary', '')
        summary_lines = self._wrap_text(summary, summary_font, self.width - 160)
        
        draw.text((80, y_pos), "💡 핵심 요약", font=self._get_font('bold', self.font_sizes['body']), fill=category_color)
        y_pos += 40
        
        for line in summary_lines[:3]:
            draw.text((80, y_pos), line, font=summary_font, fill=self.colors['text'])
            y_pos += 35
        
        # 핵심 포인트
        y_pos += 30
        draw.text((80, y_pos), "📌 주요 내용", font=self._get_font('bold', self.font_sizes['body']), fill=category_color)
        y_pos += 40
        
        # 핵심 내용에서 3개 포인트 추출
        key_points = article.get('key_points', '').split('*')[:4]  # 첫 번째는 보통 빈 문자열
        point_font = self._get_font('regular', self.font_sizes['caption'])
        
        for point in key_points[1:]:  # 빈 문자열 제외
            if point.strip():
                point_text = f"• {point.strip()[:80]}..."
                point_lines = self._wrap_text(point_text, point_font, self.width - 160)
                for line in point_lines[:2]:
                    draw.text((80, y_pos), line, font=point_font, fill=self.colors['text'])
                    y_pos += 30
                y_pos += 10
        
        # 키워드 태그
        if article.get('keywords'):
            y_pos = self.height - 150
            tag_font = self._get_font('regular', self.font_sizes['small'])
            
            x_pos = 80
            for keyword in article.get('keywords', [])[:5]:
                tag_text = f"#{keyword}"
                tag_bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
                tag_width = tag_bbox[2] - tag_bbox[0] + 20
                
                # 태그 박스
                draw.rounded_rectangle(
                    [(x_pos, y_pos), (x_pos + tag_width, y_pos + 30)],
                    radius=15,
                    outline=category_color,
                    width=2
                )
                
                # 태그 텍스트
                draw.text((x_pos + 10, y_pos + 5), tag_text, font=tag_font, fill=category_color)
                x_pos += tag_width + 10
        
        # 출처와 날짜
        footer_font = self._get_font('regular', self.font_sizes['small'])
        footer_text = f"출처: {article.get('source', '전기신문')} | {datetime.now().strftime('%Y.%m.%d')}"
        footer_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
        footer_x = (self.width - (footer_bbox[2] - footer_bbox[0])) // 2
        draw.text((footer_x, self.height - 50), footer_text, font=footer_font, fill=self.colors['text_light'])
        
        return img
    
    def create_statistics_card(self, articles):
        """통계 카드 생성 - 시각적 차트 포함"""
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        
                # matplotlib 한글 설정
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
        
        # 설치된 한글 폰트 확인
        font_list = fm.findSystemFonts(fontpaths=None)
        d2coding_fonts = [f for f in font_list if 'D2Coding' in f]
        
        if d2coding_fonts:
            # D2Coding 폰트가 있으면 사용
            font_path = d2coding_fonts[0]
            font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
            plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
        else:
            # 없으면 기본 설정 유지
            plt.rcParams['font.family'] = 'DejaVu Sans'
            
        plt.rcParams['axes.unicode_minus'] = False
        
        # 카테고리별 통계 계산
        category_counts = {}
        for article in articles:
            category = self._get_category_from_keywords(article.get('keywords', []))
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # 파이 차트 생성
        fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
        
        categories = list(category_counts.keys())
        values = list(category_counts.values())
        colors_list = [self.category_colors.get(cat, '#1F2937') for cat in categories]
        
        # 파이 차트 그리기
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=categories,
            colors=colors_list,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 14}
        )
        
        # 차트를 이미지로 변환
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_img = Image.open(buf)
        plt.close()
        
        # 차트 이미지를 카드에 붙이기
        chart_img = chart_img.resize((800, 800))
        img.paste(chart_img, ((self.width - 800) // 2, 140))
        
        # 제목 추가
        draw = ImageDraw.Draw(img)
        title_font = self._get_font('bold', self.font_sizes['main_title'])
        title_text = "📊 카테고리별 관심 기사 분포"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_x = (self.width - (title_bbox[2] - title_bbox[0])) // 2
        draw.text((title_x, 50), title_text, font=title_font, fill=self.colors['primary'])
        
        # 총 기사 수 표시
        stat_font = self._get_font('regular', self.font_sizes['body'])
        total_text = f"총 {len(articles)}개 기사 분석"
        total_bbox = draw.textbbox((0, 0), total_text, font=stat_font)
        total_x = (self.width - (total_bbox[2] - total_bbox[0])) // 2
        draw.text((total_x, self.height - 100), total_text, font=stat_font, fill=self.colors['text'])
        
        return img
    
    def save_cards_to_notion(self, cards, page_title="주간 전력산업 카드뉴스"):
        """생성된 카드들을 노션에 업로드"""
        try:
            print(f"📤 노션에 카드뉴스 업로드 시작...")
            
            # 부모 페이지 ID (PROJECT_ANALYSIS.md에서 확인)
            parent_page_id = "2002360b26038007a59fcda976552022"
            
            # 새 페이지 생성
            new_page = self.notion.client.pages.create(
                parent={
                    "type": "page_id",
                    "page_id": parent_page_id
                },
                properties={
                    "title": {
                        "title": [
                            {
                                "text": {
                                    "content": f"{page_title} - {datetime.now().strftime('%Y년 %m월 %d일')}"
                                }
                            }
                        ]
                    }
                },
                children=[]
            )
            
            page_id = new_page['id']
            print(f"✅ 새 페이지 생성 완료: {page_id}")
            
            # 각 카드를 이미지로 변환하여 업로드
            children_blocks = []
            
            # 헤더 추가
            children_blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "🗞️ 전력산업 주간 카드뉴스"}
                    }]
                }
            })
            
            # 설명 추가
            children_blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "이번 주 전력산업 관련 주요 뉴스를 카드뉴스로 정리했습니다."}
                    }]
                }
            })
            
            # 각 카드 이미지를 base64로 인코딩하여 업로드
            for i, (card_name, card_img) in enumerate(cards):
                print(f"📸 카드 업로드 중: {card_name}")
                
                # 이미지를 bytes로 변환
                img_buffer = io.BytesIO()
                card_img.save(img_buffer, format='PNG')
                img_bytes = img_buffer.getvalue()
                
                # base64 인코딩
                img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                
                # 구분선 추가
                if i > 0:
                    children_blocks.append({
                        "object": "block",
                        "type": "divider",
                        "divider": {}
                    })
                
                # 카드 제목
                children_blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": card_name}
                        }]
                    }
                })
                
                # 이미지 설명 (노션은 직접 이미지 업로드를 API로 지원하지 않음)
                children_blocks.append({
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "icon": {"emoji": "🖼️"},
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": f"{card_name} - 이미지는 별도로 다운로드하여 확인하세요."}
                        }]
                    }
                })
            
            # 블록 추가
            self.notion.client.blocks.children.append(
                block_id=page_id,
                children=children_blocks
            )
            
            print(f"✅ 노션 업로드 완료!")
            print(f"📍 페이지 URL: https://notion.so/{page_id.replace('-', '')}")
            
            return page_id
            
        except Exception as e:
            print(f"❌ 노션 업로드 중 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
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
            
            # 개별 기사 카드 (상위 5개만)
            for i, article in enumerate(interested_articles[:5]):
                print(f"🎨 기사 카드 {i+1} 생성 중: {article.get('title', '')[:30]}...")
                article_card = self.create_article_card(article, card_number=i+1)
                cards.append((f"{i+2}. {article.get('title', '')[:40]}...", article_card))
            
            # 통계 카드
            print("📊 통계 카드 생성 중...")
            stats_card = self.create_statistics_card(interested_articles)
            cards.append((f"{len(cards)+1}. 카테고리별 통계", stats_card))
            
            # 3. 로컬에 저장
            output_dir = os.path.join(os.path.dirname(__file__), 'card_news_output')
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for card_name, card_img in cards:
                filename = f"{timestamp}_{card_name.replace(' ', '_').replace('.', '')}.png"
                filepath = os.path.join(output_dir, filename)
                card_img.save(filepath)
                print(f"💾 저장 완료: {filepath}")
            
            # 4. 노션에 업로드
            page_id = self.save_cards_to_notion(cards)
            
            print("🎉 카드뉴스 생성 완료!")
            print(f"📁 저장 위치: {output_dir}")
            
            return cards
            
        except Exception as e:
            print(f"❌ 카드뉴스 생성 중 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🎨 전력산업 카드뉴스 생성기")
    print("📊 관심 기사를 시각적 카드뉴스로 변환")
    print("=" * 60)
    
    # 폰트 파일 확인
    if not os.path.exists(FONT_REGULAR):
        print(f"⚠️ 폰트 파일이 없습니다: {FONT_REGULAR}")
        print("폰트를 다운로드하거나 경로를 수정해주세요.")
        return
    
    # 카드뉴스 생성기 실행
    generator = CardNewsGenerator()
    generator.generate_card_news()


if __name__ == "__main__":
    main()
