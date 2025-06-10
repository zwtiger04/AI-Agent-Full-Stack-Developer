#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖼️ 카드뉴스 GitHub 업로더 & Notion 연동 시스템 v2
- URL 인코딩 문제 해결
- 카드뉴스 전용 데이터베이스 사용
"""

import os
import base64
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
from dotenv import load_dotenv
from notion_client import Client
from urllib.parse import quote
import re

# 환경변수 로드
load_dotenv()

class CardNewsUploaderV2:
    """🚀 개선된 카드뉴스 업로더"""
    
    def __init__(self):
        """초기화: GitHub와 Notion 설정"""
        # GitHub 설정
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_repo = os.getenv('GITHUB_REPO', 'zwtiger04/AI-Agent-Full-Stack-Developer')
        self.github_branch = os.getenv('GITHUB_BRANCH', 'main')
        
        # GitHub API 헤더
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        # Notion 클라이언트
        self.notion = Client(auth=os.getenv('NOTION_API_KEY'))
        self.card_news_db_id = os.getenv('CARD_NEWS_DATABASE_ID', '20c2360b-2603-8175-bcf6-e6d134f4d7a8')
        
        print(f"✅ CardNewsUploaderV2 초기화 완료!")
        print(f"📌 GitHub 저장소: {self.github_repo}")
        print(f"📌 카드뉴스 DB: {self.card_news_db_id}")
    
    def safe_filename(self, filename: str) -> str:
        """파일명을 안전하게 변환 (영문/숫자만)"""
        # 확장자 분리
        name, ext = os.path.splitext(filename)
        
        # 한글을 영문으로 변환
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        
        # 연속된 언더스코어 제거
        safe_name = re.sub(r'_+', '_', safe_name)
        
        # 앞뒤 언더스코어 제거
        safe_name = safe_name.strip('_')
        
        # 비어있으면 기본값
        if not safe_name:
            safe_name = f"image_{datetime.now().strftime('%H%M%S')}"
        
        return f"{safe_name}{ext}"
    
    def upload_image_to_github(self, image_path: str, custom_name: str = None) -> Optional[str]:
        """이미지를 GitHub에 업로드 (안전한 파일명 사용)"""
        try:
            if not os.path.exists(image_path):
                print(f"❌ 파일을 찾을 수 없습니다: {image_path}")
                return None
            
            # 안전한 파일명 생성
            original_name = os.path.basename(image_path)
            safe_name = custom_name or self.safe_filename(original_name)
            
            # GitHub 경로 생성
            date_folder = datetime.now().strftime('%Y%m%d')
            github_path = f"card_news/{date_folder}/{safe_name}"
            
            print(f"📤 업로드 중: {original_name} → {safe_name}")
            
            # 이미지 파일을 base64로 인코딩
            with open(image_path, 'rb') as image_file:
                content_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            
            # GitHub API URL
            api_url = f"https://api.github.com/repos/{self.github_repo}/contents/{github_path}"
            
            # 업로드 데이터
            data = {
                "message": f"📸 카드뉴스 이미지 업로드: {safe_name}",
                "content": content_base64,
                "branch": self.github_branch
            }
            
            # GitHub에 업로드
            response = requests.put(api_url, headers=self.headers, json=data)
            
            if response.status_code in [201, 200]:
                # raw URL 생성 (URL 인코딩 없이)
                raw_url = f"https://raw.githubusercontent.com/{self.github_repo}/{self.github_branch}/{github_path}"
                
                print(f"✅ 업로드 성공: {safe_name}")
                print(f"🔗 URL: {raw_url}")
                
                return raw_url
            else:
                print(f"❌ 업로드 실패: {response.status_code}")
                print(f"❌ 오류: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 업로드 중 오류: {str(e)}")
            return None
    
    def create_card_news_page(self, title: str, image_urls: List[str], 
                             description: str = "", keywords: List[str] = None) -> Optional[str]:
        """카드뉴스 전용 데이터베이스에 페이지 생성"""
        try:
            print(f"📝 카드뉴스 페이지 생성 중: {title}")
            
            # 페이지 속성 설정
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
            
            # 페이지 내용 생성
            children = []
            
            # 제목
            children.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": title}}]
                }
            })
            
            # 설명
            if description:
                children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": description}}]
                    }
                })
            
            # 구분선
            children.append({"object": "block", "type": "divider", "divider": {}})
            
            # 이미지 추가
            for i, url in enumerate(image_urls, 1):
                # 이미지 번호 헤딩
                children.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": f"슬라이드 {i}"}}]
                    }
                })
                
                # 이미지
                children.append({
                    "object": "block",
                    "type": "image",
                    "image": {"type": "external", "external": {"url": url}}
                })
                
                # 이미지 링크 (백업용)
                children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": f"이미지 링크: ", "link": None}
                        }, {
                            "type": "text",
                            "text": {"content": url, "link": {"url": url}}
                        }]
                    }
                })
                
                # 구분선 (마지막 제외)
                if i < len(image_urls):
                    children.append({"object": "block", "type": "divider", "divider": {}})
            
            # Notion 페이지 생성
            new_page = self.notion.pages.create(
                parent={"database_id": self.card_news_db_id},
                properties=properties,
                children=children
            )
            
            page_id = new_page['id']
            print(f"✅ 카드뉴스 페이지 생성 완료!")
            print(f"🔗 https://notion.so/{page_id.replace('-', '')}")
            
            return page_id
            
        except Exception as e:
            print(f"❌ 페이지 생성 중 오류: {str(e)}")
            return None
    
    def upload_card_news_folder(self, folder_path: str, title: str = None,
                               description: str = "", keywords: List[str] = None) -> bool:
        """폴더의 이미지들을 업로드하고 카드뉴스 페이지 생성"""
        try:
            if not os.path.exists(folder_path):
                print(f"❌ 폴더를 찾을 수 없습니다: {folder_path}")
                return False
            
            # 제목 기본값
            if title is None:
                title = os.path.basename(folder_path)
            
            print(f"\n📁 카드뉴스 업로드 시작: {folder_path}")
            print(f"📌 제목: {title}")
            
            # 이미지 파일 찾기
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            image_files = []
            
            for file in sorted(os.listdir(folder_path)):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(folder_path, file))
            
            if not image_files:
                print(f"❌ 이미지 파일이 없습니다.")
                return False
            
            print(f"🖼️ 발견된 이미지: {len(image_files)}개")
            
            # 이미지 업로드
            uploaded_urls = []
            for i, image_path in enumerate(image_files, 1):
                # 번호_확장자 형식으로 파일명 생성
                ext = os.path.splitext(image_path)[1]
                safe_name = f"slide_{i:02d}{ext}"
                
                url = self.upload_image_to_github(image_path, safe_name)
                if url:
                    uploaded_urls.append(url)
                else:
                    print(f"⚠️ 업로드 실패: {os.path.basename(image_path)}")
            
            if not uploaded_urls:
                print("❌ 업로드된 이미지가 없습니다.")
                return False
            
            # 카드뉴스 페이지 생성
            page_id = self.create_card_news_page(title, uploaded_urls, description, keywords)
            
            if page_id:
                print(f"\n🎉 카드뉴스 업로드 완료!")
                print(f"📌 이미지: {len(uploaded_urls)}개")
                print(f"📄 Notion: https://notion.so/{page_id.replace('-', '')}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")
            return False


def main():
    """메인 함수"""
    print("="*60)
    print("🖼️ 카드뉴스 GitHub-Notion 연동 v2")
    print("="*60)
    
    uploader = CardNewsUploaderV2()
    
    # 테스트 업로드
    uploader.upload_card_news_folder(
        "card_news/images/sample_card_news",
        title="2025년 6월 전력산업 카드뉴스 (개선판)",
        description="이미지 연결 문제를 해결한 버전입니다.",
        keywords=["테스트", "카드뉴스", "전력산업"]
    )


if __name__ == "__main__":
    main()
