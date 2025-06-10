#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 카드뉴스 GitHub-Notion 연동 실행 스크립트
"""

import os
import sys
from datetime import datetime

# .env 파일 체크
if not os.path.exists('.env'):
    print("❌ .env 파일이 없습니다!")
    sys.exit(1)

# GitHub PAT 체크
with open('.env', 'r') as f:
    env_content = f.read()
    if 'GITHUB_TOKEN' not in env_content:
        print("❌ .env 파일에 GITHUB_TOKEN이 없습니다!")
        print("👉 추가 방법: echo 'GITHUB_TOKEN=ghp_여기에_토큰' >> .env")
        sys.exit(1)

# 카드뉴스 업로더 임포트
try:
    from card_news_uploader import CardNewsUploader
except ImportError:
    print("❌ card_news_uploader.py 파일을 찾을 수 없습니다!")
    sys.exit(1)

def upload_sample():
    """샘플 카드뉴스 업로드"""
    print("\n" + "="*60)
    print("🖼️ 카드뉴스 GitHub-Notion 연동 시작!")
    print("="*60 + "\n")
    
    # 업로더 초기화
    uploader = CardNewsUploader()
    
    # 샘플 폴더 확인
    sample_folder = "card_news/images/sample_card_news"
    if not os.path.exists(sample_folder):
        print(f"📁 {sample_folder} 폴더를 생성합니다...")
        os.makedirs(sample_folder, exist_ok=True)
        print("❗ 이 폴더에 카드뉴스 이미지를 넣어주세요!")
        print("   지원 형식: .jpg, .png, .gif, .webp")
        print("   예시: 01_표지.png, 02_내용.png, 03_결론.png")
        return
    
    # 이미지 확인
    images = [f for f in os.listdir(sample_folder) 
              if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
    
    if not images:
        print(f"❌ {sample_folder} 폴더에 이미지가 없습니다!")
        print("   이미지를 추가한 후 다시 실행해주세요.")
        return
    
    print(f"✅ 발견된 이미지: {len(images)}개")
    for img in sorted(images):
        print(f"   - {img}")
    
    # 업로드 실행
    today = datetime.now().strftime("%Y년 %m월 %d일")
    success = uploader.upload_card_news_folder(
        folder_path=sample_folder,
        title=f"{today} 전력산업 카드뉴스",
        description="GitHub-Notion 연동 테스트 카드뉴스입니다.",
        keywords=["테스트", "카드뉴스", "전력산업"]
    )
    
    if success:
        print("\n🎉 성공적으로 업로드되었습니다!")
        print("📌 Notion에서 확인해보세요!")
    else:
        print("\n❌ 업로드에 실패했습니다.")

def upload_custom(folder_path):
    """사용자 지정 폴더 업로드"""
    if not os.path.exists(folder_path):
        print(f"❌ 폴더를 찾을 수 없습니다: {folder_path}")
        return
    
    # 업로더 초기화
    uploader = CardNewsUploader()
    
    # 제목 입력
    title = input("📝 카드뉴스 제목: ").strip()
    if not title:
        title = os.path.basename(folder_path)
    
    # 설명 입력
    description = input("📝 설명 (Enter로 건너뛰기): ").strip()
    
    # 키워드 입력
    keywords_input = input("🏷️ 키워드 (쉼표로 구분): ").strip()
    keywords = [k.strip() for k in keywords_input.split(',')] if keywords_input else []
    
    # 업로드 실행
    success = uploader.upload_card_news_folder(
        folder_path=folder_path,
        title=title,
        description=description,
        keywords=keywords
    )
    
    if success:
        print("\n🎉 성공적으로 업로드되었습니다!")
    else:
        print("\n❌ 업로드에 실패했습니다.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 사용자 지정 폴더
        upload_custom(sys.argv[1])
    else:
        # 샘플 업로드
        upload_sample()
