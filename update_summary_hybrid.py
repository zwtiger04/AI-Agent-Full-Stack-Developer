#!/usr/bin/env python3
"""
요약 페이지 업데이트 - 하이브리드 모드 (HTML + JSON)
기존 HTML도 유지하면서 새로운 JSON도 함께 업데이트
"""
import os
import json
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path
from summary_manager import SummaryManager

# 기존 경로 (HTML)
SUMMARY_PATH = "output/card_news/summary/improved_summary.html"

def add_to_summary(article: Dict, file_path: str, base_path: Optional[str] = None) -> bool:
    """
    요약 페이지에 새 기사 추가 (하이브리드 모드)
    1. 기존 HTML 업데이트 (기존 방식 유지)
    2. 새로운 JSON도 업데이트 (추가)
    """
    try:
        # 1. 기존 HTML 업데이트
        html_success = update_html_summary(article, file_path, base_path)
        
        # 2. 새로운 JSON 업데이트
        json_success = update_json_summary(article, file_path)
        
        # 둘 다 성공해야 True
        return html_success and json_success
        
    except Exception as e:
        print(f"❌ 요약 추가 실패: {str(e)}")
        return False

def update_html_summary(article: Dict, file_path: str, base_path: Optional[str] = None) -> bool:
    """기존 HTML 업데이트 로직"""
    try:
        # 상대 경로 계산
        if base_path:
            try:
                summary_path = Path(SUMMARY_PATH)
                file_path_obj = Path(file_path)
                
                if not summary_path.is_absolute():
                    summary_path = Path(base_path) / summary_path
                
                if summary_path.exists():
                    summary_path = summary_path.resolve()
                else:
                    summary_path = SUMMARY_PATH
            except:
                summary_path = SUMMARY_PATH
        else:
            summary_path = SUMMARY_PATH
        
        # HTML 파일 읽기
        if not os.path.exists(summary_path):
            print(f"⚠️  요약 파일이 없습니다: {summary_path}")
            return False
        
        with open(summary_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 중복 체크
        if article['title'] in html_content:
            print(f"ℹ️  이미 요약에 포함된 기사입니다: {article['title']}")
            return True
        
        # 카테고리 설정
        category = article.get('category', '기타')
        category_class = f"category-{category.lower().replace(' ', '-')}"
        category_label = category
        
        # 파일 경로 설정
        if base_path and os.path.exists(os.path.join(base_path, file_path)):
            rel_path = '../html/' + os.path.basename(file_path)
        else:
            rel_path = '../html/' + os.path.basename(file_path)
        
        # 새 카드 HTML 생성
        new_card = f'''
            <!-- 기사: {article['title'][:50]}... -->
            <div class="news-card" onclick="window.location.href='{rel_path}'">
                <span class="card-category {category_class}">{category_label}</span>
                <h3 class="card-title">{article['title']}</h3>
                <p class="card-summary">
                    {article.get('summary', '')}
                </p>
                <span class="card-date">{article.get('date', datetime.now().strftime('%Y-%m-%d'))}</span>
            </div>
'''
        
        # 카드 컨테이너 끝 부분 찾기
        insert_position = html_content.rfind('</div>', 0, html_content.rfind('</body>'))
        
        if insert_position == -1:
            print("⚠️  HTML 구조를 찾을 수 없습니다")
            return False
        
        # 새 카드 삽입
        updated_html = (
            html_content[:insert_position] + 
            '\n' + new_card + 
            '        ' + html_content[insert_position:]
        )
        
        # 파일 저장
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"✅ HTML 요약 페이지에 추가됨: {article['title'][:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ HTML 업데이트 실패: {str(e)}")
        return False

def update_json_summary(article: Dict, file_path: str) -> bool:
    """새로운 JSON 업데이트 로직"""
    try:
        manager = SummaryManager()
        
        # 파일명에서 ID 추출
        file_name = Path(file_path).name
        card_id = file_name.replace('.html', '') if file_name else None
        
        # 카드 데이터 구성
        card_data = {
            "id": card_id,
            "title": article.get('title', ''),
            "summary": article.get('summary', ''),
            "keywords": article.get('keywords', []),
            "date": article.get('date', datetime.now().strftime('%Y-%m-%d')),
            "file_path": os.path.basename(file_path),
            "category": article.get('category', '기타'),
            "added_date": datetime.now().isoformat()
        }
        
        # JSON에 추가
        success = manager.add_card(card_data)
        
        if success:
            print(f"✅ JSON 데이터베이스에 추가됨: {article['title'][:50]}...")
        
        return success
        
    except Exception as e:
        print(f"❌ JSON 업데이트 실패: {str(e)}")
        return False

def update_summary_date():
    """요약 페이지의 날짜 업데이트"""
    try:
        with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        current_date = datetime.now().strftime('%Y년 %m월 %d일')
        
        import re
        pattern = r'<p class="update-date">최종 업데이트: [^<]+</p>'
        replacement = f'<p class="update-date">최종 업데이트: {current_date}</p>'
        
        updated_html = re.sub(pattern, replacement, html_content)
        
        with open(SUMMARY_PATH, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"✅ 요약 페이지 날짜 업데이트: {current_date}")
        return True
        
    except Exception as e:
        print(f"❌ 날짜 업데이트 실패: {str(e)}")
        return False

# 테스트용
if __name__ == "__main__":
    test_article = {
        'title': '테스트 카드뉴스 - 하이브리드 모드',
        'summary': '이것은 하이브리드 모드 테스트입니다. HTML과 JSON 모두 업데이트됩니다.',
        'category': '테스트',
        'keywords': ['테스트', '하이브리드'],
        'date': '2025-06-16'
    }
    
    # 실제로는 실행하지 않음 (테스트 파일이 없으므로)
    print("✅ 하이브리드 모드 update_summary.py 준비 완료")
    print("   - HTML 업데이트 (기존 유지)")
    print("   - JSON 업데이트 (신규 추가)")
