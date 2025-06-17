# 키워드 업데이트 스크립트
import fileinput
import sys

# 기존 파일 읽기
with open('crawlers/electimes_crawler.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 키워드 목록 찾아서 업데이트
old_keywords = """    KEYWORDS = [
        '재생에너지', '전력중개사업', 'VPP', '전력시장', 'ESS', 
        '출력제어', '중앙계약', '저탄소 용량', 
        '재생에너지입찰', '보조서비스', 
        '예비력시장', '하향예비력', '계통포화',
        '전력망',  # 추가된 키워드
        '기후에너지부', '태양광', '전력감독원',
        '풍력', '해상풍력', '전력가격', 'SMP'
    ]"""

new_keywords = """    KEYWORDS = [
        '재생에너지', '전력중개사업', 'VPP', '전력시장', 'ESS', 
        '출력제어', '중앙계약', '저탄소 용량', 
        '재생에너지입찰', '보조서비스', 
        '예비력시장', '하향예비력', '계통포화',
        '전력망',  # 추가된 키워드
        '기후에너지부', '태양광', '전력감독원',
        '풍력', '해상풍력', '전력가격', 'SMP',
        '데이터센터', '전력수급', '전력확보'  # 새로 추가
    ]"""

# 내용 변경
content = content.replace(old_keywords, new_keywords)

# 파일 저장
with open('crawlers/electimes_crawler.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 키워드 업데이트 완료!")
print("추가된 키워드: 데이터센터, 전력수급, 전력확보")
