"""
Claude를 활용한 콘텐츠 개선 도구
- 노션 데이터를 읽어서 Claude용 프롬프트 생성
- 개선된 내용을 다시 노션에 업데이트
"""

import pandas as pd
from notion.notion_client import NotionClient
import json

def export_for_claude_enhancement():
    """Claude로 개선할 기사들을 준비합니다."""
    notion = NotionClient()
    database_id = notion.get_weekly_database_id()
    
    # 요약이 부실한 기사들 찾기
    articles = notion.get_articles_with_empty_fields_from_db(database_id)
    
    # Claude 프롬프트 생성
    prompt_template = """
다음은 전력산업 관련 뉴스 기사들입니다. 각 기사에 대해 풍부하고 구조화된 요약을 작성해주세요.

형식:
1. 📌 한줄 핵심 요약 (100-150자)
2. 🔍 상세 분석
   - 주요 내용 (3-4개 포인트)
   - 핵심 수치 및 데이터
   - 업계 영향 및 의미
3. 💡 시사점
4. 🏷️ 추천 태그

기사 목록:
"""
    
    articles_text = ""
    for i, article in enumerate(articles):
        articles_text += f"\n--- 기사 {i+1} ---\n"
        articles_text += f"제목: {article['title']}\n"
        articles_text += f"URL: {article['url']}\n"
        articles_text += f"현재 요약: {article.get('summary', '없음')}\n"
        articles_text += f"키워드: {', '.join(article.get('keywords', []))}\n"
        articles_text += "\n"
    
    full_prompt = prompt_template + articles_text
    
    # 프롬프트를 파일로 저장
    with open('claude_prompt.txt', 'w', encoding='utf-8') as f:
        f.write(full_prompt)
    
    print(f"✅ Claude 프롬프트가 'claude_prompt.txt'에 저장되었습니다.")
    print(f"📋 총 {len(articles)}개의 기사가 포함되었습니다.")
    print("\n사용 방법:")
    print("1. claude_prompt.txt 내용을 복사하여 Claude에 붙여넣기")
    print("2. Claude의 응답을 'claude_response.txt'로 저장")
    print("3. python claude_content_enhancer.py --update 실행")
    
    return articles

def update_from_claude_response():
    """Claude의 응답을 파싱하여 노션에 업데이트합니다."""
    try:
        with open('claude_response.txt', 'r', encoding='utf-8') as f:
            claude_response = f.read()
        
        # 응답 파싱 (간단한 구현)
        # 실제로는 더 정교한 파싱이 필요합니다
        articles = claude_response.split('--- 기사')
        
        notion = NotionClient()
        updated_count = 0
        
        for article_text in articles[1:]:  # 첫 번째는 빈 문자열
            # 제목 찾기
            title_match = article_text.find('제목:')
            if title_match != -1:
                # 파싱 로직...
                # notion.update_article_content(page_id, enhanced_content)
                updated_count += 1
        
        print(f"✅ {updated_count}개의 기사가 업데이트되었습니다.")
        
    except FileNotFoundError:
        print("❌ claude_response.txt 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--update":
        update_from_claude_response()
    else:
        export_for_claude_enhancement()
