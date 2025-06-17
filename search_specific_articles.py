#!/usr/bin/env python3
"""
특정 기사를 날짜 제한 없이 검색하는 스크립트
"""
from crawlers.electimes_crawler import ElectimesCrawler
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def search_articles():
    """특정 키워드로 전기신문 검색"""
    
    # Selenium 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # 검색할 키워드들
        search_terms = ["대구 데이터센터", "출력제어 9TWh"]
        
        for term in search_terms:
            print(f"\n🔍 '{term}' 검색 중...")
            
            # 전기신문 검색 페이지
            search_url = f"https://www.electimes.com/news/articleList.html?sc_word={term}"
            driver.get(search_url)
            time.sleep(2)
            
            # 검색 결과 확인
            articles = driver.find_elements(By.CSS_SELECTOR, "section.article-list-content")
            
            print(f"검색 결과: {len(articles)}개")
            
            # 상위 5개 결과 출력
            for i, article in enumerate(articles[:5]):
                try:
                    title_elem = article.find_element(By.CSS_SELECTOR, "h4.titles")
                    date_elem = article.find_element(By.CSS_SELECTOR, "em.dates")
                    link_elem = article.find_element(By.CSS_SELECTOR, "a")
                    
                    print(f"\n{i+1}. {title_elem.text}")
                    print(f"   날짜: {date_elem.text}")
                    print(f"   URL: {link_elem.get_attribute('href')}")
                except:
                    continue
                    
    finally:
        driver.quit()

if __name__ == "__main__":
    search_articles()
