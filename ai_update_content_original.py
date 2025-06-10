# from notion.notion_client import NotionClient  # 순환참조 방지: 완전히 삭제
# from crawlers.electimes_crawler import ElectimesCrawler  # 순환참조 방지: 완전히 삭제
import time
import re
import traceback
import requests
import os
from dotenv import load_dotenv
from googletrans import Translator # googletrans-py 임포트

# .env 파일에서 환경변수 로드
load_dotenv()

# Ollama API 엔드포인트 설정 (기본값)
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/v1/chat/completions')
# 사용할 Ollama 모델 설정
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'gemma2:9b-instruct-q5_K_M') # 기본 모델을 Gemma2 9B로 설정

# googletrans-py Translator 객체 초기화
translator = Translator()

def clean_article_content(content: str) -> str:
    """기사 내용을 정제합니다."""
    if not content:
        return ""
    
    # 1. 불필요한 공백 제거
    content = ' '.join(content.split())
    
    # 2. 특수문자 처리
    content = content.replace('&nbsp;', ' ')
    
    # 3. 중복된 마침표 제거
    content = content.replace('..', '.')
    
    return content[:200]

def generate_one_line_summary_rule_based(content: str) -> str:
    """기사 내용의 첫 문장을 추출하여 한 줄로 요약합니다 (규칙 기반)."""
    if not content:
        return ""
    
    # 1. 문장 분리
    sentences = re.split(r'[.?!\n]', content)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # 2. 첫 문장 반환 (길이 제한 없음)
    # 너무 짧은 경우 다음 문장을 포함하는 로직은 generate_one_line_summary_with_llm에서 처리
    # 규칙 기반에서는 단순 첫 문장 또는 특정 길이까지 반환하도록 구현
    summary = sentences[0] if sentences else ""
    
    # 간단한 길이 제한 (예: 200자)
    return summary[:200]

def generate_key_content_rule_based(content: str) -> str:
    """기사 내용의 첫 2~3 문단을 추출하여 핵심 내용으로 사용합니다 (규칙 기반)."""
    if not content:
        return ""
    
    # 1. 문단 분리 (줄바꿈 2개 이상 기준)
    paragraphs = re.split(r'\n{2,}', content)
    
    # 2. 첫 2~3개 문단 결합 (최대 3개 문단)
    key_paragraphs = paragraphs[:3]
    key_content = "\n\n".join(key_paragraphs)
    
    # 간단한 길이 제한 (예: 1000자)
    return key_content[:1000]

def generate_one_line_summary_with_llm(content: str, use_llm: bool = True) -> str:
    """LLM을 사용하여 기사 내용을 한 줄로 요약합니다. use_llm=False 시 규칙 기반 요약 사용."""
    if not use_llm:
        print("[LLM:Summary] Using rule-based summary generation.")
        return generate_one_line_summary_rule_based(content)
        
    try:
        # LLM을 사용하여 한국어로 직접 요약 생성
        korean_prompt = f"""Korean summary required. Write ONE sentence summary in Korean language only.

Article: {content[:800]}

Korean summary (one sentence, 100-200 characters):"""

        print(f"[LLM:Summary] Generating Korean summary directly...")
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a journalist. Always respond in Korean language."},
                    {"role": "user", "content": korean_prompt}
                ],
                "stream": False
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            korean_summary = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            print(f"[LLM:Summary] Generated Korean Summary: '{korean_summary}'")

            # 생성된 요약 후처리: 길이 제한 및 정리
            korean_summary = korean_summary.strip()
            
            # 영어 부분 제거 (괄호 안의 내용 제거)
            korean_summary = re.sub(r'\([^)]*\)', '', korean_summary)
            korean_summary = korean_summary.strip()
            
            # 영어 문장이 섞여있으면 첫 한글 문장만 추출
            sentences = re.split(r'[.!?]', korean_summary)
            korean_only_sentences = []
            for sent in sentences:
                # 한글이 포함된 문장만 선택
                if re.search(r'[가-힣]', sent) and not re.search(r'[a-zA-Z]{10,}', sent):
                    korean_only_sentences.append(sent.strip())
            
            if korean_only_sentences:
                korean_summary = korean_only_sentences[0] + '.'
            
            if len(korean_summary) > 300:
                korean_summary = korean_summary[:300].rsplit('.', 1)[0] + '.'
            elif len(korean_summary) < 50:  # 기준을 50자로 낮춤
                # 너무 짧으면 규칙 기반으로 대체
                print(f"[LLM:Summary] Summary too short, using rule-based fallback")
                return generate_one_line_summary_rule_based(content)

            print(f"[LLM:Summary] Final Korean Summary: '{korean_summary}' ({len(korean_summary)}자)")
            return korean_summary
        else:
            print(f"[LLM:Summary] Ollama API 호출 실패: 상태 코드 {response.status_code}")
            print(f"[LLM:Summary] 응답 내용: {response.text[:100]}...")
            return ""

    except Exception as e:
        print(f"[LLM:Summary] !!! LLM 요약 생성 중 오류 발생: {str(e)}")
        print(traceback.format_exc())
        return ""

