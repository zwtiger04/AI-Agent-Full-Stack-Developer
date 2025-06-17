#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 관심 기사 모니터링 시스템
- 노션에서 관심 체크된 기사를 주기적으로 확인
- 새로운 관심 기사 발견 시 카드뉴스 생성 대기열에 추가
"""

import time
import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Set
from notion.notion_client import NotionClient

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/interest_monitor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class InterestMonitor:
    """관심 기사 모니터링 클래스"""
    
    def __init__(self):
        """초기화"""
        self.notion = NotionClient()
        self.processed_file = 'processed_articles.json'
        self.pending_file = '/home/zwtiger/AI-Agent-Full-Stack-Developer/data/card_news/json/pending_cardnews.json'
        self.processed_articles = self.load_processed()
        
        # 로그 디렉토리 생성
        os.makedirs('logs', exist_ok=True)
        
        logger.info("🔍 관심 기사 모니터링 시스템 초기화 완료")
        
    def load_processed(self) -> Set[str]:
        """이미 처리한 기사 ID 로드"""
        try:
            if os.path.exists(self.processed_file):
                with open(self.processed_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"📋 기존 처리 기사 {len(data)}개 로드")
                    return set(data)
        except Exception as e:
            logger.error(f"❌ 처리 기사 로드 실패: {str(e)}")
        return set()
    
    def save_processed(self, article_id: str):
        """처리 완료한 기사 ID 저장"""
        self.processed_articles.add(article_id)
        try:
            with open(self.processed_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.processed_articles), f, ensure_ascii=False, indent=2)
            logger.info(f"✅ 처리 완료 기사 저장: {article_id}")
        except Exception as e:
            logger.error(f"❌ 처리 기사 저장 실패: {str(e)}")
    
    def check_new_interests(self) -> List[Dict]:
        """새로운 관심 기사 확인"""
        try:
            # 모든 주차의 관심 기사 가져오기
            logger.info("🔄 노션에서 관심 기사 확인 중...")
            interested = self.notion.get_interested_articles()
            
            new_articles = []
            for article in interested:
                # 이미 처리한 기사는 건너뛰기
                if article['page_id'] not in self.processed_articles:
                    new_articles.append(article)
                    logger.info(f"✨ 새로운 관심 기사 발견: {article['title']}")
            
            if new_articles:
                logger.info(f"📊 총 {len(new_articles)}개의 새로운 관심 기사 발견")
            else:
                logger.info("📭 새로운 관심 기사 없음")
                
            return new_articles
            
        except Exception as e:
            logger.error(f"❌ 관심 기사 확인 중 오류: {str(e)}")
            return []
    
    def save_pending_articles(self, articles: List[Dict]):
        """대기 중인 카드뉴스 기사 저장"""
        try:
            # 기존 대기 기사 로드
            existing = []
            if os.path.exists(self.pending_file):
                with open(self.pending_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            
            # 새 기사 추가 (중복 제거)
            existing_ids = {a['page_id'] for a in existing}
            for article in articles:
                if article['page_id'] not in existing_ids:
                    existing.append(article)
            
            # 저장
            with open(self.pending_file, 'w', encoding='utf-8') as f:
                json.dump(existing, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 대기 중인 카드뉴스 {len(existing)}개 저장")
            
        except Exception as e:
            logger.error(f"❌ 대기 기사 저장 실패: {str(e)}")
    
    def run(self, interval: int = 300):
        """모니터링 실행 (기본 5분 간격)"""
        logger.info(f"🚀 모니터링 시작 (체크 간격: {interval}초)")
        
        try:
            check_count = 0
            while True:
                check_count += 1
                logger.info(f"\n{'='*50}")
                logger.info(f"🔍 체크 #{check_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # 새로운 관심 기사 확인
                new_articles = self.check_new_interests()
                
                if new_articles:
                    # 대기 목록에 저장
                    self.save_pending_articles(new_articles)
                    
                    # 알림 (선택적)
                    self.notify_new_articles(new_articles)
                
                # 대기
                logger.info(f"💤 다음 체크까지 {interval}초 대기...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("\n👋 모니터링 종료 (사용자 중단)")
        except Exception as e:
            logger.error(f"\n❌ 모니터링 중 오류 발생: {str(e)}")
            raise
    
    def notify_new_articles(self, articles: List[Dict]):
        """새 기사 알림 (확장 가능)"""
        logger.info("\n🔔 새로운 관심 기사 알림:")
        for i, article in enumerate(articles, 1):
            logger.info(f"  {i}. {article['title']}")
            if article.get('keywords'):
                logger.info(f"     키워드: {', '.join(article['keywords'])}")
        
    def mark_as_processed(self, article_id: str):
        """기사를 처리 완료로 표시"""
        self.save_processed(article_id)
        
        # pending 목록에서 제거
        try:
            if os.path.exists(self.pending_file):
                with open(self.pending_file, 'r', encoding='utf-8') as f:
                    pending = json.load(f)
                
                # 해당 기사 제거
                pending = [a for a in pending if a['page_id'] != article_id]
                
                with open(self.pending_file, 'w', encoding='utf-8') as f:
                    json.dump(pending, f, ensure_ascii=False, indent=2)
                    
                logger.info(f"✅ 대기 목록에서 제거: {article_id}")
                
        except Exception as e:
            logger.error(f"❌ 대기 목록 업데이트 실패: {str(e)}")


def main():
    """메인 실행 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='관심 기사 모니터링')
    parser.add_argument('--interval', type=int, default=300, 
                       help='체크 간격 (초, 기본: 300)')
    parser.add_argument('--once', action='store_true',
                       help='한 번만 체크하고 종료')
    
    args = parser.parse_args()
    
    # 모니터 생성
    monitor = InterestMonitor()
    
    if args.once:
        # 한 번만 체크
        logger.info("🔍 단일 체크 모드")
        new_articles = monitor.check_new_interests()
        if new_articles:
            monitor.save_pending_articles(new_articles)
            monitor.notify_new_articles(new_articles)
    else:
        # 지속적 모니터링
        monitor.run(interval=args.interval)


if __name__ == "__main__":
    main()
