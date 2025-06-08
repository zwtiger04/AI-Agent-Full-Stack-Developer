from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class BaseCrawler(ABC):
    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url
        self.driver = None

    def setup_selenium(self):
        """Setup Selenium WebDriver with dynamic ChromeDriver path finding"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # 동적 ChromeDriver 경로 탐색
        def find_chromedriver():
            import os
            import glob
            
            # WebDriverManager 시도
            wdm_path = ChromeDriverManager().install()
            
            # 결과 검증 및 올바른 파일 찾기
            if os.path.exists(wdm_path) and os.access(wdm_path, os.X_OK) and os.path.getsize(wdm_path) > 1000000:
                return wdm_path
            
            # 같은 디렉토리에서 실제 chromedriver 찾기
            wdm_dir = os.path.dirname(wdm_path)
            for driver_path in glob.glob(os.path.join(wdm_dir, '**/chromedriver*'), recursive=True):
                if (os.path.isfile(driver_path) and os.access(driver_path, os.X_OK) and 
                    'chromedriver' in os.path.basename(driver_path) and
                    not driver_path.endswith('.chromedriver') and os.path.getsize(driver_path) > 1000000):
                    return driver_path
            
            raise Exception("올바른 chromedriver를 찾을 수 없습니다")
        
        driver_path = find_chromedriver()
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def close_selenium(self):
        """Close Selenium WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_page_content(self, url: str) -> str:
        """Get page content using requests"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return ""

    def parse_html(self, html_content: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html_content, 'html.parser')

    @abstractmethod
    def crawl(self) -> List[Dict[str, Any]]:
        """Crawl news articles"""
        pass

    @abstractmethod
    def get_article_content(self, url: str) -> Dict[str, Any]:
        """Get article content"""
        pass

    def format_article(self, title: str, content: str, url: str, 
                      published_date: datetime) -> Dict[str, Any]:
        """Format article data"""
        return {
            'title': title,
            'content': content,
            'url': url,
            'source': self.source_name,
            'published_date': published_date,
            'crawled_date': datetime.now()
        } 