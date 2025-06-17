# 현재 키워드 목록 확인
import sys
sys.path.append('.')
from crawlers.electimes_crawler import ElectimesCrawler

crawler = ElectimesCrawler(None)
print("현재 키워드 목록:")
for i, keyword in enumerate(crawler.KEYWORDS, 1):
    print(f"{i:2d}. {keyword}")

print(f"\n총 {len(crawler.KEYWORDS)}개 키워드")
