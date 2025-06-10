#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 간단한 카드뉴스 테스트 - 스크롤 시스템 직접 사용
"""

import os
import sys
import shutil
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def generate_card_news():
    print("🎯 간단한 카드뉴스 생성 테스트!")
    print("=" * 60)
    
    try:
        # 1. 노션에서 데이터 가져오기
        print("\n1️⃣ 노션 데이터 가져오기...")
        from notion.notion_client import NotionClient
        
        notion = NotionClient()
        database_id = notion.get_weekly_database_id()
        
        if not database_id:
            print("❌ 데이터베이스를 찾을 수 없습니다!")
            return
            
        # 최신 기사 가져오기
        articles = notion.get_all_articles_from_database(database_id)
        
        # AI 추천 또는 관심 기사 우선
        filtered = [a for a in articles if a.get('ai_recommend') or a.get('interest')]
        
        # 없으면 최신 기사 사용
        if not filtered:
            filtered = articles[:3]  # 테스트용으로 3개만
            
        print(f"✅ {len(filtered)}개 기사 선택")
        
        # 2. 스크롤 카드뉴스 생성
        print("\n2️⃣ 스크롤 카드뉴스 생성 중...")
        from html_card_news.scroll_detail_generator import ScrollDetailGenerator
        
        generator = ScrollDetailGenerator()
        output_dir = "./card_news_test_output"
        os.makedirs(output_dir, exist_ok=True)
        
        generated_files = []
        
        for i, article in enumerate(filtered):
            print(f"\n  📝 처리 중 ({i+1}/{len(filtered)}): {article.get('title', '제목 없음')[:30]}...")
            
            try:
                # 스크롤 카드 생성
                result_path = generator.create_detailed_card(article)
                
                if result_path and os.path.exists(result_path):
                    # 출력 폴더로 복사
                    filename = f"card_{i+1}_{os.path.basename(result_path)}"
                    dest_path = os.path.join(output_dir, filename)
                    shutil.copy2(result_path, dest_path)
                    generated_files.append(dest_path)
                    print(f"  ✅ 생성 완료: {filename}")
                else:
                    print(f"  ❌ 생성 실패")
                    
            except Exception as e:
                print(f"  ❌ 오류: {e}")
                
        # 3. 결과 요약
        if generated_files:
            print(f"\n✅ 총 {len(generated_files)}개 카드뉴스 생성 완료!")
            
            # Windows로 복사
            windows_dir = "/mnt/c/Users/KJ/Desktop/CardNews_Test"
            try:
                os.makedirs(windows_dir, exist_ok=True)
                
                for file_path in generated_files:
                    filename = os.path.basename(file_path)
                    shutil.copy2(file_path, os.path.join(windows_dir, filename))
                    
                print(f"\n🖥️ Windows 데스크톱으로 복사 완료!")
                print(f"📁 위치: C:\\Users\\KJ\\Desktop\\CardNews_Test\\")
                print(f"\n💡 브라우저에서 HTML 파일을 열어 확인하세요!")
                
                # 첫 번째 파일 미리보기
                if generated_files:
                    print(f"\n📋 생성된 파일 목록:")
                    for f in generated_files:
                        print(f"  - {os.path.basename(f)}")
                        
            except Exception as e:
                print(f"\n⚠️ Windows 복사 실패: {e}")
                print(f"수동으로 복사하세요: {output_dir}")
        else:
            print("\n❌ 생성된 카드뉴스가 없습니다.")
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_card_news()
