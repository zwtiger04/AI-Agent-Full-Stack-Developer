#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 GitHub Pages URL 변환기
Private 리포지토리의 이미지를 GitHub Pages URL로 변환
"""

def convert_to_github_pages_url(raw_url: str) -> str:
    """
    Raw GitHub URL을 GitHub Pages URL로 변환
    
    예시:
    입력: https://raw.githubusercontent.com/zwtiger04/AI-Agent-Full-Stack-Developer/main/card_news/20250608/slide_01.png
    출력: https://zwtiger04.github.io/AI-Agent-Full-Stack-Developer/card_news/20250608/slide_01.png
    """
    if "raw.githubusercontent.com" in raw_url:
        # URL 파싱
        parts = raw_url.split('/')
        username = parts[3]
        repo_name = parts[4]
        branch = parts[5]  # main
        file_path = '/'.join(parts[6:])
        
        # GitHub Pages URL 생성
        pages_url = f"https://{username}.github.io/{repo_name}/{file_path}"
        return pages_url
    return raw_url

# 테스트
test_urls = [
    "https://raw.githubusercontent.com/zwtiger04/AI-Agent-Full-Stack-Developer/main/card_news/20250608/slide_01.png",
    "https://raw.githubusercontent.com/zwtiger04/AI-Agent-Full-Stack-Developer/main/card_news/20250608/slide_02.png",
    "https://raw.githubusercontent.com/zwtiger04/AI-Agent-Full-Stack-Developer/main/card_news/20250608/slide_03.png"
]

print("🔄 GitHub Pages URL 변환 예시:\n")
for url in test_urls:
    pages_url = convert_to_github_pages_url(url)
    print(f"원본: {url}")
    print(f"변환: {pages_url}\n")

print("📌 GitHub Pages가 활성화되면 위 URL들로 이미지에 접근할 수 있습니다!")
