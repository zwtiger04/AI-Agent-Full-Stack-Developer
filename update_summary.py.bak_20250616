#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
요약 페이지 업데이트 모듈 - 최종 수정 버전
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Windows의 요약 페이지 경로
SUMMARY_PATH = "/mnt/c/Users/KJ/Desktop/EnhancedCardNews/improved_summary.html"

# 카테고리별 색상 클래스 매핑
CATEGORY_CLASSES = {
    '태양광': 'category-solar',
    '풍력': 'category-wind',
    '해상풍력': 'category-wind',
    'ESS': 'category-ess',
    'VPP': 'category-vpp',
    '전력중개': 'category-vpp',
    '정책': 'category-policy',
    '기후에너지부': 'category-policy',
    '재생에너지': 'category-renewable',
    'AI': 'category-tech',
    'PPA': 'category-tech'
}

def get_category_class(keywords: list) -> str:
    """키워드 기반 카테고리 클래스 결정"""
    for keyword in keywords:
        for key, class_name in CATEGORY_CLASSES.items():
            if key in keyword:
                return class_name
    return 'category-general'

def get_category_label(keywords: list) -> str:
    """카테고리 레이블 결정"""
    priority_order = ['ESS', 'VPP', '태양광', '풍력', '해상풍력', '정책', 'AI', 'PPA', '재생에너지']
    for priority in priority_order:
        for keyword in keywords:
            if priority in keyword:
                return priority
    return '전력산업'

def add_to_summary(article: Dict, file_path: str, base_path: Optional[str] = None) -> bool:
    """요약 페이지에 새 카드 추가"""
    try:
        # 요약 페이지 경로 결정
        if base_path is None:
            summary_path = SUMMARY_PATH
        else:
            if 'detailed' in base_path:
                parent_dir = os.path.dirname(base_path)
                summary_path = os.path.join(parent_dir, "improved_summary.html")
            else:
                summary_path = SUMMARY_PATH
            
        print(f"📍 요약 페이지 경로: {summary_path}")
        print(f"📍 파일 존재 여부: {os.path.exists(summary_path)}")
        
        # 요약 페이지 읽기
        with open(summary_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 존재하는지 확인
        if article['title'] in content:
            print(f"⚠️ 이미 요약 페이지에 존재: {article['title']}")
            return False
        
        # 카테고리 결정
        keywords = article.get('keywords', [])
        category_class = get_category_class(keywords)
        category_label = get_category_label(keywords)
        
        # 날짜 형식화
        today = datetime.now().strftime('%-m월 %-d일')
        
        # 파일명에서 상대 경로 생성
        if file_path.startswith('/mnt/c/Users/KJ/Desktop/EnhancedCardNews/'):
            rel_path = file_path.replace('/mnt/c/Users/KJ/Desktop/EnhancedCardNews/', '')
        else:
            rel_path = 'detailed/' + os.path.basename(file_path)
        
        # 새 카드 HTML 생성
        new_card = f'''
            <!-- 기사: {article['title'][:50]}... -->
            <div class="news-card" onclick="window.location.href='{rel_path}'">
                <span class="card-category {category_class}">{category_label}</span>
                <h3 class="card-title">{article['title']}</h3>
                <p class="card-summary">
                    {article.get('summary', '')}
                </p>
                <div class="card-meta">
                    <span>전기신문</span>
                    <a href="#" class="read-more">자세히 보기 →</a>
                </div>
            </div>'''
        
        # news-grid 끝 찾기
        grid_end = content.rfind('</div>', content.rfind('news-grid'))
        if grid_end == -1:
            print("❌ news-grid 끝을 찾을 수 없습니다.")
            return False
        
        # 새 카드 삽입
        new_content = content[:grid_end] + new_card + '\n        ' + content[grid_end:]
        
        # 파일 저장
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 요약 페이지에 추가됨: {article['title']}")
        return True
        
    except Exception as e:
        print(f"❌ 요약 페이지 업데이트 실패: {e}")
        return False

def update_summary_date():
    """요약 페이지의 날짜 업데이트"""
    try:
        with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 현재 날짜로 업데이트
        today = datetime.now().strftime('%Y년 %-m월 %-d일')
        
        # 타이틀 업데이트
        content = re.sub(r'<title>전력산업 카드뉴스 - \d{4}년 \d{1,2}월 \d{1,2}일</title>', 
                        f'<title>전력산업 카드뉴스 - {today}</title>', content)
        
        # subtitle 업데이트 - 정확한 패턴으로
        content = re.sub(r'<p class="subtitle">\d{4}년 \d{1,2}월 \d{1,2}일 \| 에너지 전환의 현장을 전합니다</p>', 
                        f'<p class="subtitle">{today} | 에너지 전환의 현장을 전합니다</p>', content)
        
        with open(SUMMARY_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ 요약 페이지 날짜 업데이트: {today}")
        
    except Exception as e:
        print(f"❌ 날짜 업데이트 실패: {e}")

if __name__ == "__main__":
    # 테스트용
    test_article = {
        'title': '최종 수정 테스트 기사',
        'summary': '최종 수정된 버전 테스트 요약입니다.',
        'keywords': ['ESS', '재생에너지']
    }
    add_to_summary(test_article, '/mnt/c/Users/KJ/Desktop/EnhancedCardNews/detailed/test_final.html')
