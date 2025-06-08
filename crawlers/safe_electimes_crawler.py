#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Phase 2: 메모리 누수 방지가 적용된 안전한 ElectimesCrawler

**주요 개선사항**:
- Context Manager 패턴으로 리소스 자동 관리
- 메모리 효율적 배치 처리
- 예외 안전성 보장
- 리소스 누수 방지
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Iterator
from bs4 import BeautifulSoup
import requests
import json
import os
import re
import time
import random
import pytz
import gc
from contextlib import contextmanager

# Phase 1 개선사항 임포트
try:
    from crawlers.resource_managers import ResourceMonitor, SessionManager
except ImportError:
    print("⚠️ resource_managers 임포트 실패 - 기본 리소스 관리 사용")
    ResourceMonitor = None
    SessionManager = None

# 기존 imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    from crawlers.base_crawler import BaseCrawler
    from recommenders.article_recommender import ArticleRecommender
    from notion.notion_client import NotionClient
    import joblib
    from processors.keyword_processor import KeywordProcessor
    from ai_update_content import clean_article_content, generate_one_line_summary_with_llm, generate_key_content
    FULL_DEPENDENCIES = True
except ImportError:
    FULL_DEPENDENCIES = False
    BaseCrawler = object


class SafeElectimesCrawler(BaseCrawler if FULL_DEPENDENCIES else object):
    """
    🔧 메모리 누수 방지가 적용된 안전한 전기신문 크롤러
    
    **Context Manager 패턴 적용**:
    - with 문으로 사용하여 자동 리소스 정리
    - 예외 발생 시에도 안전한 정리 보장
    - 메모리 사용량 모니터링 및 제한
    """
    
    # 전력 산업 관련 키워드
    KEYWORDS = [
        '재생에너지', '전력중개사업', 'VPP', '전력시장', 'ESS', 
        '출력제어', '중앙계약', '저탄소 용량', 
        '재생에너지입찰', '보조서비스', 
        '예비력시장', '하향예비력', '계통포화',
        '전력망', '기후에너지부', '태양광', '전력감독원'
    ]
    
    def __init__(self, notion_client=None, recommender=None, 
                 batch_size: int = 50, memory_limit_mb: float = 100):
        """
        초기화 (Context Manager로 사용하기 위해 리소스 초기화는 __enter__에서)
        """
        if FULL_DEPENDENCIES:
            super().__init__('전기신문', 'https://www.electimes.com')
        
        self.base_url = 'https://www.electimes.com'
        self.list_url = f"{self.base_url}/news/articleList.html?view_type=sm"
        self._source_name = '전기신문'
        self.batch_size = batch_size
        self.memory_limit_mb = memory_limit_mb
        
        # 크롤링 이력
        self.history_file = 'crawled_articles.json'
        self.crawled_urls = set()
        
        # 리소스들 (Context Manager에서 관리)
        self.session = None
        self.driver = None
        self.resource_monitor = None
        
        # AI 관련 (선택적)
        self.notion_client = notion_client
        self.ai_recommender = recommender
        self.vectorizer = None
        
        print("SafeElectimesCrawler 준비 완료 (Context Manager로 사용)")

    def __enter__(self):
        """Context Manager 진입: 모든 리소스 초기화"""
        print("🚀 SafeElectimesCrawler 리소스 초기화 중...")
        
        try:
            # 1. 리소스 모니터링 시작
            if ResourceMonitor:
                self.resource_monitor = ResourceMonitor(warning_threshold_mb=self.memory_limit_mb)
                self.resource_monitor.__enter__()
            
            # 2. HTTP Session 초기화
            if SessionManager:
                self.session_manager = SessionManager()
                self.session = self.session_manager.__enter__()
            else:
                # Fallback: 기본 requests 사용
                self.session = requests.Session()
                self.session.headers.update({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
            
            # 3. 크롤링 이력 로드
            self.crawled_urls = self.load_crawled_urls()
            
            # 4. AI 모델 로드 (선택적)
            self._load_ai_models()
            
            print("✅ SafeElectimesCrawler 초기화 완료")
            return self
            
        except Exception as e:
            print(f"❌ SafeElectimesCrawler 초기화 실패: {e}")
            self._cleanup_all()
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context Manager 종료: 모든 리소스 안전 정리"""
        print("🔄 SafeElectimesCrawler 리소스 정리 중...")
        
        self._cleanup_all()
        
        if exc_type:
            print(f"⚠️ 예외와 함께 종료: {exc_type.__name__}: {exc_val}")
        else:
            print("✅ SafeElectimesCrawler 정상 종료")
    
    def _cleanup_all(self):
        """모든 리소스 정리"""
        
        # Session 정리
        if hasattr(self, 'session_manager') and self.session_manager:
            try:
                self.session_manager.__exit__(None, None, None)
            except Exception as e:
                print(f"⚠️ Session 정리 중 오류: {e}")
        elif self.session:
            try:
                self.session.close()
            except Exception as e:
                print(f"⚠️ Session 정리 중 오류: {e}")
        
        # 리소스 모니터링 종료
        if self.resource_monitor:
            try:
                self.resource_monitor.__exit__(None, None, None)
            except Exception as e:
                print(f"⚠️ ResourceMonitor 정리 중 오류: {e}")
        
        # 명시적 가비지 컬렉션
        gc.collect()
    
    def _load_ai_models(self):
        """AI 모델 로드 (선택적)"""
        try:
            model_path = 'feedback/ai_recommend_model.joblib'
            vectorizer_path = 'feedback/ai_recommend_vectorizer.joblib'

            if os.path.exists(model_path) and os.path.exists(vectorizer_path):
                if FULL_DEPENDENCIES:
                    self.ai_recommender = joblib.load(model_path)
                    self.vectorizer = joblib.load(vectorizer_path)
                    print("✅ AI 추천 모델 로드 완료")
                else:
                    print("⚠️ joblib 없음 - AI 모델 로드 건너뜀")
            else:
                print("ℹ️ AI 모델 파일 없음 - 기본 크롤링만 수행")
        except Exception as e:
            print(f"⚠️ AI 모델 로드 중 오류: {e}")

    def load_crawled_urls(self) -> set:
        """이전에 크롤링한 URL 목록을 로드"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
            except Exception as e:
                print(f"⚠️ 크롤링 이력 로드 오류: {str(e)}")
        return set()

    def save_crawled_url(self, url: str):
        """크롤링한 URL을 안전하게 저장"""
        self.crawled_urls.add(url)
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.crawled_urls), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 크롤링 이력 저장 오류: {str(e)}")

    def _parse_date_safely(self, date_str: str) -> Optional[datetime]:
        """🔧 Phase 1: 안전한 날짜 파싱 메서드"""
        if not date_str or not date_str.strip():
            return None
            
        date_str = date_str.strip()
        
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
                
                if '%Y' not in pattern:
                    current_year = datetime.now().year
                    parsed_date = parsed_date.replace(year=current_year)
                
                return parsed_date
                
            except ValueError:
                continue
        
        return None

    def _smart_retry(self, operation_name: str, operation_func, max_retries: int = 3, base_delay: float = 2.0):
        """🔧 Phase 1: 스마트 네트워크 재시도 시스템"""
        retryable_exceptions = (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        )
        
        for attempt in range(max_retries):
            try:
                result = operation_func()
                return result
                
            except retryable_exceptions as e:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    jitter = random.uniform(0.1, 0.3) * delay
                    total_delay = delay + jitter
                    
                    print(f"   ⚠️ {operation_name} 재시도 {attempt + 1}/{max_retries}: {total_delay:.1f}초 대기")
                    time.sleep(total_delay)
                else:
                    print(f"   ❌ {operation_name} 최종 실패: {str(e)}")
                    break
                    
            except Exception as e:
                print(f"   ❌ {operation_name} 예상치 못한 오류: {str(e)}")
                break
        
        return None

    def is_recent_article(self, date: datetime) -> bool:
        """기사가 한국 시간 기준으로 최근 3일 내의 것인지 확인"""
        kst = pytz.timezone('Asia/Seoul')
        now_kst = datetime.now(kst)
        today_kst = now_kst.date()
        three_days_ago_kst = today_kst - timedelta(days=3)

        article_date = date.date()
        is_recent = article_date >= three_days_ago_kst
        return is_recent

    def contains_keywords(self, text: str) -> bool:
        """텍스트에 키워드가 포함되어 있는지 확인"""
        found_keywords = [keyword for keyword in self.KEYWORDS if keyword in text]
        return len(found_keywords) > 0

    @contextmanager
    def batch_processor(self, items: List[Any]) -> Iterator[List[Any]]:
        """🔧 Phase 2: 메모리 효율적 배치 처리"""
        print(f"📦 배치 처리 시작: {len(items)}개 항목 (배치 크기: {self.batch_size})")
        
        try:
            for i in range(0, len(items), self.batch_size):
                batch = items[i:i + self.batch_size]
                
                print(f"   처리 중: 배치 {i // self.batch_size + 1} ({len(batch)}개 항목)")
                
                yield batch
                
                # 배치 처리 후 메모리 정리
                gc.collect()
                
        except Exception as e:
            print(f"❌ 배치 처리 중 오류: {e}")
            raise
        
        print(f"✅ 배치 처리 완료")

    def crawl_safely(self, max_pages: int = 5) -> Iterator[Dict[str, Any]]:
        """
        🔧 Phase 2: 메모리 효율적 안전 크롤링
        
        **특징**:
        - 스트리밍 방식으로 메모리 사용량 제한
        - 배치 단위 처리로 대용량 데이터 처리 가능
        - 예외 안전성 보장
        
        Args:
            max_pages: 최대 크롤링 페이지 수
            
        Yields:
            Dict[str, Any]: 크롤링된 기사 정보
        """
        print(f"🚀 안전 크롤링 시작 (최대 {max_pages}페이지)")
        
        total_articles = 0
        recent_articles = 0
        keyword_matched = 0
        
        for page in range(1, max_pages + 1):
            print(f"📄 페이지 {page} 처리 중...")
            
            # 페이지별 기사 목록 가져오기
            page_articles = self._fetch_articles_safely(page)
            
            if not page_articles:
                print(f"   페이지 {page}에서 기사 없음 - 크롤링 종료")
                break
    def crawl_safely(self, max_pages: int = 5) -> Iterator[Dict[str, Any]]:
        """
        🔧 Phase 2: 메모리 효율적 안전 크롤링
        """
        print(f"🚀 안전 크롤링 시작 (최대 {max_pages}페이지)")
        
        total_articles = 0
        recent_articles = 0
        keyword_matched = 0
        
        for page in range(1, max_pages + 1):
            print(f"📄 페이지 {page} 처리 중...")
            
            # 페이지별 기사 목록 가져오기
            page_articles = self._fetch_articles_safely(page)
            
            if not page_articles:
                print(f"   페이지 {page}에서 기사 없음 - 크롤링 종료")
                break
            
            total_articles += len(page_articles)
            
            # 기사별 처리 (배치 처리 수정)
            for article in page_articles:
                # 날짜 필터링
                if not article.get("published_date") or not self.is_recent_article(article["published_date"]):
                    continue
                
                recent_articles += 1
                
                # 키워드 필터링
                title_and_content = article.get("title", "") + " " + article.get("content", "")
                if not self.contains_keywords(title_and_content):
                    continue
                
                keyword_matched += 1
                
                # URL 저장
                if article.get("url"):
                    self.save_crawled_url(article["url"])
                
                # 메모리 효율적으로 하나씩 yield
                yield article
            
            # 페이지 처리 후 가비지 컬렉션
            gc.collect()
                        if article.get('url'):
                            self.save_crawled_url(article['url'])
                        
                        # 메모리 효율적으로 하나씩 yield
                        yield article
            
            # 페이지 처리 후 가비지 컬렉션
            gc.collect()
        
        print(f"📊 크롤링 완료 통계:")
        print(f"   전체 기사: {total_articles}개")
        print(f"   최근 기사: {recent_articles}개")
        print(f"   키워드 매칭: {keyword_matched}개")

    def _fetch_articles_safely(self, page: int = 1) -> List[Dict[str, Any]]:
        """안전한 기사 목록 가져오기"""
        url = f"{self.list_url}&page={page}"
        
        def fetch_page():
            if not self.session:
                raise RuntimeError("Session이 초기화되지 않았습니다.")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text

        html_content = self._smart_retry(
            operation_name=f"기사 목록 가져오기 (페이지 {page})",
            operation_func=fetch_page,
            max_retries=3,
            base_delay=1.5
        )

        if not html_content:
            return []
            
        return self._parse_articles_from_html(html_content)

    def _parse_articles_from_html(self, html_content: str) -> List[Dict[str, Any]]:
        """HTML에서 기사 정보 추출"""
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        article_items = soup.select('section#section-list li.item')
        
        for item in article_items:
            title_link = item.select_one('h4.titles a.linked')
            date_tag = item.select_one('em.replace-date')
            source_tag = item.select_one('span.byline a')

            title = title_link.text.strip() if title_link else None
            url = self.base_url + title_link['href'] if title_link and title_link.has_attr('href') else None
            date_str = date_tag.text.strip() if date_tag else None
            source = source_tag.text.strip() if source_tag else self._source_name

            # 안전한 날짜 파싱
            published_date = None
            if date_str:
                published_date = self._parse_date_safely(date_str)
                        
            if title and url and published_date:
                articles.append({
                    'title': title,
                    'url': url,
                    'published_date': published_date,
                    'source': source,
                    'content': '',  # 필요 시 별도로 가져옴
                    'keywords': [],
                    'ai_recommend': False
                })
        
        return articles


# 편의 함수: 기존 호환성 유지
def create_safe_crawler(*args, **kwargs):
    """안전한 크롤러 생성 함수"""
    return SafeElectimesCrawler(*args, **kwargs)


# 사용 예시
if __name__ == "__main__":
    print("🧪 SafeElectimesCrawler 테스트")
    
    # Context Manager로 안전하게 사용
    with SafeElectimesCrawler(batch_size=10) as crawler:
        articles = list(crawler.crawl_safely(max_pages=2))
        print(f"✅ 총 {len(articles)}개 기사 수집")
        
        for i, article in enumerate(articles[:3], 1):
            print(f"📰 기사 {i}: {article['title'][:50]}...")
