#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 전력산업 뉴스 크롤러 - 메인 실행 스크립트
- 전기신문 뉴스 자동 수집
- Notion 자동 동기화  
- AI 추천 시스템 학습/업데이트
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# 프로젝트 모듈 import (실제 사용되는 것만)
from notion.notion_client import NotionClient
from crawlers.electimes_crawler import ElectimesCrawler
from ai_recommender import fit_and_save_model, update_notion_ai_recommend_all

def setup_logging():
    """로깅 시스템 설정"""
    # 로그 디렉토리 생성
    os.makedirs('logs', exist_ok=True)
    
    # 로깅 설정
    log_filename = f'logs/crawler_{datetime.now().strftime("%Y%m%d")}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def main():
    """메인 실행 함수"""
    logger = setup_logging()
    
    try:
        logger.info("🚀 전력산업 뉴스 크롤러 시작")
        
        # 환경변수 로드
        load_dotenv()
        logger.info("✅ 환경변수 로드 완료")
        
        # 1️⃣ Notion 클라이언트 초기화
        notion = NotionClient()
        logger.info("✅ NotionClient 초기화 완료")
        
        # 2️⃣ 크롤러 초기화 및 실행
        crawler = ElectimesCrawler(notion)
        logger.info("✅ ElectimesCrawler 초기화 완료")
        
        articles = crawler.crawl()
        logger.info(f"📰 크롤링 완료: {len(articles)}개 기사")
        
        if not articles:
            logger.warning("⚠️ 크롤링된 기사가 없습니다")
            return
        
        # 3️⃣ Notion 데이터베이스 연결
        database_id = notion.get_weekly_database_id()
        if not database_id:
            logger.error("❌ Notion 데이터베이스 ID를 가져올 수 없습니다")
            return
        
        logger.info(f"✅ 데이터베이스 연결 완료: {database_id}")
        
        # 4️⃣ Notion 동기화
        notion.sync_articles(articles, database_id)
        logger.info(f"💾 Notion 동기화 완료: {len(articles)}개 기사")
        
        # 5️⃣ AI 추천 모델 학습
        try:
            fit_and_save_model(notion)
            logger.info("🤖 AI 추천 모델 학습 완료")
        except Exception as ai_error:
            logger.warning(f"⚠️ AI 모델 학습 실패: {str(ai_error)}")
        
        # 6️⃣ AI 추천 업데이트
        try:
            update_notion_ai_recommend_all()
            logger.info("🔄 AI 추천 업데이트 완료")
        except Exception as update_error:
            logger.warning(f"⚠️ AI 추천 업데이트 실패: {str(update_error)}")
        
        logger.info("🎉 전체 프로세스 완료!")
        
    except Exception as e:
        logger.error(f"💥 실행 중 오류 발생: {str(e)}")
        logger.error(f"📍 오류 유형: {e.__class__.__name__}")
        import traceback
        logger.error(f"📝 스택 트레이스:\n{traceback.format_exc()}")
        raise

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 전력산업 뉴스 크롤러")
    print("🔗 전기신문 → Notion 자동 동기화")
    print("=" * 60)
    main()
