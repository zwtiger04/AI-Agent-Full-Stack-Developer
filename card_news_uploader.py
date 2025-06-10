#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖼️ 카드뉴스 GitHub 업로더 & Notion 연동 시스템
- GitHub에 이미지 업로드
- 업로드된 이미지 URL을 Notion에 자동 추가
- 카드뉴스 관리 자동화
"""

import os
import base64
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
from dotenv import load_dotenv
from notion.notion_client import NotionClient

# 환경변수 로드
load_dotenv()

class CardNewsUploader:
    """🚀 카드뉴스를 GitHub에 업로드하고 Notion에 연동하는 클래스"""
    
    def __init__(self):
        """초기화: GitHub와 Notion 설정"""
        # GitHub 설정
        self.github_token = os.getenv('GITHUB_TOKEN')  # GitHub PAT
        self.github_repo = os.getenv('GITHUB_REPO', 'zwtiger04/AI-Agent-Full-Stack-Developer')
        self.github_branch = os.getenv('GITHUB_BRANCH', 'main')
        
        # GitHub API 헤더
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        # Notion 클라이언트
        self.notion = NotionClient()
        
        print(f"✅ CardNewsUploader 초기화 완료!")
        print(f"📌 GitHub 저장소: {self.github_repo}")
        print(f"📌 브랜치: {self.github_branch}")
    
    def upload_image_to_github(self, image_path: str, github_path: str = None) -> Optional[str]:
        """
        🖼️ 이미지를 GitHub에 업로드하고 URL을 반환
        
        Args:
            image_path: 로컬 이미지 파일 경로
            github_path: GitHub 저장소 내 경로 (기본값: card_news/날짜/파일명)
            
        Returns:
            str: 업로드된 이미지의 raw URL (Notion에서 사용 가능)
        """
        try:
            # 파일 존재 확인
            if not os.path.exists(image_path):
                print(f"❌ 파일을 찾을 수 없습니다: {image_path}")
                return None
            
            # GitHub 경로 생성 (기본값: card_news/YYYYMMDD/filename)
            if github_path is None:
                date_folder = datetime.now().strftime('%Y%m%d')
                filename = os.path.basename(image_path)
                github_path = f"card_news/{date_folder}/{filename}"
            
            print(f"📤 업로드 중: {image_path} → {github_path}")
            
            # 이미지 파일을 base64로 인코딩
            with open(image_path, 'rb') as image_file:
                content_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            
            # GitHub API URL
            api_url = f"https://api.github.com/repos/{self.github_repo}/contents/{github_path}"
            
            # 업로드 데이터
            data = {
                "message": f"📸 카드뉴스 이미지 업로드: {os.path.basename(image_path)}",
                "content": content_base64,
                "branch": self.github_branch
            }
            
            # GitHub에 업로드
            response = requests.put(api_url, headers=self.headers, json=data)
            
            if response.status_code in [201, 200]:  # 성공
                result = response.json()
                # raw URL 생성 (Notion에서 직접 사용 가능)
                raw_url = f"https://raw.githubusercontent.com/{self.github_repo}/{self.github_branch}/{github_path}"
                
                print(f"✅ 업로드 성공!")
                print(f"🔗 Raw URL: {raw_url}")
                print(f"📄 GitHub 페이지: {result['content']['html_url']}")
                
                return raw_url
            else:
                print(f"❌ 업로드 실패: {response.status_code}")
                print(f"❌ 오류 메시지: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 업로드 중 오류 발생: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return None
    
    def create_card_news_page(self, title: str, image_urls: List[str], 
                             description: str = "", keywords: List[str] = None) -> Optional[str]:
        """
        📄 Notion에 카드뉴스 페이지 생성
        
        Args:
            title: 카드뉴스 제목
            image_urls: GitHub에 업로드된 이미지 URL 리스트
            description: 카드뉴스 설명
            keywords: 관련 키워드 리스트
            
        Returns:
            str: 생성된 Notion 페이지 ID
        """
        try:
            # 현재 주차 데이터베이스 ID 가져오기
            database_id = self.notion.get_weekly_database_id()
            if not database_id:
                print("❌ Notion 데이터베이스를 찾을 수 없습니다.")
                return None
            
            print(f"📝 Notion 페이지 생성 중: {title}")
            
            # 페이지 속성 설정
            properties = {
                "제목": {
                    "title": [{"text": {"content": f"[카드뉴스] {title}"}}]
                },
                "출처": {
                    "rich_text": [{"text": {"content": "카드뉴스"}}]
                },
                "날짜": {
                    "date": {"start": datetime.now().isoformat()}
                },
                "한줄요약": {
                    "rich_text": [{"text": {"content": description[:200] if description else "카드뉴스 이미지"}}]
                },
                "바로가기": {
                    "url": image_urls[0] if image_urls else ""  # 첫 번째 이미지 URL
                }
            }
            
            # 키워드가 있으면 추가
            if keywords:
                properties["키워드"] = {
                    "multi_select": [{"name": keyword} for keyword in keywords]
                }
            
            # 페이지 내용 (이미지들 추가)
            children = []
            
            # 제목과 설명 추가
            children.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": title}}]
                }
            })
            
            if description:
                children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": description}}]
                    }
                })
            
            # 이미지들 추가
            for i, image_url in enumerate(image_urls):
                children.append({
                    "object": "block",
                    "type": "image",
                    "image": {
                        "type": "external",
                        "external": {"url": image_url}
                    }
                })
                
                # 이미지 사이에 구분선 추가 (마지막 이미지 제외)
                if i < len(image_urls) - 1:
                    children.append({
                        "object": "block",
                        "type": "divider",
                        "divider": {}
                    })
            
            # Notion 페이지 생성
            new_page = self.notion.client.pages.create(
                parent={"database_id": database_id},
                properties=properties,
                children=children
            )
            
            page_id = new_page['id']
            print(f"✅ Notion 페이지 생성 완료! (ID: {page_id})")
            
            # 페이지 URL 생성 (브라우저에서 열 수 있는 URL)
            page_url = f"https://www.notion.so/{page_id.replace('-', '')}"
            print(f"🔗 Notion 페이지: {page_url}")
            
            return page_id
            
        except Exception as e:
            print(f"❌ Notion 페이지 생성 중 오류: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return None
    
    def upload_card_news_folder(self, folder_path: str, title: str = None, 
                               description: str = "", keywords: List[str] = None) -> bool:
        """
        📁 폴더의 모든 이미지를 GitHub에 업로드하고 Notion 페이지 생성
        
        Args:
            folder_path: 이미지가 있는 폴더 경로
            title: 카드뉴스 제목 (기본값: 폴더명)
            description: 카드뉴스 설명
            keywords: 관련 키워드 리스트
            
        Returns:
            bool: 성공 여부
        """
        try:
            # 폴더 존재 확인
            if not os.path.exists(folder_path):
                print(f"❌ 폴더를 찾을 수 없습니다: {folder_path}")
                return False
            
            # 제목 기본값 설정
            if title is None:
                title = os.path.basename(folder_path)
            
            print(f"📁 카드뉴스 폴더 처리 중: {folder_path}")
            print(f"📌 제목: {title}")
            
            # 이미지 파일 찾기 (jpg, jpeg, png, gif)
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            image_files = []
            
            for file in sorted(os.listdir(folder_path)):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(folder_path, file))
            
            if not image_files:
                print(f"❌ 폴더에 이미지 파일이 없습니다.")
                return False
            
            print(f"🖼️ 발견된 이미지: {len(image_files)}개")
            
            # 각 이미지를 GitHub에 업로드
            uploaded_urls = []
            for image_path in image_files:
                url = self.upload_image_to_github(image_path)
                if url:
                    uploaded_urls.append(url)
                    print(f"✅ {os.path.basename(image_path)} 업로드 완료")
                else:
                    print(f"❌ {os.path.basename(image_path)} 업로드 실패")
            
            if not uploaded_urls:
                print("❌ 업로드된 이미지가 없습니다.")
                return False
            
            # Notion 페이지 생성
            page_id = self.create_card_news_page(title, uploaded_urls, description, keywords)
            
            if page_id:
                # 업로드 기록 저장
                self.save_upload_record(title, uploaded_urls, page_id)
                print(f"🎉 카드뉴스 업로드 완료!")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ 폴더 처리 중 오류: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return False
    
    def save_upload_record(self, title: str, image_urls: List[str], page_id: str):
        """📝 업로드 기록을 JSON 파일에 저장"""
        try:
            record_file = "card_news/upload_history.json"
            
            # 기존 기록 로드
            if os.path.exists(record_file):
                with open(record_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = []
            
            # 새 기록 추가
            new_record = {
                "title": title,
                "upload_date": datetime.now().isoformat(),
                "image_urls": image_urls,
                "notion_page_id": page_id,
                "image_count": len(image_urls)
            }
            
            history.append(new_record)
            
            # 저장
            os.makedirs(os.path.dirname(record_file), exist_ok=True)
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            
            print(f"📝 업로드 기록 저장 완료: {record_file}")
            
        except Exception as e:
            print(f"⚠️ 기록 저장 중 오류 (무시하고 계속): {str(e)}")


def main():
    """🚀 메인 실행 함수"""
    print("=" * 60)
    print("🖼️ 카드뉴스 GitHub 업로더 & Notion 연동")
    print("=" * 60)
    
    # 업로더 초기화
    uploader = CardNewsUploader()
    
    # 예시: 단일 이미지 업로드
    # image_url = uploader.upload_image_to_github("card_news/images/sample.jpg")
    # if image_url:
    #     uploader.create_card_news_page("테스트 카드뉴스", [image_url], "설명", ["전력", "뉴스"])
    
    # 예시: 폴더 전체 업로드
    # uploader.upload_card_news_folder(
    #     "card_news/images/20250608_전력산업",
    #     title="2025년 6월 전력산업 동향",
    #     description="이번 주 전력산업의 주요 이슈를 카드뉴스로 정리했습니다.",
    #     keywords=["전력산업", "재생에너지", "ESS", "VPP"]
    # )


if __name__ == "__main__":
    main()
