#!/usr/bin/env python3
import os
import sys
from datetime import datetime
import pytz
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 노션 클라이언트 import
from notion.notion_client import NotionClient

def add_articles_to_notion():
    """관심 기사들을 수동으로 노션에 추가"""
    
    # 노션 클라이언트 초기화
    notion = NotionClient()
    
    # 추가할 기사 정보 (URL은 실제 URL로 변경 필요)
    articles = [
        {
            "title": "대구시, 데이터센터 전력 확보 비상",
            "source": "전기신문",
            "date": datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d'),
            "url": "https://www.electimes.com/article.php?aid=1234567890",  # 실제 URL 필요
            "keywords": ["데이터센터", "전력확보", "전력수급"],
            "one_line_summary": "대구시가 급증하는 데이터센터 전력 수요에 대응하기 위해 비상 대책을 마련했다",
            "key_content": "• 데이터센터 전력 수요 급증\n• 전력 인프라 확충 필요\n• 지자체 차원의 대응 방안 모색"
        },
        {
            "title": "신재생 출력제어 9TWh 돌파…올해만 7TWh 버려",
            "source": "전기신문", 
            "date": datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d'),
            "url": "https://www.electimes.com/article.php?aid=0987654321",  # 실제 URL 필요
            "keywords": ["출력제어", "재생에너지", "전력망"],
            "one_line_summary": "재생에너지 출력제어량이 9TWh를 돌파하며 에너지 낭비 우려가 커지고 있다",
            "key_content": "• 출력제어 규모 역대 최대\n• 계통 포화로 인한 불가피한 조치\n• 전력망 확충 시급성 증대"
        }
    ]
    
    # 각 기사를 노션에 추가
    for article in articles:
        try:
            # add_article 메서드 사용
            result = notion.add_article(article)
            print(f"✅ 성공적으로 추가됨: {article['title']}")
            print(f"   노션 페이지 ID: {result}")
            
        except Exception as e:
            print(f"❌ 추가 실패: {article['title']}")
            print(f"   오류: {str(e)}")
    
    print("\n💡 팁: 실제 기사 URL을 찾아서 수정한 후 실행하세요!")
    print("   전기신문 웹사이트에서 해당 기사를 검색해보세요.")

if __name__ == "__main__":
    add_articles_to_notion()
