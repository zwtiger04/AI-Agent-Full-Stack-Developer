#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카드뉴스 이미지를 GitHub에 업로드하고 노션에 추가
"""

import os
import base64
import json
from datetime import datetime
from github import Github
from notion_client import Client
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

def upload_images_to_github():
    """생성된 카드뉴스 이미지를 GitHub에 업로드"""
    
    # GitHub 설정
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN이 설정되지 않았습니다.")
        print("1. GitHub에서 Personal Access Token을 생성하세요")
        print("2. .env 파일에 GITHUB_TOKEN=your_token 추가하세요")
        return None
    
    g = Github(github_token)
    repo_name = "zwtiger04/AI-Agent-Full-Stack-Developer"
    
    try:
        repo = g.get_repo(repo_name)
        print(f"✅ GitHub 저장소 연결: {repo_name}")
    except Exception as e:
        print(f"❌ GitHub 저장소 연결 실패: {e}")
        return None
    
    # 이미지 폴더 경로
    output_dir = "/home/zwtiger/AI-Agent-Full-Stack-Developer/card_news_output"
    
    # 오늘 날짜로 폴더 생성
    today = datetime.now().strftime("%Y%m%d")
    github_folder = f"card_news/{today}"
    
    uploaded_urls = []
    
    # 이미지 파일들 업로드
    for filename in sorted(os.listdir(output_dir)):
        if filename.startswith(today) and filename.endswith('.png'):
            filepath = os.path.join(output_dir, filename)
            
            # 파일 읽기
            with open(filepath, 'rb') as f:
                content = f.read()
            
            # GitHub 경로
            github_path = f"{github_folder}/{filename}"
            
            try:
                # 파일 업로드
                repo.create_file(
                    path=github_path,
                    message=f"Add card news image: {filename}",
                    content=content,
                    branch="main"
                )
                
                # Raw URL 생성
                raw_url = f"https://raw.githubusercontent.com/{repo_name}/main/{github_path}"
                uploaded_urls.append({
                    'filename': filename,
                    'url': raw_url
                })
                
                print(f"✅ 업로드 완료: {filename}")
                print(f"   URL: {raw_url}")
                
            except Exception as e:
                print(f"❌ 업로드 실패 ({filename}): {e}")
    
    return uploaded_urls

def update_notion_with_images(page_id, image_urls):
    """노션 페이지에 이미지 URL 추가"""
    
    notion_token = os.getenv('NOTION_API_KEY')
    notion = Client(auth=notion_token)
    
    # 이미지 블록 생성
    children_blocks = []
    
    for img_info in image_urls:
        # 이미지 제목
        children_blocks.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": img_info['filename'].split('_')[-1].replace('.png', '')}
                }]
            }
        })
        
        # 이미지 블록
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
    
    # 노션에 블록 추가
    try:
        notion.blocks.children.append(
            block_id=page_id,
            children=children_blocks
        )
        print(f"✅ 노션 페이지 업데이트 완료!")
    except Exception as e:
        print(f"❌ 노션 업데이트 실패: {e}")

if __name__ == "__main__":
    print("🚀 GitHub 업로드 시작...")
    
    # GitHub에 업로드
    uploaded_urls = upload_images_to_github()
    
    if uploaded_urls:
        print(f"\n📸 총 {len(uploaded_urls)}개 이미지 업로드 완료!")
        
        # 노션 페이지 ID (최근 생성된 페이지)
        notion_page_id = "20c2360b-2603-81b7-9280-e105e0730059"
        
        print(f"\n📝 노션 페이지에 이미지 추가 중...")
        update_notion_with_images(notion_page_id, uploaded_urls)
    else:
        print("❌ 이미지 업로드에 실패했습니다.")
