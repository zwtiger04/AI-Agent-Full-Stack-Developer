# 크롤링 날짜 제한을 3일에서 7일로 확장
import fileinput

# electimes_crawler.py 파일 수정
with open('crawlers/electimes_crawler.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 3일을 7일로 변경
content = content.replace('timedelta(days=3)', 'timedelta(days=7)')
content = content.replace('최근 3일', '최근 7일')

with open('crawlers/electimes_crawler.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 크롤링 날짜 제한을 3일에서 7일로 확장했습니다!")
