#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖼️ 카드뉴스 업로드 예제 스크립트
이 스크립트를 실행하면 지정된 폴더의 이미지들을 GitHub에 업로드하고
Notion에 자동으로 페이지를 생성합니다.
"""

from card_news_uploader import CardNewsUploader
import sys
import os

def main():
    """메인 실행 함수"""
    # 업로더 초기화
    uploader = CardNewsUploader()
    
    # 명령줄 인자로 폴더 경로 받기
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        # 기본 폴더 경로
        folder_path = "card_news/images/test"
        print(f"폴더 경로가 지정되지 않았습니다. 기본 경로 사용: {folder_path}")
    
    # 폴더 존재 확인
    if not os.path.exists(folder_path):
        print(f"❌ 폴더를 찾을 수 없습니다: {folder_path}")
        print("\n사용법: python upload_card_news_example.py [폴더경로]")
        print("예시: python upload_card_news_example.py card_news/images/20250608_전력산업")
        return
    
    # 제목과 설명 입력받기 (선택사항)
    print(f"\n📁 업로드할 폴더: {folder_path}")
    title = input("📝 카드뉴스 제목 (Enter로 폴더명 사용): ").strip()
    if not title:
        title = os.path.basename(folder_path)
    
    description = input("📝 설명 (선택사항, Enter로 건너뛰기): ").strip()
    
    # 키워드 입력받기
    keywords_input = input("🏷️ 키워드 (쉼표로 구분, Enter로 건너뛰기): ").strip()
    keywords = [k.strip() for k in keywords_input.split(',')] if keywords_input else None
    
    print("\n" + "="*60)
    print(f"📌 제목: {title}")
    print(f"📌 설명: {description if description else '없음'}")
    print(f"📌 키워드: {', '.join(keywords) if keywords else '없음'}")
    print("="*60 + "\n")
    
    # 확인
    confirm = input("계속하시겠습니까? (y/N): ").strip().lower()
    if confirm != 'y':
        print("취소되었습니다.")
        return
    
    # 업로드 실행
    success = uploader.upload_card_news_folder(
        folder_path=folder_path,
        title=title,
        description=description,
        keywords=keywords
    )
    
    if success:
        print("\n🎉 카드뉴스 업로드가 완료되었습니다!")
        print("📝 업로드 기록은 card_news/upload_history.json에 저장되었습니다.")
    else:
        print("\n❌ 카드뉴스 업로드에 실패했습니다.")


if __name__ == "__main__":
    main()
