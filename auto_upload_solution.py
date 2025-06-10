#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카드뉴스 자동 업로드 솔루션 - GitHub Pages 활용
"""

import os
import shutil
from datetime import datetime
from notion.notion_client import NotionClient

class AutoUploadSolution:
    def __init__(self):
        self.notion = NotionClient()
        self.output_dir = "/home/zwtiger/AI-Agent-Full-Stack-Developer/card_news_output"
        
    def create_github_pages_structure(self):
        """GitHub Pages용 디렉토리 구조 생성"""
        # docs 폴더 생성 (GitHub Pages용)
        docs_dir = "/home/zwtiger/AI-Agent-Full-Stack-Developer/docs"
        os.makedirs(docs_dir, exist_ok=True)
        
        # card_news 폴더
        card_news_dir = os.path.join(docs_dir, "card_news")
        os.makedirs(card_news_dir, exist_ok=True)
        
        # 오늘 날짜 폴더
        today = datetime.now().strftime("%Y%m%d")
        today_dir = os.path.join(card_news_dir, today)
        os.makedirs(today_dir, exist_ok=True)
        
        # 이미지 복사
        image_urls = []
        for filename in sorted(os.listdir(self.output_dir)):
            if filename.startswith(today) and filename.endswith('.png'):
                src = os.path.join(self.output_dir, filename)
                dst = os.path.join(today_dir, filename)
                shutil.copy2(src, dst)
                
                # GitHub Pages URL 생성 (저장소 설정 후 사용 가능)
                # https://zwtiger04.github.io/AI-Agent-Full-Stack-Developer/card_news/20250608/filename.png
                github_pages_url = f"https://zwtiger04.github.io/AI-Agent-Full-Stack-Developer/card_news/{today}/{filename}"
                image_urls.append({
                    'filename': filename,
                    'url': github_pages_url,
                    'local_path': dst
                })
                print(f"✅ 복사 완료: {filename}")
        
        # index.html 생성
        self.create_index_html(today_dir, image_urls)
        
        return image_urls, today_dir
    
    def create_index_html(self, directory, image_urls):
        """이미지 갤러리 HTML 페이지 생성"""
        html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>전력산업 카드뉴스</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 40px;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card img {
            width: 100%;
            height: auto;
            display: block;
        }
        .card-title {
            padding: 15px;
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗞️ 전력산업 카드뉴스 - """ + datetime.now().strftime('%Y년 %m월 %d일') + """</h1>
        <div class="gallery">
"""
        
        for img in image_urls:
            title = img['filename'].split('_')[-1].replace('.png', '').replace('_', ' ')
            html_content += f"""
            <div class="card">
                <img src="{img['filename']}" alt="{title}">
                <div class="card-title">{title}</div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
</body>
</html>
"""
        
        # HTML 파일 저장
        with open(os.path.join(directory, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ index.html 생성 완료")
    
    def create_commit_script(self, today_dir):
        """Git 커밋 스크립트 생성"""
        script_content = f"""#!/bin/bash
# 카드뉴스 GitHub 업로드 스크립트

cd /home/zwtiger/AI-Agent-Full-Stack-Developer

# Git 추가
git add docs/card_news/
git add {today_dir}

# 커밋
git commit -m "Add card news for {datetime.now().strftime('%Y-%m-%d')}"

# 푸시
git push origin main

echo "✅ GitHub 업로드 완료!"
echo "📍 GitHub Pages에서 확인: https://zwtiger04.github.io/AI-Agent-Full-Stack-Developer/card_news/{datetime.now().strftime('%Y%m%d')}/"
"""
        
        script_path = "/home/zwtiger/AI-Agent-Full-Stack-Developer/upload_to_github.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        os.chmod(script_path, 0o755)
        print(f"✅ 업로드 스크립트 생성: {script_path}")
        
        return script_path
    
    def create_notion_page_with_local_paths(self, image_urls):
        """로컬 경로를 사용해 노션 페이지 생성 (수동 업로드 안내)"""
        try:
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
            
            # 콘텐츠 블록
            blocks = [
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "🗞️ 전력산업 주간 카드뉴스"}
                        }]
                    }
                },
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "icon": {"emoji": "📌"},
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "이미지 업로드 방법:\n1. 아래 명령어를 실행하여 GitHub에 업로드\n2. 또는 각 이미지 위치에 드래그 앤 드롭으로 업로드"}
                        }]
                    }
                },
                {
                    "object": "block",
                    "type": "code",
                    "code": {
                        "language": "bash",
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "cd /home/zwtiger/AI-Agent-Full-Stack-Developer\n./upload_to_github.sh"}
                        }]
                    }
                }
            ]
            
            # 각 이미지 위치 표시
            for img in image_urls:
                blocks.extend([
                    {
                        "object": "block",
                        "type": "divider",
                        "divider": {}
                    },
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": img['filename'].split('_')[-1].replace('.png', '')}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": f"📁 로컬 경로: {img['local_path']}\n🔗 GitHub Pages URL (업로드 후): {img['url']}"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "[ 여기에 이미지 드래그 앤 드롭 ]"},
                                "annotations": {
                                    "italic": True,
                                    "color": "gray"
                                }
                            }]
                        }
                    }
                ])
            
            # 블록 추가
            self.notion.client.blocks.children.append(
                block_id=page_id,
                children=blocks
            )
            
            print(f"\n✅ 노션 페이지 생성 완료!")
            print(f"📍 페이지: https://notion.so/{page_id.replace('-', '')}")
            
            return page_id
            
        except Exception as e:
            print(f"❌ 노션 페이지 생성 오류: {str(e)}")
            return None


def main():
    print("=" * 60)
    print("🚀 카드뉴스 자동 업로드 솔루션")
    print("=" * 60)
    
    solution = AutoUploadSolution()
    
    # 1. GitHub Pages 구조 생성
    print("\n📁 GitHub Pages 구조 생성 중...")
    image_urls, today_dir = solution.create_github_pages_structure()
    
    # 2. Git 커밋 스크립트 생성
    print("\n📝 업로드 스크립트 생성 중...")
    script_path = solution.create_commit_script(today_dir)
    
    # 3. 노션 페이지 생성
    print("\n📄 노션 페이지 생성 중...")
    page_id = solution.create_notion_page_with_local_paths(image_urls)
    
    print("\n" + "=" * 60)
    print("✅ 완료! 다음 단계를 진행하세요:")
    print("=" * 60)
    print("\n1️⃣ GitHub에 업로드하려면:")
    print(f"   bash {script_path}")
    print("\n2️⃣ 또는 노션 페이지에서 직접 이미지 업로드:")
    print(f"   https://notion.so/{page_id.replace('-', '')}")
    print("\n3️⃣ GitHub Pages 활성화 (저장소 Settings > Pages):")
    print("   Source: Deploy from a branch")
    print("   Branch: main /docs")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
