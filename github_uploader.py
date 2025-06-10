#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 자동 업로드 + 노션 연동
"""

import os
import base64
from datetime import datetime
import requests
from notion.notion_client import NotionClient
from dotenv import load_dotenv

load_dotenv()

class GitHubUploader:
    def __init__(self):
        # GitHub 설정
        self.owner = "zwtiger04"
        self.repo = "AI-Agent-Full-Stack-Developer"
        self.branch = "main"
        
        # 환경 변수에서 토큰 읽기 (없으면 None)
        self.token = os.getenv('GITHUB_TOKEN')
        
        # Notion 클라이언트
        self.notion = NotionClient()
        
    def check_github_access(self):
        """GitHub 접근 가능 여부 확인"""
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        headers = {}
        if self.token:
            headers['Authorization'] = f'token {self.token}'
            
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ GitHub 저장소 접근 가능: {self.owner}/{self.repo}")
            return True
        else:
            print(f"❌ GitHub 저장소 접근 불가: {response.status_code}")
            return False
    
    def upload_to_github(self, filepath, github_path):
        """파일을 GitHub에 업로드"""
        # 파일 읽기
        with open(filepath, 'rb') as f:
            content = base64.b64encode(f.read()).decode()
        
        # GitHub API URL
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{github_path}"
        
        # 요청 데이터
        data = {
            "message": f"Add card news image: {os.path.basename(filepath)}",
            "content": content,
            "branch": self.branch
        }
        
        # 헤더
        headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if self.token:
            headers['Authorization'] = f'token {self.token}'
        
        # 업로드 시도
        response = requests.put(url, json=data, headers=headers)
        
        if response.status_code == 201:
            raw_url = f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{self.branch}/{github_path}"
            print(f"✅ 업로드 성공: {raw_url}")
            return raw_url
        else:
            print(f"❌ 업로드 실패: {response.status_code}")
            print(f"응답: {response.json()}")
            return None
    
    def upload_card_news_images(self, output_dir):
        """카드뉴스 이미지들을 GitHub에 업로드하고 노션에 추가"""
        
        # 1. GitHub 접근 확인
        if not self.check_github_access():
            print("\n⚠️ GitHub 접근 불가. 다음 방법을 시도하세요:")
            print("1. .env 파일에 GITHUB_TOKEN 추가")
            print("2. 또는 수동으로 이미지 업로드")
            return None
        
        # 2. 이미지 파일 찾기
        timestamp = datetime.now().strftime("%Y%m%d")
        image_files = []
        
        for filename in sorted(os.listdir(output_dir)):
            if filename.startswith(timestamp) and filename.endswith('.png'):
                image_files.append(os.path.join(output_dir, filename))
        
        if not image_files:
            print("❌ 업로드할 이미지가 없습니다.")
            return None
        
        print(f"\n📸 {len(image_files)}개 이미지 발견")
        
        # 3. GitHub에 업로드
        uploaded_images = []
        github_folder = f"card_news/{timestamp}"
        
        for filepath in image_files:
            filename = os.path.basename(filepath)
            github_path = f"{github_folder}/{filename}"
            
            print(f"\n📤 업로드 중: {filename}")
            url = self.upload_to_github(filepath, github_path)
            
            if url:
                uploaded_images.append({
                    'name': filename.split('_')[-1].replace('.png', ''),
                    'url': url
                })
        
        if not uploaded_images:
            print("❌ 업로드된 이미지가 없습니다.")
            return None
        
        # 4. 노션에 추가
        return self.add_to_notion(uploaded_images)
    
    def add_to_notion(self, uploaded_images):
        """업로드된 이미지를 노션에 추가"""
        try:
            print("\n📝 노션 페이지 생성 중...")
            
            parent_page_id = "2002360b26038007a59fcda976552022"
            
            # 페이지 생성
            new_page = self.notion.client.pages.create(
                parent={
                    "type": "page_id",
                    "page_id": parent_page_id
                },
                properties={
                    "title": {
                        "title": [{
                            "text": {
                                "content": f"전력산업 카드뉴스 - {datetime.now().strftime('%Y년 %m월 %d일')}"
                            }
                        }]
                    }
                }
            )
            
            page_id = new_page['id']
            print(f"✅ 페이지 생성 완료: {page_id}")
            
            # 이미지 블록 추가
            blocks = []
            
            # 헤더
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "🗞️ 전력산업 주간 카드뉴스"}
                    }]
                }
            })
            
            # 각 이미지
            for img in uploaded_images:
                # 구분선
                blocks.append({
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                })
                
                # 이미지
                blocks.append({
                    "object": "block",
                    "type": "image",
                    "image": {
                        "type": "external",
                        "external": {"url": img['url']}
                    }
                })
            
            # 블록 추가
            self.notion.client.blocks.children.append(
                block_id=page_id,
                children=blocks
            )
            
            print(f"✅ 노션 업로드 완료!")
            print(f"📍 페이지: https://notion.so/{page_id.replace('-', '')}")
            
            return page_id
            
        except Exception as e:
            print(f"❌ 노션 업로드 오류: {str(e)}")
            return None


def main():
    print("=" * 60)
    print("🚀 GitHub 자동 업로드 시작")
    print("=" * 60)
    
    uploader = GitHubUploader()
    output_dir = "/home/zwtiger/AI-Agent-Full-Stack-Developer/card_news_output"
    
    uploader.upload_card_news_images(output_dir)


if __name__ == "__main__":
    main()