def generate_key_content(content: str, use_llm: bool = True) -> str:
    """기사 내용에서 핵심 내용을 추출합니다. use_llm=False 시 규칙 기반 핵심 내용 사용."""
    if not use_llm:
        print("[LLM:KeyContent] Using rule-based key content generation.")
        return generate_key_content_rule_based(content)
        
    try:
        # LLM을 사용하여 한국어로 직접 핵심 내용 추출
        korean_prompt = f"""Write key points in Korean. Use bullet points.

Article: {content[:1000]}

Korean key points (3-5 points):"""

        print(f"[LLM:KeyContent] Generating Korean key points directly...")
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": "You are an analyst. Always respond in Korean language."},
                    {"role": "user", "content": korean_prompt}
                ],
                "stream": False
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            korean_key_content = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            print(f"[LLM:KeyContent] Generated Korean Key Content: '{korean_key_content[:200]}...'")
            
            # 불필요한 공백 정리 및 영어 제거
            korean_key_content = re.sub(r'\s+', ' ', korean_key_content)
            
            # 괄호 안의 영어 설명 제거
            korean_key_content = re.sub(r'\([^)]*\)', '', korean_key_content)
            
            # 영어가 너무 많이 섞여있으면 규칙 기반 사용
            english_ratio = len(re.findall(r'[a-zA-Z]', korean_key_content)) / max(len(korean_key_content), 1)
            if english_ratio > 0.3:  # 30% 이상이 영어면
                print("[LLM:KeyContent] Too much English content, using rule-based fallback")
                return generate_key_content_rule_based(content)
            
            # 잘못된 한글 수정 (예: 에너gie -> 에너지)
            korean_key_content = re.sub(r'에너gie', '에너지', korean_key_content)
            korean_key_content = re.sub(r'우성', '지원', korean_key_content)  # 우성 -> 지원
            
            korean_key_content = korean_key_content.strip()
            korean_key_content = korean_key_content[:1900] # Notion rich_text 2000자 제한 고려하여 1900자로 제한

            print(f"[LLM:KeyContent] Final Korean Key Content: '{korean_key_content[:200]}...'")
            return korean_key_content
        else:
            print(f"[LLM:KeyContent] Ollama API 호출 실패: 상태 코드 {response.status_code}")
            print(f"[LLM:KeyContent] 응답 내용: {response.text[:100]}...")
            return ""

    except Exception as e:
        print(f"[LLM:KeyContent] !!! LLM 핵심 내용 추출 중 오류 발생: {str(e)}")
        print(traceback.format_exc())
        return ""

