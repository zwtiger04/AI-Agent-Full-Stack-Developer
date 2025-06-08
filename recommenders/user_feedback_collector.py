from typing import List, Dict, Any
from notion_client import Client

class UserFeedbackCollector:
    def __init__(self, notion_client: Client):
        self.notion = notion_client
        
    def get_interested_articles(self, database_id: str) -> List[Dict[str, Any]]:
        """관심 표시된 기사 목록 가져오기"""
        try:
            results = []
            query = self.notion.databases.query(
                database_id=database_id,
                filter={
                    "property": "관심",
                    "checkbox": {
                        "equals": True
                    }
                }
            )
            results.extend(query.get('results', []))
            
            articles = []
            for page in results:
                props = page['properties']
                articles.append({
                    'page_id': page['id'],
                    'title': self._get_text_content(props, '제목'),
                    'content': self._get_text_content(props, '핵심 내용'),
                    'summary': self._get_text_content(props, '한줄요약'),
                    'keywords': [k['name'] for k in props.get('키워드', {}).get('multi_select', [])]
                })
            return articles
        except Exception as e:
            print(f"관심 기사 수집 실패: {e}")
            return []
            
    def _get_text_content(self, props: Dict, key: str) -> str:
        """Notion 속성에서 텍스트 내용 추출"""
        arr = props.get(key, {}).get('title' if key == '제목' else 'rich_text', [])
        return arr[0].get('plain_text', '') if arr and 'plain_text' in arr[0] else '' 