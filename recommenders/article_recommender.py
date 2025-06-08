from typing import List, Dict, Any, Optional
from recommenders.user_feedback_collector import UserFeedbackCollector

class ArticleRecommender:
    def __init__(self, notion_client):
        self.notion = notion_client
        self.feedback_collector = UserFeedbackCollector(notion_client)
        self.patterns = {
            'keywords': set(),
            'content_patterns': [],
            'title_patterns': []
        }
        
    def analyze_article_patterns(self, interested_articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """관심 표시된 기사들의 패턴 분석"""
        self.patterns = {
            'keywords': set(),
            'content_patterns': [],
            'title_patterns': []
        }
        
        for article in interested_articles:
            # 키워드 수집
            self.patterns['keywords'].update(article['keywords'])
            
            # 제목 패턴 분석
            title_pattern = self._analyze_title_pattern(article['title'])
            if title_pattern:
                self.patterns['title_patterns'].append(title_pattern)
            
            # 본문 패턴 분석
            content_pattern = self._analyze_content_pattern(article['content'])
            if content_pattern:
                self.patterns['content_patterns'].append(content_pattern)
                
        return self.patterns
    
    def predict_interest(self, article: Dict[str, Any], patterns: Optional[Dict[str, Any]] = None) -> bool:
        """기사의 관심도를 예측합니다."""
        try:
            if not patterns:
                return False
                
            # 키워드와 토픽 매칭 점수 계산
            keyword_matches = sum(1 for keyword in patterns.get('keywords', []) 
                                if keyword in article.get('content', ''))
            topic_matches = sum(1 for topic in patterns.get('topics', []) 
                              if topic in article.get('content', ''))
            
            # 총점 계산 (키워드 1점, 토픽 2점)
            total_score = keyword_matches + (topic_matches * 2)
            
            # 상세 분석 결과 출력
            print(f"[AI 추천] 분석 결과:")
            print(f"- 키워드 매칭: {keyword_matches}개")
            print(f"- 토픽 매칭: {topic_matches}개")
            print(f"- 총점: {total_score}점")
            
            # 2점 이상이면 관심 기사로 판단
            is_interesting = total_score >= 2
            print(f"- 관심 기사 여부: {'예' if is_interesting else '아니오'}")
            
            return is_interesting
            
        except Exception as e:
            print(f"[AI 추천] 오류 발생: {str(e)}")
            return False
    
    def _analyze_title_pattern(self, title: str) -> Dict[str, Any]:
        """제목 패턴 분석"""
        return {
            'length': len(title),
            'has_numbers': any(c.isdigit() for c in title),
            'has_special_chars': any(not c.isalnum() for c in title),
            'word_count': len(title.split())
        }
    
    def _analyze_content_pattern(self, content: str) -> Dict[str, Any]:
        """본문 패턴 분석"""
        if not content:
            return {
                'length': 0,
                'paragraph_count': 0,
                'avg_paragraph_length': 0
            }
            
        paragraphs = [p for p in content.split('\n') if p.strip()]
        if not paragraphs:
            return {
                'length': len(content),
                'paragraph_count': 0,
                'avg_paragraph_length': 0
            }
            
        return {
            'length': len(content),
            'paragraph_count': len(paragraphs),
            'avg_paragraph_length': len(content) / len(paragraphs)
        }
    
    def _is_pattern_match(self, pattern1: Dict[str, Any], pattern2: Dict[str, Any]) -> bool:
        """두 패턴이 유사한지 비교"""
        if pattern1.keys() != pattern2.keys():
            return False
            
        for key in pattern1:
            if isinstance(pattern1[key], (int, float)):
                # 숫자 값은 20% 이내 차이면 유사하다고 판단
                if abs(pattern1[key] - pattern2[key]) / max(pattern1[key], pattern2[key]) > 0.2:
                    return False
            else:
                # 다른 타입은 정확히 일치해야 함
                if pattern1[key] != pattern2[key]:
                    return False
        return True 