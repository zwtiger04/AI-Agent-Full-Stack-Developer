from datetime import datetime
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from crawlers.base_crawler import BaseCrawler
from notion.notion_client import NotionClient

class KPXCrawler(BaseCrawler):
    def __init__(self, notion_client: NotionClient, recommender: Optional[Any] = None):
        super().__init__('한국전력거래소', 'https://www.kpx.or.kr')
        self.notion_client = notion_client
        self.recommender = recommender
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.notice_url = f"{self.base_url}/www/notice/notice_list.do"
        self.press_url = f"{self.base_url}/www/notice/press_list.do"

    def get_news_list(self) -> List[Dict[str, Any]]:
        """Get list of news articles from KPX"""
        articles = []
        
        # Get notices
        notice_articles = self._get_notice_list()
        articles.extend(notice_articles)
        
        # Get press releases
        press_articles = self._get_press_list()
        articles.extend(press_articles)
        
        return articles

    def _get_notice_list(self) -> List[Dict[str, Any]]:
        """Get list of notices"""
        articles = []
        try:
            html_content = self.get_page_content(self.notice_url)
            soup = self.parse_html(html_content)
            
            # Find all notice items
            notice_items = soup.select('table.board-list tbody tr')
            
            for item in notice_items:
                try:
                    # Extract notice information
                    title_element = item.select_one('td.title a')
                    if not title_element:
                        continue
                        
                    title = title_element.text.strip()
                    url = title_element.get('href', '')
                    if url and not url.startswith('http'):
                        url = self.base_url + url
                        
                    date_element = item.select_one('td.date')
                    date_str = date_element.text.strip() if date_element else ''
                    
                    # Parse date
                    try:
                        published_date = datetime.strptime(date_str, '%Y-%m-%d')
                    except ValueError:
                        published_date = datetime.now()
                    
                    articles.append({
                        'title': title,
                        'url': url,
                        'published_date': published_date,
                        'type': 'notice'
                    })
                except Exception as e:
                    print(f"Error processing notice: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error getting notice list: {str(e)}")
            
        return articles

    def _get_press_list(self) -> List[Dict[str, Any]]:
        """Get list of press releases"""
        articles = []
        try:
            html_content = self.get_page_content(self.press_url)
            soup = self.parse_html(html_content)
            
            # Find all press items
            press_items = soup.select('table.board-list tbody tr')
            
            for item in press_items:
                try:
                    # Extract press information
                    title_element = item.select_one('td.title a')
                    if not title_element:
                        continue
                        
                    title = title_element.text.strip()
                    url = title_element.get('href', '')
                    if url and not url.startswith('http'):
                        url = self.base_url + url
                        
                    date_element = item.select_one('td.date')
                    date_str = date_element.text.strip() if date_element else ''
                    
                    # Parse date
                    try:
                        published_date = datetime.strptime(date_str, '%Y-%m-%d')
                    except ValueError:
                        published_date = datetime.now()
                    
                    articles.append({
                        'title': title,
                        'url': url,
                        'published_date': published_date,
                        'type': 'press'
                    })
                except Exception as e:
                    print(f"Error processing press release: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error getting press list: {str(e)}")
            
        return articles

    def get_article_content(self, url: str) -> Dict[str, Any]:
        """Get article content from KPX"""
        try:
            html_content = self.get_page_content(url)
            soup = self.parse_html(html_content)
            
            # Extract article content
            content_element = soup.select_one('.board-view-content')
            content = content_element.text.strip() if content_element else ''
            
            # Extract attachments if any
            attachments = []
            attachment_elements = soup.select('.board-view-file a')
            for element in attachment_elements:
                attachments.append({
                    'name': element.text.strip(),
                    'url': element.get('href', '')
                })
            
            return {
                'content': content,
                'attachments': attachments
            }
        except Exception as e:
            print(f"Error getting article content: {str(e)}")
            return {'content': '', 'attachments': []} 