import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'power_news')

# Notion Configuration
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
NOTION_PARENT_PAGE_ID = os.getenv('NOTION_PARENT_PAGE_ID')

# Debug: Print loaded environment variables
print(f"Loaded NOTION_API_KEY: {NOTION_API_KEY is not None}") # Check if key is loaded
print(f"Loaded NOTION_PARENT_PAGE_ID: {NOTION_PARENT_PAGE_ID}") # Print the parent page ID

# Crawling Configuration
KEYWORDS = [
    '재생에너지', '전력중개사업', 'VPP', '전력시장', 'ESS',
    '출력제어', '중앙계약', '저탄소 용량', '전력산업', '전력정책',
    '재생에너지입찰', '보조서비스', '예비력시장', '하향예비력', '계통포화',
    '전력망', '기후에너지부', '태양광', '전력감독원',
    '풍력', '해상풍력', '전력가격', 'SMP'
]

# News Sources
NEWS_SOURCES = {
    '전기신문': 'https://www.electimes.com',
    '전기저널': 'https://www.electimes.com',
    '한국전력거래소': 'https://www.kpx.or.kr',
    '산업부': 'https://www.motie.go.kr',
    '한국전력': 'https://www.kepco.co.kr'
}

# Crawling Schedule (in hours)
CRAWLING_INTERVAL = 6 