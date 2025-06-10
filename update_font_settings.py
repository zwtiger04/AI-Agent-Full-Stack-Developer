#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카드 뉴스 생성기 폰트 설정 업데이트
"""

import os

# card_news_generator.py 파일 읽기
file_path = '/home/zwtiger/AI-Agent-Full-Stack-Developer/card_news_generator.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 폰트 경로 부분 수정
new_font_section = '''# 한글 폰트 경로 설정
import os
import platform

# 시스템별 폰트 경로 설정
if platform.system() == 'Linux':
    # WSL/Linux에서 사용자 폰트 경로 확인
    user_font_dir = os.path.expanduser('~/.fonts')
    if os.path.exists(os.path.join(user_font_dir, 'D2Coding-Ver1.3.2-20180524.ttf')):
        FONT_REGULAR = os.path.join(user_font_dir, 'D2Coding-Ver1.3.2-20180524.ttf')
        FONT_BOLD = os.path.join(user_font_dir, 'D2CodingBold-Ver1.3.2-20180524.ttf')
    else:
        # 프로젝트 내 폰트 폴더
        FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
        FONT_REGULAR = os.path.join(FONT_DIR, 'NotoSansKR-Regular.otf')
        FONT_BOLD = os.path.join(FONT_DIR, 'NotoSansKR-Bold.otf')
else:
    # 기본 폰트 설정
    FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
    FONT_REGULAR = os.path.join(FONT_DIR, 'NotoSansKR-Regular.otf')
    FONT_BOLD = os.path.join(FONT_DIR, 'NotoSansKR-Bold.otf')'''

# matplotlib 한글 설정 추가
matplotlib_settings = '''        # matplotlib 한글 설정
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
        
        # 설치된 한글 폰트 확인
        font_list = fm.findSystemFonts(fontpaths=None)
        d2coding_fonts = [f for f in font_list if 'D2Coding' in f]
        
        if d2coding_fonts:
            # D2Coding 폰트가 있으면 사용
            font_path = d2coding_fonts[0]
            font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
            plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
        else:
            # 없으면 기본 설정 유지
            plt.rcParams['font.family'] = 'DejaVu Sans'
            
        plt.rcParams['axes.unicode_minus'] = False'''

# 기존 폰트 설정 부분 찾아서 교체
import re

# 폰트 경로 설정 부분 교체
pattern1 = r'# 한글 폰트 경로 설정\nFONT_DIR.*?\nFONT_BOLD.*?\.otf\'\n'
content = re.sub(pattern1, new_font_section + '\n', content, flags=re.DOTALL)

# matplotlib 설정 부분 찾아서 교체
pattern2 = r'# matplotlib 한글 설정\n\s+plt\.rcParams\[\'font\.family\'\].*?\n\s+plt\.rcParams\[\'axes\.unicode_minus\'\].*?\n'
replacement2 = matplotlib_settings + '\n'
content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)

# 파일 저장
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 폰트 설정 업데이트 완료!")