def main():
    # 순환참조 방지를 위해 main 함수 내에서 동적으로 임포트
    from notion.notion_client import NotionClient
    from crawlers.electimes_crawler import ElectimesCrawler

    notion = NotionClient()
    crawler = ElectimesCrawler(notion)  # notion_client 인자 추가
    
    try:
        print("Chromium WebDriver initialized successfully")
        database_id = notion.get_weekly_database_id()

        if not database_id:
            print("Error: Database not found or could not be created.")
            return

        print(f"Found existing database with ID: {database_id}")

        # Notion 데이터베이스의 모든 기사 목록 가져오기
        print("Fetching all articles from Notion database...")
        notion_articles_response = notion.client.databases.query(database_id)
        notion_articles = notion_articles_response.get('results', [])
        print(f"Found {len(notion_articles)} articles in Notion database.")

        updated_count = 0
        for i, notion_article in enumerate(notion_articles):
            page_id = notion_article['id']
            notion_title_property = notion_article['properties'].get('제목', {})
            notion_title = "".join([text_item.get('plain_text', '') for text_item in notion_title_property.get('title', [])])
            
            # 바로가기 URL 가져오기
            url_property = notion_article['properties'].get('바로가기', {})
            current_url = url_property.get('url', '')
            
            if not current_url:
                print(f"Skipping article '{notion_title}' - No URL found")
                continue

            print(f"--- Processing article {i+1}/{len(notion_articles)}: ID={page_id}, Title='{notion_title}' ---")

            try:
                print(f"DEBUG: Crawling article content from URL: {current_url}")
                article_details = crawler.get_article_content(current_url)

                if article_details and article_details.get('content'):
                    # 핵심 내용 정제 및 2000자 제한 적용
                    cleaned_content = clean_article_content(article_details.get('content', ''))[:2000]
                    
                    # LLM (Ollama)을 사용하여 한줄요약 생성 시도, 실패 시 폴백
                    # 프롬프트 개선 테스트를 위해 use_llm=True로 변경
                    summary = generate_one_line_summary_with_llm(cleaned_content, use_llm=True)
                    if not summary: # LLM 및 폴백 모두 실패했을 경우 대비 (매우 드물겠지만)
                         summary = "요약 생성 실패"
                         
                    # LLM을 사용하여 핵심 내용 생성
                    # 프롬프트 개선 테스트를 위해 use_llm=True로 변경
                    key_content = generate_key_content(cleaned_content, use_llm=True)

                    # Notion DB 업데이트 속성 준비
                    properties_to_update = {
                        "바로가기": {"url": current_url},
                        "한줄요약": {"rich_text": [{"text": {"content": summary}}]},
                        "핵심 내용": {"rich_text": [{"text": {"content": key_content}}]}
                    }
                    
                    if article_details.get('keywords'):
                        # 기존 키워드 유지하고 새 키워드 추가 (중복 제거 필요)
                        existing_keywords = [k['name'] for k in notion_article['properties'].get('키워드', {}).get('multi_select', [])]
                        new_keywords = article_details.get('keywords', [])
                        combined_keywords = list(set(existing_keywords + new_keywords))
                        properties_to_update['키워드'] = {"multi_select": [{"name": k} for k in combined_keywords]}

                    print(f"DEBUG: Updating Notion page ID {page_id} with extracted content.")
                    success = notion.update_article_in_database(page_id, properties_to_update)
                    if success:
                        print(f"Successfully updated article ID: {page_id}")
                        updated_count += 1
                    else:
                        print(f"Failed to update article ID: {page_id}")
                else:
                    print(f"DEBUG: Failed to crawl article content or content is empty for URL: {current_url}")
                    # 크롤링 실패 시에도 다음 기사로 넘어가도록 처리
                    continue # 명시적으로 다음 반복으로 이동

            except Exception as e:
                # 특정 기사 처리 중 예상치 못한 오류 발생 시
                print(f"Error processing article {i+1}/{len(notion_articles)} (ID={page_id}) from URL {current_url}: {str(e)}")
                print(traceback.format_exc())
                # 오류가 발생했더라도 다음 기사 처리는 계속 진행
                continue # 명시적으로 다음 반복으로 이동

        print(f"--- Script Finished ---")
        print(f"Total articles found in Notion: {len(notion_articles)}")
        print(f"Articles successfully updated: {updated_count}")
        print(f"--- ---")

    except Exception as e:
        # 스크립트 실행 중 전체 오류 발생 시 (DB 연결 등 초기 단계 오류)
        print(f"스크립트 실행 중 전체 오류 발생: {e}")
        print(traceback.format_exc())

if __name__ == '__main__':
    main() 