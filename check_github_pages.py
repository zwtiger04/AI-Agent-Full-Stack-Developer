#!/usr/bin/env python3
"""
🔍 GitHub Pages 상태 확인
"""

import requests
import time

def check_github_pages():
    """GitHub Pages 활성화 상태 확인"""
    
    print("🔍 GitHub Pages 상태 확인 중...\n")
    
    # 테스트할 URL들
    test_urls = [
        "https://zwtiger04.github.io/AI-Agent-Full-Stack-Developer/",
        "https://zwtiger04.github.io/AI-Agent-Full-Stack-Developer/card_news/20250608/slide_01.png"
    ]
    
    for url in test_urls:
        print(f"확인 중: {url}")
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ 성공! (상태 코드: {response.status_code})")
            elif response.status_code == 404:
                print(f"❌ 실패 - 404 Not Found")
                print("   → GitHub Pages가 아직 활성화되지 않았거나 배포 중입니다")
            else:
                print(f"⚠️  상태 코드: {response.status_code}")
        except Exception as e:
            print(f"❌ 연결 실패: {str(e)}")
        print()
    
    print("\n📌 GitHub Pages 설정 방법:")
    print("1. https://github.com/zwtiger04/AI-Agent-Full-Stack-Developer/settings/pages")
    print("2. Source → Deploy from a branch → main → Save")
    print("3. 10분 정도 기다린 후 다시 확인")

if __name__ == "__main__":
    check_github_pages()
