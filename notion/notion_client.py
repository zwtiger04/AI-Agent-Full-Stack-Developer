from typing import Dict, Any, List
from datetime import datetime
from notion_client import Client
from config.config import NOTION_API_KEY, NOTION_DATABASE_ID, NOTION_PARENT_PAGE_ID # NOTION_DATABASE_ID는 이제 사용하지 않을 수 있으며, NOTION_PARENT_PAGE_ID를 추가합니다.
import pandas as pd
import re
from ai_update_content import generate_one_line_summary_with_llm, generate_key_content, clean_article_content

class NotionClient:
    def __init__(self):
        self.client = Client(auth=NOTION_API_KEY)
        self.databases = {}  # 데이터베이스 ID 캐시
        # self.database_id = NOTION_DATABASE_ID # 환경 변수 대신 동적으로 설정
        # self.database_id = None # 초기에는 데이터베이스 ID를 None으로 설정

    def _search_database(self, title: str) -> List[Dict]:
        """
        데이터베이스를 제목으로 검색합니다.
        
        Args:
            title (str): 검색할 데이터베이스 제목
            
        Returns:
            List[Dict]: 검색된 데이터베이스 목록
        """
        try:
            search_response = self.client.search(
                query=title,
                filter={
                    "property": "object",
                    "value": "database"
                }
            )
            
            results = []
            for result in search_response.get('results', []):
                db_title = "".join([text_item['plain_text'] for text_item in result['title']])
                if db_title == title:
                    results.append({
                        'id': result['id'],
                        'title': db_title
                    })
                    print(f"[Notion] 데이터베이스 찾음: {db_title} (ID: {result['id']})")
            
            return results
            
        except Exception as e:
            print(f"[Notion] 데이터베이스 검색 중 오류 발생: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return []

    def get_weekly_database_id(self, parent_page_id: str = NOTION_PARENT_PAGE_ID) -> str | None:
        """Get or create the database ID for the current week."""
        try:
            # 현재 연도와 주차 계산
            now = datetime.now()
            current_year = now.year
            current_week = now.isocalendar()[1]
            database_title = f"전력 산업 뉴스 {current_year}년 {current_week}주차"
            
            # 데이터베이스 검색
            results = self._search_database(database_title)
            if results:
                found_database_id = results[0]['id']
                self.databases[database_title] = found_database_id
                return found_database_id
                
            # 데이터베이스가 없으면 생성
            return self._create_weekly_database(database_title, parent_page_id)
            
        except Exception as e:
            print(f"[Notion] 주간 데이터베이스 ID 조회 중 오류 발생: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return None

    def _create_weekly_database(self, database_title: str, parent_page_id: str) -> str:
        """
        주간 데이터베이스를 생성합니다.
        
        Args:
            database_title (str): 생성할 데이터베이스 제목
            parent_page_id (str): 부모 페이지 ID
            
        Returns:
            str: 생성된 데이터베이스 ID
        """
        if not parent_page_id:
            raise ValueError("parent_page_id is not set")
        
        print(f"[Notion] 데이터베이스 '{database_title}' 생성 중... (부모 페이지: {parent_page_id})")
        
        # Create a new database under the specified parent page
        new_database = self.client.databases.create(
            parent={
                "type": "page_id",
                "page_id": parent_page_id
            },
            title=[
                {
                    "type": "text",
                    "text": {
                        "content": database_title
                    }
                }
            ],
            properties={
                "제목": {"title": {}},
                "출처": {"rich_text": {}},
                "날짜": {"date": {}},
                "키워드": {"multi_select": {}},
                "한줄요약": {"rich_text": {}},
                "핵심 내용": {"rich_text": {}},
                "바로가기": {"url": {}},
                "관심": {"checkbox": {}},
                "AI추천": {"checkbox": {}}
            }
        )
        
        created_database_id = new_database['id']
        print(f"[Notion] 데이터베이스 생성 완료 (ID: {created_database_id})")
        self.databases[database_title] = created_database_id
        return created_database_id

    def create_news_card(self, article: Dict[str, Any], database_id: str) -> Dict[str, Any]:
        """Create a news card in Notion (database_id를 인자로 받음)"""
        if not database_id:
            print("Database ID is not set. Cannot create news card.")
            return None

        # published_date 처리
        published_date = article.get('published_date', datetime.now())
        if hasattr(published_date, 'strftime'):
            published_date_str = published_date.strftime('%Y-%m-%d')
            published_date_iso = published_date.isoformat()
        else:
            published_date_str = str(published_date)
            published_date_iso = str(published_date)

        # 본문 정제
        cleaned_content = clean_article_content(article['content'])
        # 한줄요약 및 핵심 내용 생성
        summary = generate_one_line_summary_with_llm(cleaned_content)
        key_points = generate_key_content(cleaned_content)

        content = f"""
# {article['title']}

## 한줄 요약
{summary}

## 핵심 내용
{key_points}

## 주요 키워드
{', '.join(article.get('keywords', []))}

## 출처
- 미디어: {article.get('source', '')}
- 날짜: {published_date_str}
- 링크: {article.get('url', '')}
        """

        new_page = {
            "parent": {"database_id": database_id},
            "properties": {
                "제목": {
                    "title": [
                        {"text": {"content": article.get('title', '')}}
                    ]
                },
                "출처": {
                    "rich_text": [
                        {"text": {"content": article.get('source', '')}}
                    ]
                },
                "날짜": {
                    "date": {"start": published_date_iso}
                },
                "키워드": {
                    "multi_select": [
                        {"name": keyword} for keyword in article.get('keywords', [])
                    ]
                },
                "한줄요약": {
                    "rich_text": [
                        {"text": {"content": summary}}
                    ]
                },
                "핵심 내용": {
                    "rich_text": [
                        {"text": {"content": key_points}}
                    ]
                },
                "바로가기": {
                    "url": article.get('url', '')
                },
                "관심": {
                    "checkbox": False
                },
                "AI추천": {
                    "checkbox": article.get('ai_recommend', False)  # AI 추천 상태 반영
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"type": "text", "text": {"content": f"[기사 원문 바로가기]({article.get('url', '')})"}}
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"type": "text", "text": {"content": f"한줄 요약: {summary}"}}
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"type": "text", "text": {"content": content}}
                        ]
                    }
                }
            ]
        }

        return self.client.pages.create(**new_page)

    def sync_articles(self, articles: List[Dict[str, Any]], database_id: str) -> List[Dict[str, Any]]:
        """Sync articles to Notion (update if exists, create if not)"""
        synced_articles = []
        
        # Ensure database_id is set before syncing
        if not database_id:
             print("Database ID is not provided. Cannot sync articles.")
             return []
             
        for article in articles:
            try:
                # 본문 정제
                cleaned_content = clean_article_content(article['content'])
                # 한줄요약 및 핵심 내용 생성 (LLM 사용)
                summary = generate_one_line_summary_with_llm(cleaned_content, use_llm=True)
                key_points = generate_key_content(cleaned_content, use_llm=True)

                # Ensure content is within Notion's limits (2000 characters)
                summary = summary[:2000] if summary else ""
                key_points = key_points[:2000] if key_points else ""

                # 기존 페이지 존재 여부 확인 (URL 기준)
                article_url = article.get('url', '')
                print(f"[Notion:sync] Searching for existing page with URL: {article_url}")
                try:
                    existing_pages = self.client.databases.query(
                        database_id=database_id,
                        filter={
                            "property": "바로가기",
                            "url": {"equals": article_url}
                        }
                    )
                    if existing_pages.get('results'):
                        page_id = existing_pages['results'][0]['id']
                        print(f"[Notion:sync] Found existing page for '{article.get('title', '')}' (ID: {page_id})")
                        
                        # 기존 페이지의 현재 상태 가져오기
                        current_page = self.client.pages.retrieve(page_id=page_id)
                        current_properties = current_page.get('properties', {})
                        
                        # 업데이트할 속성 준비
                        properties_to_update = {}
                        
                        # 1. 출처 업데이트 (새로운 출처가 있고, 기존 출처와 다른 경우)
                        new_source = article.get('source', '')
                        current_source = ''.join([text.get('plain_text', '') for text in current_properties.get('출처', {}).get('rich_text', [])])
                        if new_source and new_source != current_source:
                            properties_to_update['출처'] = {"rich_text": [{"text": {"content": new_source}}]}
                            print(f"[Notion:sync] 출처 업데이트: {current_source} -> {new_source}")
                        
                        # 2. 한줄요약 업데이트 (새로운 요약이 있고, 기존 요약과 다른 경우)
                        current_summary = ''.join([text.get('plain_text', '') for text in current_properties.get('한줄요약', {}).get('rich_text', [])])
                        if summary and summary != current_summary:
                            properties_to_update['한줄요약'] = {"rich_text": [{"text": {"content": summary}}]}
                            print(f"[Notion:sync] 한줄요약 업데이트: {current_summary[:50]}... -> {summary[:50]}...")
                        
                        # 3. 핵심 내용 업데이트 (새로운 내용이 있고, 기존 내용과 다른 경우)
                        current_key_points = ''.join([text.get('plain_text', '') for text in current_properties.get('핵심 내용', {}).get('rich_text', [])])
                        if key_points and key_points != current_key_points:
                            properties_to_update['핵심 내용'] = {"rich_text": [{"text": {"content": key_points}}]}
                            print(f"[Notion:sync] 핵심 내용 업데이트: {current_key_points[:50]}... -> {key_points[:50]}...")
                        
                        # 4. 키워드 업데이트 (새로운 키워드가 있는 경우)
                        new_keywords = article.get('keywords', [])
                        current_keywords = [k['name'] for k in current_properties.get('키워드', {}).get('multi_select', [])]
                        if new_keywords and set(new_keywords) != set(current_keywords):
                            properties_to_update['키워드'] = {"multi_select": [{"name": k} for k in new_keywords]}
                            print(f"[Notion:sync] 키워드 업데이트: {current_keywords} -> {new_keywords}")
                        
                        # 업데이트할 속성이 있는 경우에만 업데이트 실행
                        if properties_to_update:
                            print(f"[Notion:sync] 기존 기사 업데이트 시도: {article.get('title', '')} (Page ID: {page_id})")
                            try:
                                self.client.pages.update(
                                    page_id=page_id,
                                    properties=properties_to_update
                                )
                                print(f"[Notion:sync] 기존 기사 업데이트 성공: {article.get('title', '')} (Page ID: {page_id})")
                                synced_articles.append({'id': page_id, 'title': article.get('title', '')})
                            except Exception as e:
                                print(f"[Notion:sync] !!! Error updating page {page_id} for article '{article.get('title', '')}': {e}")
                                import traceback
                                print(traceback.format_exc())
                        else:
                            print(f"[Notion:sync] 업데이트할 내용이 없음: {article.get('title', '')}")
                            synced_articles.append({'id': page_id, 'title': article.get('title', '')})
                    else:
                        # 없으면 새로 생성
                        print(f"[Notion:sync] 새 기사 생성 시도: {article.get('title', '')}")
                        new_page = {
                            "parent": {"database_id": database_id},
                            "properties": {
                                "제목": {
                                    "title": [
                                        {"text": {"content": article.get('title', '')}}
                                    ]
                                },
                                "출처": {
                                    "rich_text": [
                                        {"text": {"content": article.get('source', '')}}
                                    ]
                                },
                                "날짜": {
                                    "date": {"start": article.get('published_date', datetime.now()).isoformat()}
                                },
                                "키워드": {
                                    "multi_select": [
                                        {"name": keyword} for keyword in article.get('keywords', [])
                                    ]
                                },
                                "한줄요약": {
                                    "rich_text": [
                                        {"text": {"content": summary}}
                                    ]
                                },
                                "핵심 내용": {
                                    "rich_text": [
                                        {"text": {"content": key_points}}
                                    ]
                                },
                                "바로가기": {
                                    "url": article.get('url', '')
                                },
                                "관심": {
                                    "checkbox": False
                                },
                                "AI추천": {
                                    "checkbox": article.get('ai_recommend', False)
                                }
                            }
                        }
                        print(f"[Notion:sync] Attempting to create new page with properties: {new_page}")
                        try:
                            notion_page = self.client.pages.create(**new_page)
                            if notion_page:
                                print(f"[Notion:sync] 새 기사 생성 성공: {article.get('title', '')} (Page ID: {notion_page['id']})")
                                synced_articles.append(notion_page)
                            else:
                                 print(f"[Notion:sync] 새 기사 생성 실패: {article.get('title', '')} - Notion API에서 응답 없음")
                        except Exception as e:
                            print(f"[Notion:sync] !!! Error creating new page for article '{article.get('title', '')}': {e}")
                            import traceback
                            print(traceback.format_exc())
                except Exception as e:
                    print(f"[Notion:sync] !!! Outer error syncing article '{article.get('title', article.get('url', 'Unknown Article'))}': {e}")
                    import traceback
                    print(traceback.format_exc())
                
            except Exception as e:
                print(f"[Notion] !!! Outer error syncing article '{article.get('title', article.get('url', 'Unknown Article'))}': {e}")
                import traceback
                print(traceback.format_exc())
                
        return synced_articles

    def export_feedback_to_csv(self, database_id: str, csv_path: str = 'feedback/feedback.csv', limit: int = 1000) -> None:
        """Notion DB에서 기사 정보와 관심 컬럼을 읽어와 CSV로 저장 (핵심 내용 포함)"""
        try:
            results = []
            query = self.client.databases.query(database_id=database_id, page_size=100)
            results.extend(query.get('results', []))
            # 페이징 처리 (최대 limit까지)
            while query.get('has_more') and len(results) < limit:
                query = self.client.databases.query(
                    database_id=database_id,
                    start_cursor=query['next_cursor'],
                    page_size=100
                )
                results.extend(query.get('results', []))
            rows = []
            for page in results:
                props = page['properties']
                def safe_get_text(prop, key):
                    arr = prop.get(key, {}).get('title' if key == '제목' else 'rich_text', [])
                    return arr[0].get('plain_text', '') if arr and 'plain_text' in arr[0] else ''
                rows.append({
                    'title': safe_get_text(props, '제목'),
                    'url': props.get('바로가기', {}).get('url', ''),
                    'summary': safe_get_text(props, '한줄요약'),
                    'content': safe_get_text(props, '핵심 내용'),
                    'interest': props.get('관심', {}).get('checkbox', False),
                    'ai_recommend': props.get('AI추천', {}).get('checkbox', False)
                })
            df = pd.DataFrame(rows)
            import os
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            df.to_csv(csv_path, index=False)
            print(f"피드백 데이터 {csv_path}로 저장 완료. 총 {len(df)}건.")
        except Exception as e:
            print(f"피드백 데이터 저장 실패: {e}")

    def export_interested_articles_to_csv(self, database_id: str, csv_path: str = 'feedback/interested_articles.csv', limit: int = 1000) -> None:
        """Notion DB에서 '관심' 컬럼이 체크된 기사만 필터링하여 CSV로 저장"""
        try:
            results = []
            query = self.client.databases.query(
                database_id=database_id,
                filter={
                    "property": "관심",
                    "checkbox": {
                        "equals": True
                    }
                },
                page_size=100
            )
            results.extend(query.get('results', []))
            # 페이징 처리 (최대 limit까지)
            while query.get('has_more') and len(results) < limit:
                query = self.client.databases.query(
                    database_id=database_id,
                    filter={
                        "property": "관심",
                        "checkbox": {
                            "equals": True
                        }
                    },
                    start_cursor=query['next_cursor'],
                    page_size=100
                )
                results.extend(query.get('results', []))
            rows = []
            for page in results:
                props = page['properties']
                def safe_get_text(prop, key):
                    arr = prop.get(key, {}).get('title' if key == '제목' else 'rich_text', [])
                    return arr[0].get('plain_text', '') if arr and 'plain_text' in arr[0] else ''
                rows.append({
                    'title': safe_get_text(props, '제목'),
                    'url': props.get('바로가기', {}).get('url', ''),
                    'summary': safe_get_text(props, '한줄요약'),
                    'interest': props.get('관심', {}).get('checkbox', False),
                    'ai_recommend': props.get('AI추천', {}).get('checkbox', False)
                })
            df = pd.DataFrame(rows)
            import os
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            df.to_csv(csv_path, index=False)
            print(f"관심 기사 데이터 {csv_path}로 저장 완료. 총 {len(df)}건.")
        except Exception as e:
            print(f"관심 기사 데이터 저장 실패: {e}") 

    def update_ai_recommendation(self, page_id: str, ai_recommend: bool) -> None:
        """Notion DB의 특정 기사에 대해 AI 추천 결과를 업데이트합니다.
        
        Args:
            page_id (str): Notion 페이지 ID
            ai_recommend (bool): AI 추천 여부 (True/False)
        """
        try:
            self.client.pages.update(
                page_id=page_id,
                properties={
                    "AI추천": {
                        "checkbox": ai_recommend
                    }
                }
            )
            print(f"AI 추천 결과 업데이트 완료: {page_id}, 추천 여부: {ai_recommend}")
        except Exception as e:
            print(f"AI 추천 결과 업데이트 실패: {e}") 

    def update_article_content(self, page_id: str, content: str) -> None:
        """Notion DB의 특정 기사에 대해 '핵심 내용' 컬럼을 업데이트합니다."""
        try:
            self.client.pages.update(
                page_id=page_id,
                properties={
                    "핵심 내용": {
                        "rich_text": [
                            {"text": {"content": content[:2000]}}  # Notion API 제한 고려
                        ]
                    }
                }
            )
            print(f"핵심 내용 업데이트 완료: {page_id}")
        except Exception as e:
            print(f"핵심 내용 업데이트 실패: {e}") 

    def update_article_url(self, page_id: str, url: str) -> None:
        """Update article URL in Notion"""
        self.client.pages.update(
            page_id=page_id,
            properties={
                "바로가기": {"url": url}
            }
        )

    def update_article_in_database(self, page_id: str, properties: Dict[str, Any]) -> bool:
        """Update article properties in Notion database"""
        try:
            print(f"Updating page {page_id} with properties: {properties}")
            self.client.pages.update(
                page_id=page_id,
                properties=properties
            )
            print(f"Successfully updated page {page_id}")
            return True
        except Exception as e:
            print(f"Error updating article in database: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return False

    def get_page_blocks(self, page_id: str) -> List[Dict[str, Any]]:
        """Get all blocks for a given Notion page."""
        blocks = []
        next_cursor = None
        while True:
            response = self.client.blocks.children.list(
                block_id=page_id,
                page_size=100,
                start_cursor=next_cursor
            )
            blocks.extend(response.get('results', []))
            if not response.get('has_more'):
                break
            next_cursor = response.get('next_cursor')
        return blocks

    def extract_link_from_blocks(self, blocks: List[Dict[str, Any]]) -> str | None:
        """Extract a potential article link from a list of Notion blocks.
        Looks for URL in paragraphs or bookmark blocks.
        """
        for block in blocks:
            block_type = block.get('type')
            if block_type == 'paragraph':
                rich_text = block.get('paragraph', {}).get('rich_text', [])
                for text_obj in rich_text:
                    if text_obj.get('type') == 'text' and text_obj.get('href'):
                        # Check if text object itself is a link
                        print(f"DEBUG: Found text with href: {text_obj['href']}")
                        return text_obj['href']
                    if text_obj.get('type') == 'text' and text_obj.get('text', {}).get('content'):
                         # Look for URL patterns in plain text
                         content = text_obj['text']['content']
                         url_match = re.search(r'https?://[\w.-]+\S+', content)
                         if url_match:
                             print(f"DEBUG: Found URL pattern in paragraph text: {url_match.group(0)}")
                             return url_match.group(0)
            elif block_type == 'bookmark':
                bookmark_url = block.get('bookmark', {}).get('url')
                if bookmark_url:
                    print(f"DEBUG: Found bookmark URL: {bookmark_url}")
                    return bookmark_url
            # Add other block types if needed (e.g., code, heading, etc.)

        print("DEBUG: No potential article link found in blocks.")
        return None 

    def get_all_weekly_databases(self) -> List[str]:
        """모든 주차의 데이터베이스 ID를 가져옵니다."""
        try:
            # 현재 연도와 주차 계산
            now = datetime.now()
            current_year = now.year
            current_week = now.isocalendar()[1]
            
            # 최근 4주치 데이터베이스 검색
            databases = []
            for week_offset in range(4):
                target_week = current_week - week_offset
                if target_week <= 0:
                    target_week += 52
                    target_year = current_year - 1
                else:
                    target_year = current_year
                    
                database_title = f"전력 산업 뉴스 {target_year}년 {target_week}주차"
                
                # 데이터베이스 검색
                results = self._search_database(database_title)
                databases.extend(result['id'] for result in results)
            
            return databases
            
        except Exception as e:
            print(f"[Notion] 데이터베이스 목록 조회 중 오류 발생: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return []

    def get_interested_articles(self, database_id: str = None) -> List[Dict[str, Any]]:
        """관심 표시된 기사들을 가져옵니다. database_id가 None이면 모든 주차에서 가져옵니다."""
        try:
            interested_articles = []
            
            if database_id:
                # 특정 데이터베이스에서만 가져오기
                databases = [database_id]
            else:
                # 모든 주차의 데이터베이스에서 가져오기
                databases = self.get_all_weekly_databases()
            
            for db_id in databases:
                # 관심 표시된 기사만 필터링
                query = self.client.databases.query(
                    database_id=db_id,
                    filter={
                        "property": "관심",
                        "checkbox": {
                            "equals": True
                        }
                    },
                    page_size=100
                )
                
                results = query.get('results', [])
                while query.get('has_more'):
                    query = self.client.databases.query(
                        database_id=db_id,
                        filter={
                            "property": "관심",
                            "checkbox": {
                                "equals": True
                            }
                        },
                        start_cursor=query['next_cursor'],
                        page_size=100
                    )
                    results.extend(query.get('results', []))
                
                # 기사 정보 추출
                for page in results:
                    props = page['properties']
                    def safe_get_text(prop, key):
                        arr = prop.get(key, {}).get('title' if key == '제목' else 'rich_text', [])
                        return arr[0].get('plain_text', '') if arr and 'plain_text' in arr[0] else ''
                    
                    article = {
                        'page_id': page['id'],
                        'title': safe_get_text(props, '제목'),
                        'url': props.get('바로가기', {}).get('url', ''),
                        'summary': safe_get_text(props, '한줄요약'),
                        'content': safe_get_text(props, '핵심 내용'),
                        'keywords': [opt['name'] for opt in props.get('키워드', {}).get('multi_select', [])],
                        'interest': props.get('관심', {}).get('checkbox', False),
                        'ai_recommend': props.get('AI추천', {}).get('checkbox', False)
                    }
                    interested_articles.append(article)
            
            print(f"[Notion] 총 {len(interested_articles)}개의 관심 기사를 찾았습니다.")
            return interested_articles
            
        except Exception as e:
            print(f"[Notion] 관심 기사 조회 중 오류 발생: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return [] 

    def get_all_articles_from_database(self, database_id: str) -> List[Dict[str, Any]]:
        """특정 데이터베이스의 모든 기사 (페이지) 정보를 가져옵니다."""
        try:
            all_articles = []
            
            # 데이터베이스의 모든 페이지 조회 (페이징 처리 포함)
            query = self.client.databases.query(
                database_id=database_id,
                page_size=100
            )
            
            results = query.get('results', [])
            all_articles.extend(results)
            
            while query.get('has_more'):
                query = self.client.databases.query(
                    database_id=database_id,
                    start_cursor=query['next_cursor'],
                    page_size=100
                )
                results = query.get('results', [])
                all_articles.extend(results)
                
            # 필요한 기사 정보 추출
            extracted_articles = []
            for page in all_articles:
                props = page['properties']
                def safe_get_text(prop, key):
                    arr = prop.get(key, {}).get('title' if key == '제목' else 'rich_text', [])
                    return arr[0].get('plain_text', '') if arr and 'plain_text' in arr[0] else ''
                    
                extracted_articles.append({
                    'page_id': page['id'],
                    'title': safe_get_text(props, '제목'),
                    'url': props.get('바로가기', {}).get('url', ''),
                    'summary': safe_get_text(props, '한줄요약'),
                    'source': safe_get_text(props, '출처'),
                    'key_points': safe_get_text(props, '핵심 내용'),
                    'keywords': [opt['name'] for opt in props.get('키워드', {}).get('multi_select', [])],
                    'interest': props.get('관심', {}).get('checkbox', False),
                    'ai_recommend': props.get('AI추천', {}).get('checkbox', False)
                })
            
            return extracted_articles
            
        except Exception as e:
            print(f"Error getting all articles from database: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return []

    def get_articles_with_empty_fields_from_db(self, database_id: str) -> List[Dict[str, Any]]:
        """특정 데이터베이스에서 한줄요약, 출처, 핵심 내용 중 하나라도 빈 필드가 있는 기사를 찾습니다."""
        try:
            all_articles = self.get_all_articles_from_database(database_id)
            articles_with_empty_fields = []
            
            for article in all_articles:
                empty_fields = {
                    'summary': not article.get('summary', '').strip(),
                    'source': not article.get('source', '').strip(),
                    'key_points': not article.get('key_points', '').strip()
                }
                
                if any(empty_fields.values()):
                    article['empty_fields'] = empty_fields
                    articles_with_empty_fields.append(article)
                    print(f"Found article with empty fields: {article['title']}")
                    print(f"Empty fields: {[k for k, v in empty_fields.items() if v]}")
                    
            return articles_with_empty_fields
            
        except Exception as e:
            print(f"Error getting articles with empty fields: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return [] 

    def get_all_articles_from_db(self, database_id: str) -> List[Dict]:
        """특정 데이터베이스의 모든 기사를 가져옵니다.
        
        Args:
            database_id: Notion 데이터베이스 ID
            
        Returns:
            List[Dict]: 기사 정보 리스트
        """
        try:
            articles = []
            query = self.client.databases.query(database_id=database_id, page_size=100)
            articles.extend(query.get('results', []))
            
            while query.get('has_more'):
                query = self.client.databases.query(
                    database_id=database_id,
                    start_cursor=query['next_cursor'],
                    page_size=100
                )
                articles.extend(query.get('results', []))
            
            # 기사 정보 추출
            processed_articles = []
            for page in articles:
                props = page['properties']
                def safe_get_text(prop, key):
                    arr = prop.get(key, {}).get('title' if key == '제목' else 'rich_text', [])
                    return arr[0].get('plain_text', '') if arr and 'plain_text' in arr[0] else ''
                
                processed_articles.append({
                    'page_id': page['id'],
                    'title': safe_get_text(props, '제목'),
                    'url': props.get('바로가기', {}).get('url', ''),
                    'source': safe_get_text(props, '출처'),
                    'summary': safe_get_text(props, '한줄요약'),
                    'key_points': safe_get_text(props, '핵심 내용')
                })
            
            return processed_articles
            
        except Exception as e:
            print(f"데이터베이스에서 기사 목록을 가져오는 중 오류 발생: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return [] 