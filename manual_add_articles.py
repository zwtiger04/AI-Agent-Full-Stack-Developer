import os
from dotenv import load_dotenv
from notion.notion_client import NotionClient
from datetime import datetime
import pytz

load_dotenv()

# 노션 클라이언트 초기화
notion = NotionClient()

# 추가할 기사 정보
articles = [
    {
        "title": "대구시, 데이터센터 전력 확보 비상",
        "url": "https://www.electimes.com/article.asp?aid=1234567890",  # 실제 URL로 변경 필요
        "summary": "대구시가 급증하는 데이터센터 전력 수요 대응에 나섰다",
        "keywords": ["데이터센터", "전력망"],
        "date": datetime.now(pytz.timezone('Asia/Seoul'))
    },
    {
        "title": "신재생 출력제어 9TWh 돌파…올해만 7TWh 버려",
        "url": "https://www.electimes.com/article.asp?aid=0987654321",  # 실제 URL로 변경 필요
        "summary": "재생에너지 출력제어량이 급증하며 에너지 낭비 우려가 커지고 있다",
        "keywords": ["출력제어", "재생에너지"],
        "date": datetime.now(pytz.timezone('Asia/Seoul'))
    }
]

# 노션에 추가
for article in articles:
    try:
        notion.add_article(article)
        print(f"✅ 추가 완료: {article['title']}")
    except Exception as e:
        print(f"❌ 추가 실패: {article['title']} - {e}")
