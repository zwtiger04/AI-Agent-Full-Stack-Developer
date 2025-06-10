#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 최신 스크롤 카드뉴스 시스템 실행 스크립트
"""

import os
import sys
import shutil
from datetime import datetime

def main():
    print("🚀 최신 스크롤 카드뉴스 시스템 실행!")
    print("=" * 60)
    
    try:
        # 환경 설정
        print("\n1️⃣ 환경 설정 중...")
        from notion.notion_client import NotionClient
        from html_card_news.scroll_detail_generator import ScrollDetailGenerator
        from html_card_news.enhanced_card_system import EnhancedCardNewsSystem
        
        print("✅ 모든 모듈 임포트 성공!")
        
        # 시스템 초기화
        print("\n2️⃣ 시스템 초기화 중...")
        notion = NotionClient()
        detail_generator = ScrollDetailGenerator()
        system = EnhancedCardNewsSystem()
        system.detail_generator = detail_generator
        
        print("✅ 시스템 초기화 완료!")
        
        # 데이터베이스 선택
        print("\n3️⃣ 노션 데이터베이스 접근 중...")
        database_id = notion.get_weekly_database_id()
        
        if not database_id:
            print("❌ 데이터베이스를 찾을 수 없습니다!")
            return
            
        print(f"✅ 현재 주차 데이터베이스 찾음: {database_id}")
        
        # 기사 가져오기
        print("\n4️⃣ 기사 가져오는 중...")
        articles = notion.get_all_articles_from_database(database_id)
        
        # AI 추천 또는 관심 기사 필터링
        filtered_articles = [
            article for article in articles 
            if article.get('ai_recommend') or article.get('interest')
        ]
        
        print(f"📊 전체 기사: {len(articles)}개")
        print(f"✨ AI추천/관심 기사: {len(filtered_articles)}개")
        
        if not filtered_articles:
            print("\n💡 AI 추천이나 관심 표시된 기사가 없어서 최신 기사 5개를 사용합니다.")
            filtered_articles = articles[:5]
        else:
            # 최대 10개로 제한
            filtered_articles = filtered_articles[:10]
        
        if not filtered_articles:
            print("❌ 처리할 기사가 없습니다!")
            return
            
        # 카드뉴스 생성
        print(f"\n5️⃣ {len(filtered_articles)}개 기사로 카드뉴스 생성 중...")
        result = system.generate_complete_system(filtered_articles)
        
        if result.get('summary'):
            print("\n✅ 카드뉴스 생성 완료!")
            
            # Windows로 복사
            print("\n6️⃣ Windows로 파일 복사 중...")
            windows_dir = "/mnt/c/Users/KJ/Desktop/PowerNews_Latest"
            os.makedirs(windows_dir, exist_ok=True)
            
            # 요약 파일 복사
            summary_filename = os.path.basename(result['summary'])
            shutil.copy2(result['summary'], os.path.join(windows_dir, summary_filename))
            
            # 상세 파일들 복사
            detail_dir = os.path.join(windows_dir, 'detailed')
            os.makedirs(detail_dir, exist_ok=True)
            
            src_detail_dir = os.path.join(system.output_dir, 'detailed')
            copied_count = 0
            for filename in result['details'].values():
                src = os.path.join(src_detail_dir, filename)
                dst = os.path.join(detail_dir, filename)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    copied_count += 1
            
            print(f"\n🎉 모든 작업 완료!")
            print(f"📁 요약 페이지: C:\\Users\\KJ\\Desktop\\PowerNews_Latest\\{summary_filename}")
            print(f"📁 상세 페이지: C:\\Users\\KJ\\Desktop\\PowerNews_Latest\\detailed\\ ({copied_count}개 파일)")
            print(f"\n💡 브라우저에서 요약 페이지를 열어 확인하세요!")
        else:
            print("❌ 카드뉴스 생성 실패!")
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n💡 문제 해결 방법:")
        print("1. 환경변수(.env) 파일에 NOTION_API_KEY가 설정되어 있는지 확인")
        print("2. 노션 데이터베이스에 접근 권한이 있는지 확인")
        print("3. 필요한 패키지가 모두 설치되어 있는지 확인")

if __name__ == "__main__":
    main()
