from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import requests
from selenium import webdriver # Selenium 관련 import 주석 처리
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from crawlers.base_crawler import BaseCrawler
from recommenders.article_recommender import ArticleRecommender
import json
import os
import re
import time
import pytz # pytz 라이브러리 추가
from notion.notion_client import NotionClient
import joblib
from processors.keyword_processor import KeywordProcessor
from ai_update_content import clean_article_content, generate_one_line_summary_with_llm, generate_key_content

class ElectimesCrawler(BaseCrawler):
    # 전력 산업 관련 키워드
    KEYWORDS = [
        '재생에너지', '전력중개사업', 'VPP', '전력시장', 'ESS', 
        '출력제어', '중앙계약', '저탄소 용량', 
        '재생에너지입찰', '보조서비스', 
        '예비력시장', '하향예비력', '계통포화',
        '전력망',  # 추가된 키워드
        '기후에너지부',  # 사용자 요청으로 추가
        '태양광', # 사용자 요청으로 추가
        '전력감독원'  # 사용자 요청으로 추가
    ]
    
    def __init__(self, notion_client: NotionClient, recommender: Optional[Any] = None):
        super().__init__('전기신문', 'https://www.electimes.com')
        self._source_name = '전기신문' # Explicitly store source name
        # 모든 섹션의 기사를 크롤링하기 위해 URL 수정
        self.list_url = f"{self.base_url}/news/articleList.html?view_type=sm"
        print("ElectimesCrawler initialized (using requests)")
        
        # 크롤링 이력 파일 경로
        self.history_file = 'crawled_articles.json'
        self.crawled_urls = self.load_crawled_urls()
        
        # Selenium 관련 초기화 제거 또는 주석 처리
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
        
        # WebDriverManager 버그 해결: 동적 경로 탐색
        def find_chromedriver_path():
            """WebDriverManager 결과를 검증하고 올바른 chromedriver 찾기"""
            import os
            import glob
            
            try:
                # 1단계: WebDriverManager 시도
                wdm_path = ChromeDriverManager().install()
                
                # 2단계: 결과 검증
                if os.path.exists(wdm_path) and os.access(wdm_path, os.X_OK):
                    # 올바른 파일인지 확인 (크기 체크)
                    if os.path.getsize(wdm_path) > 1000000:  # 1MB 이상이면 정상적인 chromedriver
                        return wdm_path
                
                # 3단계: 같은 디렉토리에서 실제 chromedriver 찾기
                wdm_dir = os.path.dirname(wdm_path)
                potential_drivers = glob.glob(os.path.join(wdm_dir, '**/chromedriver*'), recursive=True)
                
                for driver_path in potential_drivers:
                    if (os.path.isfile(driver_path) and 
                        os.access(driver_path, os.X_OK) and 
                        'chromedriver' in os.path.basename(driver_path) and
                        not driver_path.endswith('.chromedriver') and
                        os.path.getsize(driver_path) > 1000000):  # 실제 실행파일인지 확인
                        return driver_path
                
                # 4단계: 전체 .wdm 디렉토리에서 찾기 (마지막 수단)
                home_dir = os.path.expanduser("~")
                wdm_base = os.path.join(home_dir, ".wdm", "drivers", "chromedriver")
                if os.path.exists(wdm_base):
                    all_drivers = glob.glob(os.path.join(wdm_base, "**/chromedriver"), recursive=True)
                    for driver_path in all_drivers:
                        if (os.path.isfile(driver_path) and 
                            os.access(driver_path, os.X_OK) and
                            os.path.getsize(driver_path) > 1000000):
                            return driver_path
                
                raise Exception("올바른 chromedriver를 찾을 수 없습니다")
                
            except Exception as e:
                raise Exception(f"ChromeDriver 경로 탐색 실패: {e}")
        
        try:
            driver_path = find_chromedriver_path()
            service = Service(driver_path)
            print(f"ChromeDriver 경로: {driver_path}")
        except Exception as e:
            print(f"ChromeDriver 초기화 실패: {e}")
            raise
        
        try:
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            print("Chromium WebDriver initialized successfully")
        except Exception as e:
            print(f"Error initializing Chromium WebDriver: {str(e)}")
            # Selenium 초기화 실패 시 requests 사용으로 폴백 (선택 사항)
            print("Falling back to requests for page content.")
            self.driver = None
            
        # AI 추천 시스템 초기화
        self.article_recommender = ArticleRecommender(notion_client)
        self.ai_recommender = recommender  # recommender를 ai_recommender로 사용
        self.patterns = None  # 관심 패턴
        self.keywords = set()  # 동적 키워드 세트
        self.update_crawling_criteria()  # 초기 크롤링 기준 설정

    def __del__(self):
        """드라이버 종료"""
        if hasattr(self, 'driver') and self.driver is not None:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error closing WebDriver: {str(e)}")

    def load_crawled_urls(self) -> set:
        """이전에 크롤링한 URL 목록을 로드"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
            except Exception as e:
                print(f"Error loading crawled URLs: {str(e)}")
        return set()

    def save_crawled_url(self, url: str):
        """크롤링한 URL을 저장"""
        self.crawled_urls.add(url)
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.crawled_urls), f)
        except Exception as e:
            print(f"Error saving crawled URL: {str(e)}")

    def is_recent_article(self, date: datetime) -> bool:
        """기사가 한국 시간 기준으로 최근 3일 내의 것인지 확인 (날짜만 비교)"""
        kst = pytz.timezone('Asia/Seoul')
        now_kst = datetime.now(kst) # 한국 시간 현재 시각
        today_kst = now_kst.date() # 한국 시간 오늘 날짜
        three_days_ago_kst = today_kst - timedelta(days=3) # 한국 시간 3일 전 날짜

        # 기사 날짜의 시간 정보 제거 (naive datetime 가정)
        article_date = date.date()

        is_recent = article_date >= three_days_ago_kst
        # print(f"Date check (KST) - Article date (date only): {article_date}, 3 days ago (KST date only): {three_days_ago_kst}, Is recent: {is_recent})") # Debug log 제거
        return is_recent

    def _parse_date_safely(self, date_str: str) -> Optional[datetime]:
        """
        🔧 안전한 날짜 파싱 메서드
        
        **목적**: 다양한 날짜 형식을 시도하되, 실패 시 None 반환
        **장점**: 파싱 실패한 기사를 명확히 구분 가능
        **보안**: 현재 시간으로 대체하지 않아 필터링 무력화 방지
        
        Args:
            date_str (str): 파싱할 날짜 문자열
            
        Returns:
            Optional[datetime]: 성공시 datetime 객체, 실패시 None
        """
        if not date_str or not date_str.strip():
            return None
            
        date_str = date_str.strip()
        
        # 🎯 시도할 날짜 형식 패턴들 (우선순위 순)
        date_patterns = [
            '%Y.%m.%d %H:%M',     # 2025.06.03 10:00
            '%Y.%m.%d',           # 2025.06.03
            '%Y-%m-%d %H:%M:%S',  # 2025-06-03 10:00:00
            '%Y-%m-%d %H:%M',     # 2025-06-03 10:00
            '%Y-%m-%d',           # 2025-06-03
            '%Y/%m/%d %H:%M',     # 2025/06/03 10:00
            '%Y/%m/%d',           # 2025/06/03
            '%m.%d %H:%M',        # 06.03 10:00 (연도 없음)
            '%m-%d %H:%M',        # 06-03 10:00 (연도 없음)
            '%m/%d %H:%M',        # 06/03 10:00 (연도 없음)
        ]
        
        for pattern in date_patterns:
            try:
                parsed_date = datetime.strptime(date_str, pattern)
                
                # 🔍 연도가 없는 패턴의 경우 현재 연도 적용
                if '%Y' not in pattern:
                    current_year = datetime.now().year
                    parsed_date = parsed_date.replace(year=current_year)
                
                print(f"[Electimes] 날짜 파싱 성공: '{date_str}' → {parsed_date} (패턴: {pattern})")
                return parsed_date
                
            except ValueError:
                continue  # 다음 패턴 시도
        
        # 🚨 모든 패턴 실패 시
        print(f"[Electimes] ⚠️  날짜 파싱 실패: '{date_str}' - 지원되지 않는 형식")
        print(f"[Electimes] 📋 지원 형식: {', '.join(date_patterns[:5])} 등")
        return None  # ✅ 현재 시간 대신 None 반환

    def _smart_retry(self, operation_name: str, operation_func, max_retries: int = 3, base_delay: float = 2.0):
        """
        🔧 스마트 네트워크 재시도 시스템
        
        **특징**:
        - 지수 백오프 (Exponential Backoff): 2초 → 4초 → 8초
        - 오류 분류: 일시적 vs 영구적 오류 구분
        - 지터(Jitter): 랜덤 요소 추가로 서버 부하 분산
        
        Args:
            operation_name (str): 작업 이름 (로그용)
            operation_func (callable): 실행할 함수
            max_retries (int): 최대 재시도 횟수
            base_delay (float): 기본 대기 시간(초)
            
        Returns:
            operation_func의 결과 또는 None
        """
        import random
        
        # 🔍 재시도 가능한 오류 타입들
        retryable_exceptions = (
            requests.exceptions.ConnectionError,     # 연결 오류
            requests.exceptions.Timeout,            # 타임아웃
            requests.exceptions.HTTPError,          # HTTP 5xx 오류
            TimeoutException,                       # Selenium 타임아웃
        )
        
        for attempt in range(max_retries):
            try:
                print(f"[Electimes] {operation_name} 시도 중... (시도 {attempt + 1}/{max_retries})")
                result = operation_func()
                print(f"[Electimes] ✅ {operation_name} 성공!")
                return result
                
            except retryable_exceptions as e:
                if attempt < max_retries - 1:
                    # 🎯 지수 백오프 + 지터 계산
                    delay = base_delay * (2 ** attempt)  # 2초 → 4초 → 8초
                    jitter = random.uniform(0.1, 0.3) * delay  # 10-30% 랜덤 추가
                    total_delay = delay + jitter
                    
                    print(f"[Electimes] ⚠️ {operation_name} 일시적 오류: {type(e).__name__}")
                    print(f"[Electimes] 🔄 {total_delay:.1f}초 후 재시도... (지수 백오프)")
                    time.sleep(total_delay)
                else:
                    print(f"[Electimes] ❌ {operation_name} 최종 실패: {str(e)}")
                    break
                    
            except (requests.exceptions.HTTPError, ValueError, AttributeError) as e:
                # 🚫 영구적 오류 - 재시도하지 않음
                print(f"[Electimes] ❌ {operation_name} 영구적 오류 (재시도 안함): {type(e).__name__} - {str(e)}")
                break
                
            except Exception as e:
                # 🤔 알 수 없는 오류 - 보수적으로 재시도
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"[Electimes] ❓ {operation_name} 알 수 없는 오류: {type(e).__name__} - {str(e)}")
                    print(f"[Electimes] 🔄 {delay}초 후 재시도...")
                    time.sleep(delay)
                else:
                    print(f"[Electimes] ❌ {operation_name} 최종 실패 (알 수 없는 오류): {str(e)}")
                    break
        
        return None  # 모든 시도 실패

    def contains_keywords_and_extract(self, text: str) -> tuple[bool, list]:
        """텍스트에 키워드가 포함되어 있는지 확인하고 매칭된 키워드 반환"""
        found_keywords = [keyword for keyword in self.KEYWORDS if keyword in text]
        if found_keywords:
            return True, found_keywords
        return False, []
    
    def contains_keywords(self, text: str) -> bool:
        """이전 버전과의 호환성을 위한 래퍼 함수"""
        contains, _ = self.contains_keywords_and_extract(text)
        return contains

    def get_page_content(self, url: str) -> str:
        """🔧 개선된 Selenium 페이지 컨텐츠 가져오기 (스마트 재시도 적용)"""
        if self.driver is None:
            print("Selenium driver not initialized. Cannot get page content.")
            return ""

        def fetch_with_selenium():
            """Selenium으로 페이지 가져오기 작업"""
            self.driver.get(url)
            
            # Simple wait for page content to potentially load dynamically
            time.sleep(5)
            
            html_content = self.driver.page_source

            # Save HTML content to file for debugging
            filename = url.split('/')[-1].split('?')[0]
            if not filename:
                filename = 'index.html'
            if not filename.endswith('.html'):
                filename = filename + '.html'
                
            # Append query parameters to filename for distinction
            query_string = url.split('?')
            if len(query_string) > 1:
                filename = f"{filename}?{'?'.join(query_string[1:])}"

            # Replace invalid characters in filename
            filename = re.sub(r'[^a-zA-Z0-9_.-?=&]', '_', filename)
            debug_file = f"debug_{filename}"

            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Saved HTML content to {debug_file}")
            
            return html_content

        # 🚀 스마트 재시도 시스템 사용 (Selenium 전용 설정)
        result = self._smart_retry(
            operation_name=f"Selenium 페이지 로드 ({url})",
            operation_func=fetch_with_selenium,
            max_retries=3,
            base_delay=3.0  # Selenium은 더 느리므로 대기 시간 증가
        )

        if result:
            print(f"Successfully fetched {url} using Selenium. Content length: {len(result)}")
            return result
        else:
            print(f"Failed to fetch {url} using Selenium after all retries")
            return ""

    def parse_html(self, html_content: str) -> BeautifulSoup:
        """Parse HTML content using BeautifulSoup"""
        return BeautifulSoup(html_content, 'html.parser')

    def update_crawling_criteria(self):
        """크롤링 기준 업데이트"""
        try:
            # AI 추천 모델 및 벡터라이저 로드
            model_path = 'feedback/ai_recommend_model.joblib'
            vectorizer_path = 'feedback/ai_recommend_vectorizer.joblib'

            if os.path.exists(model_path) and os.path.exists(vectorizer_path):
                try:
                    self.ai_recommender = joblib.load(model_path)
                    self.vectorizer = joblib.load(vectorizer_path) # Add vectorizer loading
                    print("[Crawler] AI 추천 모델 및 벡터라이저 로드 완료")
                except Exception as model_e:
                    print(f"[Crawler] AI 추천 모델/벡터라이저 로드 중 오류 발생: {str(model_e)}")
                    self.ai_recommender = None # Ensure it's None on error
                    self.vectorizer = None # Ensure it's None on error
            else:
                print("[Crawler] AI 추천 모델 또는 벡터라이저 파일이 없습니다. AI 추천 필터링을 건너뜀.")
                self.ai_recommender = None
                self.vectorizer = None

            # 관심 기사에서 키워드 추출
            # Note: This part assumes ArticleRecommender can load patterns/keywords without a pre-trained model
            # If not, this needs adjustment.
            if hasattr(self, 'article_recommender') and self.article_recommender:
                 interested_articles = self.article_recommender.notion.get_interested_articles()
                 if interested_articles:
                     # Assuming analyze_article_patterns extracts keywords from interested articles
                     patterns = self.article_recommender.analyze_article_patterns(interested_articles) # patterns 변수 추가
                     if patterns and 'keywords' in patterns:
                         # self.keywords를 KEYWORDS와 합치는 로직 필요 시 추가
                         # 현재는 KEYWORDS + 관심기사 키워드 모두 contains_keywords에서 사용하도록 가정
                         # self.keywords.update(patterns['keywords'])
                         print(f"[Crawler] 관심 기사에서 키워드 추출 완료 (contains_keywords에서 사용됨)")
                     else:
                         print("[Crawler] 관심 기사에서 추출할 키워드가 없습니다.")
                 else:
                      print("[Crawler] 관심 기사가 없어 키워드 추출을 건너뜀.")
            # else:
            #     print("[Crawler] ArticleRecommender가 초기화되지 않아 관심 기사 키워드 추출을 건너뜀.") # Debug log

        except Exception as e:
            print(f"[Crawler] 크롤링 기준 업데이트 중 오류 발생: {str(e)}")
            import traceback
            print(traceback.format_exc())

    def _fetch_articles(self, page: int = 1) -> List[Dict[str, Any]]:
        """특정 페이지의 기사 목록 원시 데이터를 가져옵니다."""
        url = f"{self.list_url}&page={page}"
        print(f"[Electimes] 기사 목록 가져오는 중 (페이지 {page}): {url}")
        
        try:
            # Selenium 드라이버가 초기화되었으면 Selenium 사용, 아니면 requests 사용
            if self.driver:
                html_content = self.get_page_content(url)
            else:
                # 🚀 개선된 requests 호출 (스마트 재시도 적용)
                def fetch_page_list():
                    """페이지 목록 가져오기 작업"""
                    response = requests.get(url, timeout=15)
                    response.raise_for_status()
                    return response.text

                print(f"[Electimes] Selenium 드라이버 사용 불가. 스마트 재시도로 기사 목록 가져오는 중: {url}")
                html_content = self._smart_retry(
                    operation_name=f"기사 목록 가져오기 (페이지 {page})",
                    operation_func=fetch_page_list,
                    max_retries=3,
                    base_delay=1.5  # 목록 페이지는 좀 더 빠르게
                )

            if not html_content:
                print(f"[Electimes] 페이지 콘텐츠를 가져오지 못했습니다: {url}")
                return []
                
            soup = self.parse_html(html_content)
            # 수정된 CSS 선택자 사용
            articles = []
            # section#section-list li.item 아래에서 기사 항목 찾기
            article_items = soup.select('section#section-list li.item')
            
            if not article_items:
                 print(f"[Electimes] 페이지 {page}에서 기사 항목을 찾지 못했습니다. (선택자: section#section-list li.item)")
                 # 빈 목록을 반환하여 페이지네이션 중단 로직이 작동하도록 유도
                 return []

            print(f"[Electimes] 페이지 {page}에서 {len(article_items)}개의 기사 항목 발견.")

            for item in article_items:
                # 수정된 CSS 선택자 사용: 제목 링크, 날짜
                title_link = item.select_one('h4.titles a.linked')
                date_tag = item.select_one('em.replace-date')
                source_tag = item.select_one('span.byline a') # 출처(기자 이름/소속) 가져오기 추가

                title = title_link.text.strip() if title_link else None
                url = self.base_url + title_link['href'] if title_link and title_link.has_attr('href') else None
                date_str = date_tag.text.strip() if date_tag else None
                source = source_tag.text.strip() if source_tag else self._source_name # 출처 가져오기

                # 🔧 개선된 날짜 파싱 시도 (다양한 형식 고려)
                published_date = None
                if date_str:
                    published_date = self._parse_date_safely(date_str)
                            
                # ✅ 제목, URL, 날짜가 모두 성공적으로 파싱된 경우만 추가
                if title and url and published_date:
                     articles.append({
                         'title': title,
                         'url': url,
                         'published_date': published_date,
                         'source': source, # 출처 추가
                         'content': '', # content는 상세 페이지에서 가져옴
                         'keywords': [], # 키워드는 나중에 추가
                         'ai_recommend': False # AI 추천 초기값
                     })
                     # print(f"[Electimes] 기사 항목 추출: {title} - {date_str}") # Debug log 제거
                elif date_str and not published_date:
                    # 📝 날짜 파싱 실패한 기사는 로그로 기록
                    print(f"[Electimes] ⚠️  날짜 파싱 실패로 기사 제외: '{title}' - 날짜: '{date_str}'")
                # else:
                #     print(f"[Electimes] 기사 항목 스킵 (정보 누락): 제목={title}, URL={url}, 날짜={date_str}") # Debug log 제거
                
            return articles
            
        except requests.exceptions.RequestException as e:
             print(f"[Electimes] HTTP 요청 오류 발생 (페이지 {page}): {str(e)}")
             return []
        except Exception as e:
            print(f"[Electimes] 기사 목록 가져오는 중 오류 발생 (페이지 {page}): {str(e)}")
            import traceback
            print(traceback.format_exc())
            return []

    def _extract_date(self, article: Dict[str, Any]) -> Optional[datetime]:
         """🔧 기사 딕셔너리에서 날짜 정보를 안전하게 추출합니다."""
         date = article.get('published_date')
         if isinstance(date, str):
             # 🔧 안전한 날짜 파싱 메서드 사용
             return self._parse_date_safely(date)
         return date

    def crawl(self) -> list:
        """
        전기신문 기사를 크롤링합니다.
        한국 날짜 기준으로 최근 3일 이내 기사가 나타날 때까지 페이지를 탐색하며,
        키워드 및 AI 추천 필터링을 거쳐 상세 내용을 크롤링합니다.
        """
        print("[Electimes] 크롤링 시작...")
        self.update_crawling_criteria() # 최신 기준 업데이트
        
        crawled_articles_details = []
        page = 1
        recent_article_found_on_page = True # 현재 페이지에서 최근 기사 발견 여부
        consecutive_pages_without_recent = 0 # 최근 기사 없는 연속 페이지 수
        max_consecutive_without_recent = 3 # 최근 기사 없이 탐색할 최대 연속 페이지 수
        
        while recent_article_found_on_page and page <= 20: # 최대 20페이지까지 탐색 (안전 장치)
            print(f"[Electimes] 페이지 {page} 탐색 중...")
            recent_article_found_on_page = False # 다음 페이지를 위해 초기화

            raw_articles_on_page = self._fetch_articles(page)
            
            if not raw_articles_on_page:
                 print(f"[Electimes] 페이지 {page}에서 가져온 기사 없음. 탐색 종료.")
                 break # 기사 목록이 없으면 탐색 종료

            # 1. 날짜 필터링 및 최근 기사 발견 여부 체크
            recent_articles_on_page = []
            for article in raw_articles_on_page:
                 published_date = self._extract_date(article)
                 if published_date and self.is_recent_article(published_date):
                     recent_articles_on_page.append(article)
                     recent_article_found_on_page = True # 현재 페이지에서 최근 기사 발견!

            if recent_article_found_on_page:
                 consecutive_pages_without_recent = 0 # 최근 기사를 찾았으므로 카운트 리셋
                 print(f"[Electimes] 페이지 {page}에서 최근 3일 이내 기사 발견. 탐색 계속.")
            else:
                 consecutive_pages_without_recent += 1
                 print(f"[Electimes] 페이지 {page}에서 최근 3일 이내 기사 없음. 연속 {consecutive_pages_without_recent} 페이지.")
                 if consecutive_pages_without_recent >= max_consecutive_without_recent:
                     print(f"[Electimes] 최근 기사 없는 페이지가 {max_consecutive_without_recent}번 연속되어 탐색 종료.")
                     break # 연속 3페이지 동안 최근 기사가 없으면 탐색 종료

            # 날짜 필터링 통과한 기사들에 대해서만 추가 처리
            articles_to_process = recent_articles_on_page
            
            # 2. AI 추천 예측 적용 (모델이 로드된 경우에만)
            if self.ai_recommender and self.vectorizer and articles_to_process:
                # predict_ai_recommend는 ArticleRecommender 인스턴스 메서드이므로 self.article_recommender 사용
                # 하지만 predict_ai_recommend는 내부적으로 vectorizer와 model을 로드함. 중복 로딩 방지 또는 인자 전달 필요.
                # 현재 ai_recommender 인스턴스는 LogisticRegression 모델 객체이므로 predict 메서드를 사용해야 함.
                # 그리고 predict에는 벡터화된 텍스트 데이터(X_vec)가 필요하므로 vectorizer를 사용해야 함.
                
                try:
                     # 텍스트 준비 (제목 + 본문. 본문은 get_article_content 후 알 수 있지만, 여기서는 목록 정보만 사용)
                     # AI 예측은 상세 내용을 가져온 후 해야 더 정확하지만, 현재 구조상 목록 단계에서 일부 예측 시도.
                     # 상세 내용을 가져온 후 AI 예측 및 필터링하는 방식으로 변경하는 것이 합리적입니다.
                     # 계획을 수정하여, 페이지 목록 가져오기 -> 날짜 필터링 -> 상세 내용 크롤링 (조건부) -> 상세 내용에 대해 AI 예측 -> 최종 필터링 순서로 변경합니다.

                     # **수정된 계획 적용:**
                     # 페이지 목록 가져오기 -> 날짜 필터링 -> 상세 내용 크롤링 (조건부) -> 상세 내용에 대해 AI 예측 -> 최종 필터링

                     # 이 페이지의 최근 기사 목록에 대해 상세 내용 크롤링 시도 (이미 크롤링된 URL은 건너뛰지 않음)
                    articles_with_details = []
                    for article_summary in articles_to_process:
                        url = article_summary.get('url')
                        # **수정:** 이미 크롤링된 URL도 다시 상세 내용을 가져오도록 변경 (항상 최신 본문 확보)
                        # if url and url not in self.crawled_urls:
                        if url:
                            print(f"[Electimes] 상세 내용 가져오는 중: {article_summary.get('title', '제목 없음')}")
                            article_details = self.get_article_content(url) # 상세 내용 크롤링
                            if article_details and article_details.get('content'):
                                # 상세 내용이 있는 경우, 기존 목록 정보에 합침
                                full_article = {**article_summary, **article_details}
                                articles_with_details.append(full_article)
                                print(f"[Electimes] 상세 내용 크롤링 완료: {article_summary.get('title', '제목 없음')}")
                            else:
                                print(f"[Electimes] 상세 내용 크롤링 실패 또는 내용 없음: {article_summary.get('title', '제목 없음')}")
                        else:
                             print(f"[Electimes] URL 정보가 없어 상세 내용 크롤링 스킵: {article_summary.get('title', '제목 없음')}") # Debug log 제거

                    # 상세 내용을 가져온 기사들에 대해 AI 추천 예측
                    articles_after_ai_predict = []
                    if articles_with_details and self.ai_recommender and self.vectorizer:
                        # 텍스트 데이터 준비 (제목 + 본문)
                        texts = [f"{a.get('title', '')} {a.get('content', '')}" for a in articles_with_details]

                        # 벡터화 및 예측
                        try:
                            X_vec = self.vectorizer.transform(texts)
                            # Use the loaded model's predict method directly
                            preds = self.ai_recommender.predict(X_vec)

                            for i, article in enumerate(articles_with_details):
                                article['ai_recommend'] = bool(preds[i])
                                articles_after_ai_predict.append(article)
                            print(f"[Electimes] AI 추천 예측 완료 ({len(articles_after_ai_predict)}건)")
                        except Exception as predict_e:
                            print(f"[Electimes] AI 추천 예측 중 오류 발생: {str(predict_e)}")
                            print(traceback.format_exc())
                            # 예측 실패 시 AI 추천은 기본값(False) 유지
                            articles_after_ai_predict = articles_with_details # 오류 발생해도 다음 단계로 넘어가도록
                    else:
                        # AI 모델 없거나 예측 대상 없으면 AI 추천 필터링 건너뛰고 다음 단계로
                        articles_after_ai_predict = articles_with_details
                        if not (self.ai_recommender and self.vectorizer):
                             print("[Electimes] AI 추천 모델이 로드되지 않아 예측을 건너뜠습니다.")

                    # 3. 키워드 및 AI 추천 필터링 (최종 대상 선정)
                    final_articles_to_sync = []
                    for article in articles_after_ai_predict:
                        # 키워드 포함 여부 확인 및 매칭된 키워드 추출 (본문 포함)
                        title_and_content = f"{article.get('title', '')} {article.get('content', '')}"
                        contains_kw, matched_keywords = self.contains_keywords_and_extract(title_and_content)
                        
                        # 매칭된 키워드를 기사에 저장
                        if matched_keywords:
                            article['keywords'] = matched_keywords
                            print(f"[Electimes] 키워드 매칭: {article.get('title', '제목 없음')} → {matched_keywords}")

                        # AI 추천 결과 확인 (AI 모델 로드된 경우에만 필터링 적용)
                        passes_ai_filter = True # 기본적으로 통과 (AI 모델 없는 경우)
                        if self.ai_recommender and self.vectorizer:
                             # AI 추천 결과가 True인 기사만 통과
                             passes_ai_filter = article.get('ai_recommend', False)
                             # print(f"[Electimes] 기사 '{article.get('title', '')}': 키워드={contains_kw}, AI추천={article.get('ai_recommend', False)}, 통과={contains_kw and passes_ai_filter}") # Debug log 제거

                        # 최종 필터링: 키워드 포함 OR AI 추천 True
                        # 키워드가 포함되어 있거나 AI가 추천한 경우 크롤링 대상
                        if contains_kw or (self.ai_recommender and article.get('ai_recommend', False)):
                            final_articles_to_sync.append(article)
                            # 성공적으로 처리된 기사 URL 저장
                            self.save_crawled_url(article.get('url'))
                            
                            # 크롤링 이유 표시
                            reason = []
                            if contains_kw:
                                reason.append(f"키워드: {matched_keywords}")
                            if article.get('ai_recommend', False):
                                reason.append("AI추천")
                            print(f"[Electimes] 최종 크롤링 대상: {article.get('title', '제목 없음')} (이유: {', '.join(reason)})")
                        # else:
                        #      print(f"[Electimes] 최종 제외: {article.get('title', '제목 없음')} (키워드: {contains_kw}, AI추천 통과: {passes_ai_filter}))") # Debug log 제거

                    crawled_articles_details.extend(final_articles_to_sync)

                except Exception as process_e:
                    print(f"[Electimes] 페이지 {page} 기사 처리 중 오류 발생: {str(process_e)}")
                    print(traceback.format_exc())
                    # 오류 발생 시 해당 페이지의 나머지 기사는 건너뛸 수 있음 (구현에 따라 다름)

            page += 1 # 다음 페이지로 이동

        print(f"[Electimes] 크롤링 종료. 총 {len(crawled_articles_details)}건의 기사 크롤링 완료.")
        return crawled_articles_details

    def get_article_content(self, url: str) -> Dict[str, Any]:
        """🔧 개선된 기사 상세 내용 가져오기 (스마트 재시도 적용)"""
        
        # Extract idxno from URL for debug filename
        match_idxno = re.search(r'idxno=(\d+)', url)
        idxno = match_idxno.group(1) if match_idxno else 'unknown'
        debug_file = f"debug_article_{idxno}.html"

        def fetch_article():
            """실제 기사 가져오기 작업"""
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'

            # Save HTML content to file for debugging
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Saved HTML content to {debug_file}")

            return response.text

        # 🚀 스마트 재시도 시스템 사용
        html_content = self._smart_retry(
            operation_name=f"기사 내용 가져오기 ({url})",
            operation_func=fetch_article,
            max_retries=3,
            base_delay=2.0
        )

        if not html_content:
            print(f"[Electimes] ❌ 기사 내용 가져오기 최종 실패: {url}")
            return {'content': '', 'attachments': [], 'published_date': None}

        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        published_date = None

        # 1. Try to find date in article header
        article_header = soup.select_one('.article-header')
        if article_header:
            date_text = article_header.get_text()
            print(f"Found article header text: {date_text}")
            date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', date_text)
            if date_match:
                # 🔧 안전한 날짜 파싱 메서드 사용
                published_date = self._parse_date_safely(date_match.group(1))
                if published_date:
                    print(f"Extracted date from article header: {published_date}")
                else:
                    print(f"Error parsing article header date: {date_match.group(1)}")

        # 2. Try meta tag if not found in header
        if not published_date:
            meta_time = soup.find('meta', {'property': 'article:published_time'})
            if meta_time and meta_time.get('content'):
                # 🔧 안전한 날짜 파싱으로 개선 
                date_str = meta_time['content'][:10]
                print(f"Found meta date string: {date_str}")
                
                # 연도 조정 후 파싱 시도
                date_parts = date_str.split('-')
                if len(date_parts) == 3:
                    current_year = datetime.now().year
                    adjusted_date_str = f"{current_year}-{date_parts[1]}-{date_parts[2]}"
                    published_date = self._parse_date_safely(adjusted_date_str)
                    if published_date:
                        print(f"Extracted date from meta (adjusted year): {published_date}")
                    else:
                        print(f"Error parsing meta published_time: {adjusted_date_str}")

        # 3. Fallback: <li>입력 YYYY.MM.DD HH:MM</li>
        if not published_date:
            li_input = soup.find('li', string=re.compile(r'입력'))
            if li_input:
                print(f"Found input li text: {li_input.text}")
                date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', li_input.text)
                if date_match:
                    # 🔧 안전한 날짜 파싱 메서드 사용
                    published_date = self._parse_date_safely(date_match.group(1))
                    if published_date:
                        print(f"Extracted date from <li>: {published_date}")
                    else:
                        print(f"Error parsing <li> date: {date_match.group(1)}")

        if not published_date:
            print("Date not found in any source.")

        # Extract content
        content = ''
        content_selectors = ['.view-cont', '.article-content', '.article-body', '#article-view-content-div', '.content']
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element and content_element.text.strip():
                content = content_element.text.strip()
                break
        if not content or len(content.strip()) < 10:
            content = '본문 추출 실패'
        print(f"Extracted content length: {len(content)}")
        if len(content) > 100:
            print(f"Content preview: {content[:100]}...")

        print(f"Successfully processed article: {url}")
        return {
            'content': content,
            'attachments': [],
            'published_date': published_date
        } 