#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 실제 노션 데이터로 개선된 카드뉴스 생성
"""

import os
from datetime import datetime
from notion.notion_client import NotionClient
from enhanced_article_card_generator import EnhancedArticleCardGenerator
import base64
import requests

def main():
    print("🎨 개선된 개별 기사 카드뉴스 생성")
    print("=" * 60)
    
    # 1. 노션 클라이언트 초기화
    notion = NotionClient()
    generator = EnhancedArticleCardGenerator()
    
    # 2. 이번 주 데이터베이스에서 기사 가져오기
    print("\n📊 노션에서 기사 가져오는 중...")
    database_id = notion.get_weekly_database_id()
    
    if not database_id:
        print("❌ 데이터베이스를 찾을 수 없습니다.")
        return
        
    # 관심 표시된 기사 우선, 없으면 전체 기사
    interested_articles = notion.get_interested_articles(database_id)
    
    if interested_articles:
        articles = interested_articles[:5]  # 최대 5개
        print(f"✅ 관심 표시된 기사 {len(articles)}개 발견")
    else:
        all_articles = notion.get_all_articles_from_db(database_id)
        articles = all_articles[:5]  # 최대 5개
        print(f"✅ 전체 기사 중 상위 {len(articles)}개 선택")
    
    # 3. 각 기사별로 개선된 카드 생성
    print("\n🎨 개별 기사 카드 생성 중...")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(os.getcwd(), 'enhanced_cards_output')
    os.makedirs(output_dir, exist_ok=True)
    
    generated_cards = []
    
    for i, article in enumerate(articles, 1):
        print(f"\n[{i}/{len(articles)}] {article['title'][:50]}...")
        
        try:
            # 카드 생성
            card_img = generator.create_structured_article_card(article)
            
            # 파일 저장
            safe_title = article['title'][:30].replace('/', '_').replace(' ', '_')
            filename = f"{timestamp}_{i}_{safe_title}.png"
            filepath = os.path.join(output_dir, filename)
            card_img.save(filepath)
            
            generated_cards.append({
                'filepath': filepath,
                'filename': filename,
                'article': article
            })
            
            print(f"  ✅ 카드 생성 완료: {filename}")
            
        except Exception as e:
            print(f"  ❌ 카드 생성 실패: {str(e)}")
    
    # 4. 결과 요약
    print("\n" + "=" * 60)
    print(f"📊 생성 결과")
    print("=" * 60)
    print(f"✅ 총 {len(generated_cards)}개 카드 생성 완료")
    print(f"📁 저장 위치: {output_dir}")
    
    # 5. Imgur 업로드 (선택사항)
    print("\n📤 생성된 카드를 Imgur에 업로드하시겠습니까? (Y/N)")
    # 자동으로 Y 선택
    upload_choice = 'Y'
    
    if upload_choice.upper() == 'Y':
        upload_to_imgur(generated_cards)
    
    print("\n🎉 완료!")

def upload_to_imgur(cards):
    """Imgur에 카드 업로드"""
    CLIENT_ID = 'dd32dd3c6aaa9a0'
    
    print("\n📤 Imgur 업로드 중...")
    uploaded = []
    
    for card_info in cards[:3]:  # 최대 3개만
        filepath = card_info['filepath']
        
        try:
            with open(filepath, 'rb') as f:
                img_data = f.read()
            
            b64_image = base64.b64encode(img_data).decode()
            
            headers = {'Authorization': f'Client-ID {CLIENT_ID}'}
            data = {
                'image': b64_image,
                'type': 'base64',
                'title': card_info['article']['title'][:50],
                'description': '개선된 전력산업 카드뉴스'
            }
            
            response = requests.post(
                'https://api.imgur.com/3/image',
                headers=headers,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    img_link = result['data']['link']
                    uploaded.append({
                        'title': card_info['article']['title'],
                        'link': img_link
                    })
                    print(f"  ✅ {card_info['filename']}")
                    print(f"     📎 {img_link}")
        
        except Exception as e:
            print(f"  ❌ 업로드 실패: {str(e)}")
    
    # 결과 출력
    if uploaded:
        print(f"\n✅ {len(uploaded)}개 카드 업로드 완료!")
        print("\n📱 카드뉴스 링크:")
        for item in uploaded:
            print(f"\n🔗 {item['title'][:50]}...")
            print(f"   {item['link']}")

if __name__ == "__main__":
    main()
