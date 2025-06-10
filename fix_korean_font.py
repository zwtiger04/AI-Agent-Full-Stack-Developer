#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카드 뉴스 생성기 한글 폰트 문제 수정
"""

# 현재 어떤 폰트가 사용 가능한지 확인
from PIL import ImageFont
import os

print("🔍 폰트 디렉토리 확인...")

# 사용 가능한 폰트 경로들
font_paths = [
    "/home/zwtiger/.fonts/D2Coding-Ver1.3.2-20180524.ttf",
    "/home/zwtiger/.fonts/D2CodingBold-Ver1.3.2-20180524.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
]

for path in font_paths:
    if os.path.exists(path):
        try:
            font = ImageFont.truetype(path, 24)
            print(f"✅ 사용 가능: {path}")
        except Exception as e:
            print(f"❌ 로드 실패: {path} - {e}")
    else:
        print(f"❌ 파일 없음: {path}")

# 한글 지원 폰트 확인
print("\n🔍 시스템 한글 폰트 검색...")
import subprocess
result = subprocess.run(['fc-list', ':lang=ko'], capture_output=True, text=True)
if result.stdout:
    print("한글 폰트 발견:")
    print(result.stdout)
else:
    print("한글 폰트 없음")
