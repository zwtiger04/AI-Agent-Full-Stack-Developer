#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖼️ 카드뉴스 GitHub Pages 업로더
Private 리포지토리 + GitHub Pages 사용
"""

import os
import base64
import requests
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv
from notion_client import Client
import re
import time

load_dotenv()

class CardNewsUploaderPages:
    """GitHub Pages를 사용하는 카드뉴스 업로더"""
    
    def __init__(self):
        # GitHub 설정
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_username = 'zwtiger04'
        self.github_repo = 'AI-Agent-Full-Stack-Developer'
        self.github_branch = 'main'
        
        # GitHub API 헤더
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        # Notion 설정
        self.notion = Client(auth=os.getenv('NOTION_API_KEY'))
        self.card_news_db_id = os.getenv('CARD_NEWS_DATABASE_ID', '20c2360b-2603-8175-bcf6-e6d134f4d7a8')
        
        print(f"✅ GitHub Pages 업로더 초기화 완료!")
    
    def safe_filename(self, filename: str) -> str:
        """파일명 안전하게 변환"""
        name, ext = os.path.splitext(filename)
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        safe_name = re.sub(r'_+', '_', safe_name).strip('_')
        if not safe_name:
            safe_name = f"image_{datetime.now().strftime('%H%M%S')}"
        return f"{safe_name}{ext}"
    
    def upload_image_to_github(self, image_path: str, custom_name: str = None) -> Optional[str]:
        """이미지를 GitHub에 업로드하고 GitHub Pages URL 반환"""
        try:
            if not os.path.exists(image_path):
                print(f"❌ 파일을 찾을 수 없습니다: {image_path}")
                return None
            
            # 파일명 처리
            original_name = os.path.basename(image_path)
            safe_name = custom_name or self.safe_filename(original_name)
            
            # GitHub 경로
            date_folder = datetime.now().strftime('%Y%m%d')
            github_path = f"card_news/{date_folder}/{safe_name}"
            
            print(f"📤 업로드 중: {original_name} → {safe_name}")
            
            # base64 인코딩
            with open(image_path, 'rb') as f:
                content_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            # GitHub API
            api_url = f"https://api.github.com/repos/{self.github_username}/{self.github_repo}/contents/{github_path}"
            
            data = {
                "message": f"📸 카드뉴스: {safe_name}",
                "content": content_base64,
                "branch": self.github_branch
            }
            
            response = requests.put(api_url, headers=self.headers, json=data)
            
            if response.status_code in [201, 200]:
                # GitHub Pages URL 생성
                pages_url = f"https://{self.github_username}.github.io/{self.github_repo}/{github_path}"
                
                print(f"✅ 업로드 성공!")
                print(f"🔗 GitHub Pages URL: {pages_url}")
                
                return pages_url
            else:
                print(f"❌ 업로드 실패: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 오류: {str(e)}")
            return None
    
    def create_notion_page(self, title: str, image_urls: List[str], 
                          description: str = "", keywords: List[str] = None) -> Optional[str]:
        """Notion 페이지 생성"""
        try:
            print(f"\n📝 Notion 페이지 생성 중...")
            
            # 속성
            properties = {
                "제목": {"title": [{"text": {"content": title}}]},
                "업로드일": {"date": {"start": datetime.now().isoformat()}},
                "이미지수": {"number": len(image_urls)},
                "설명": {"rich_text": [{"text": {"content": description}}]},
                "GitHub링크": {"url": image_urls[0] if image_urls else ""},
                "상태": {"select": {"name": "공개"}}
            }
            
            if keywords:
                properties["키워드"] = {"multi_select": [{"name": k} for k in keywords]}
            
            # 페이지 내용
            children = [
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "icon": {"type": "emoji", "emoji": "📸"},
                        "rich_text": [{"type": "text", "text": {"content": "GitHub Pages를 통해 제공되는 카드뉴스입니다."}}]
                    }
                },
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {"rich_text": [{"type": "text", "text": {"content": title}}]}
                }
            ]
            
            if description:
                children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": description}}]}
                })
            
            children.append({"object": "block", "type": "divider", "divider": {}})
            
            # 이미지 추가
            for i, url in enumerate(image_urls, 1):
                children.extend([
                    {
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {"rich_text": [{"type": "text", "text": {"content": f"📄 슬라이드 {i}"}}]}
                    },
                    {
                        "object": "block",
                        "type": "image",
                        "image": {"type": "external", "external": {"url": url}}
                    }
                ])
            
            # 페이지 생성
            new_page = self.notion.pages.create(
                parent={"database_id": self.card_news_db_id},
                properties=properties,
                children=children
            )
            
            page_id = new_page['id']
            print(f"✅ Notion 페이지 생성 완료!")
            print(f"🔗 https://notion.so/{page_id.replace('-', '')}")
            
            return page_id
            
        except Exception as e:
            print(f"❌ Notion 오류: {str(e)}")
            return None
    
    def upload_folder(self, folder_path: str, title: str = None,
                     description: str = "", keywords: List[str] = None) -> bool:
        """폴더 전체 업로드"""
        try:
            if not os.path.exists(folder_path):
                print(f"❌ 폴더 없음: {folder_path}")
                return False
            
            title = title or os.path.basename(folder_path)
            
            print(f"\n" + "="*60)
            print(f"📁 카드뉴스 업로드 (GitHub Pages)")
            print(f"📌 제목: {title}")
            print("="*60)
            
            # 이미지 찾기
            image_files = []
            for file in sorted(os.listdir(folder_path)):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    image_files.append(os.path.join(folder_path, file))
            
            if not image_files:
                print("❌ 이미지 없음")
                return False
            
            print(f"🖼️ 이미지: {len(image_files)}개 발견")
            
            # 업로드
            uploaded_urls = []
            for i, img_path in enumerate(image_files, 1):
                safe_name = f"slide_{i:02d}{os.path.splitext(img_path)[1]}"
                url = self.upload_image_to_github(img_path, safe_name)
                if url:
                    uploaded_urls.append(url)
            
            if not uploaded_urls:
                print("❌ 업로드 실패")
                return False
            
            print(f"\n⏳ GitHub Pages 배포 대기중... (30초)")
            time.sleep(30)  # GitHub Pages 배포 대기
            
            # Notion 페이지 생성
            page_id = self.create_notion_page(title, uploaded_urls, description, keywords)
            
            if page_id:
                print(f"\n🎉 완료!")
                print(f"📌 이미지: {len(uploaded_urls)}개")
                print(f"📄 Notion: https://notion.so/{page_id.replace('-', '')}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ 오류: {str(e)}")
            return False


if __name__ == "__main__":
    uploader = CardNewsUploaderPages()
    
    # 테스트
    uploader.upload_folder(
        "card_news/images/sample_card_news",
        title="GitHub Pages 테스트 카드뉴스",
        description="Private 리포지토리 + GitHub Pages 활용",
        keywords=["테스트", "GitHub Pages"]
    )
