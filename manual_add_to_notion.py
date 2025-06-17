#!/usr/bin/env python3
"""
관심 있는 기사를 수동으로 노션에 추가하는 스크립트
"""
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

from notion.notion_client import NotionClient

def add_manual_articles():
    """수동으로 기사 추가"""
    notion = NotionClient()
    
    # 추가할 기사 정보를 여기에 입력하세요
    articles = [
        {
            "title": "대구시, 데이터센터 전력 확보 비상",
            "source": "전기신문",  # 또는 실제 출처
            "date": "2025-06-05",  # 실제 날짜로 변경
            "url": "https://example.com/article1",  # 실제 URL로 변경
            "keywords": ["데이터센터", "전력확보", "대구"],
            "one_line_summary": "대구시가 급증하는 데이터센터 전력 수요에 대응하기 위해 비상 대책을 마련했다",
            "key_content": """• 데이터센터 전력 수요 급증으로 전력 부족 우려
• 지자체 차원의 전력 인프라 확충 계획 수립
• 재생에너지와 연계한 안정적 전력 공급 방안 모색"""
        },
        {
            "title": "신재생 출력제어 9TWh 돌파…올해만 7TWh 버려",
            "source": "전기신문",  # 또는 실제 출처
            "date": "2025-06-03",  # 실제 날짜로 변경
            "url": "https://example.com/article2",  # 실제 URL로 변경
            "keywords": ["출력제어", "재생에너지", "전력망"],
            "one_line_summary": "재생에너지 출력제어량이 9TWh를 돌파하며 에너지 낭비 우려가 커지고 있다",
            "key_content": """• 재생에너지 출력제어 규모 역대 최대 기록
• 계통 포화로 인한 불가피한 조치
• 전력망 확충과 ESS 확대 등 대책 시급"""
        }
    ]
    
    for article in articles:
        try:
            # 날짜 형식 변환
            date_obj = datetime.strptime(article['date'], '%Y-%m-%d')
            date_obj = pytz.timezone('Asia/Seoul').localize(date_obj)
            article['date'] = date_obj.strftime('%Y-%m-%d')
            
            # 노션에 추가
            result = notion.add_article(article)
            print(f"✅ 성공: {article['title']}")
            print(f"   페이지 ID: {result}")
            
        except Exception as e:
            print(f"❌ 실패: {article['title']}")
            print(f"   오류: {str(e)}")
    
    print("\n💡 사용법:")
    print("1. 위 articles 리스트의 정보를 실제 기사 정보로 수정")
    print("2. 특히 URL과 날짜를 정확히 입력")
    print("3. python3 manual_add_to_notion.py 실행")

if __name__ == "__main__":
    add_manual_articles()
