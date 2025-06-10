#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖼️ 카드뉴스 Imgur 업로더 (무료 대안)
Private 리포지토리를 유지하면서 무료로 이미지 호스팅
"""

import os
import base64
import requests
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv
from notion_client import Client
import re

load_dotenv()

print("""
📌 Imgur 무료 이미지 호스팅 사용법:

1. https://imgur.com 가입
2. https://api.imgur.com/oauth2/addclient 에서 앱 등록
3. Client ID 받기
4. .env 파일에 추가:
   IMGUR_CLIENT_ID=your_client_id_here

장점:
- 완전 무료
- Private 리포지토리 유지
- 이미지 직접 링크 제공
- Notion에서 바로 표시

단점:
- 이미지가 Imgur에 저장됨
- 일일 업로드 제한 있음 (충분함)
""")

class CardNewsImgurUploader:
    """Imgur를 사용하는 무료 카드뉴스 업로더"""
    
    def __init__(self):
        self.imgur_client_id = os.getenv('IMGUR_CLIENT_ID')
        self.notion = Client(auth=os.getenv('NOTION_API_KEY'))
        self.card_news_db_id = os.getenv('CARD_NEWS_DATABASE_ID', '20c2360b-2603-8175-bcf6-e6d134f4d7a8')
        
        if not self.imgur_client_id:
            print("❌ IMGUR_CLIENT_ID가 설정되지 않았습니다!")
            print("👉 https://api.imgur.com/oauth2/addclient 에서 등록 후")
            print("   echo 'IMGUR_CLIENT_ID=your_id' >> .env")
            return
        
        print("✅ Imgur 업로더 초기화 완료!")
    
    def upload_to_imgur(self, image_path: str) -> Optional[str]:
        """이미지를 Imgur에 업로드"""
        try:
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            headers = {'Authorization': f'Client-ID {self.imgur_client_id}'}
            data = {'image': image_data, 'type': 'base64'}
            
            response = requests.post('https://api.imgur.com/3/image', headers=headers, data=data)
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data']['link']
                print(f"✅ Imgur 업로드 성공: {image_url}")
                return image_url
            else:
                print(f"❌ Imgur 업로드 실패: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 오류: {str(e)}")
            return None

# Cloudinary 대안도 있습니다:
print("""
🌟 다른 무료 대안들:

1. **Cloudinary** (추천)
   - 무료: 25GB 저장공간, 25GB 대역폭/월
   - API 지원 우수
   - 이미지 변환 기능

2. **ImgBB**
   - 완전 무료
   - API 지원
   - 간단한 사용법

3. **GitHub Issues 트릭**
   - Issues에 이미지 드래그&드롭
   - 생성된 URL 복사해서 사용
   - 완전 무료, 하지만 비공식 방법
""")
