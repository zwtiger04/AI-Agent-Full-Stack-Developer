from typing import List, Dict, Any
import re
from collections import Counter
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer

class KeywordProcessor:
    def __init__(self):
        self.okt = Okt()
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            tokenizer=self._tokenize,
            stop_words=self._get_stop_words()
        )
        
    def _tokenize(self, text: str) -> List[str]:
        """텍스트를 토큰화하고 명사만 추출"""
        # 특수문자 제거
        text = re.sub(r'[^\w\s]', ' ', text)
        # 명사 추출
        nouns = self.okt.nouns(text)
        # 2글자 이상인 명사만 선택
        return [noun for noun in nouns if len(noun) >= 2]
    
    def _get_stop_words(self) -> List[str]:
        """불용어 목록 반환"""
        return [
            # 언론/미디어 관련
            '기자', '뉴스', '보도', '연합', '매일', '경제',
            
            # 전력/에너지 관련
            '전력', '전기', '발전', '송전', '배전', '원자력', '신재생', '에너지',
            
            # 시간 관련
            '올해', '내년', '작년', '당시', '현재', '최근', '지난', '앞으로',
            
            # 조직/기관 관련
            '기관', '단체', '회사', '기업', '정부', '부처', '부서', '팀',
            '조직', '위원회', '협회', '연맹', '연합', '기구',
            
            # 산업/시장 관련
            '시장', '산업', '분야', '영역', '부문', '부분', '측면',
            
            # 정책/계획 관련
            '방안', '대책', '정책', '계획', '전략', '방향', '목표',
            
            # 문제/이슈 관련
            '문제', '이슈', '쟁점', '논란', '갈등', '해결', '개선',
            
            # 발전/성장 관련
            '발전', '성장', '확대', '증가', '향상', '강화',
            
            # 실행/추진 관련
            '추진', '실행', '이행', '시행', '적용', '활용', '운용',
            
            # 검토/분석 관련
            '확인', '검토', '검증', '평가', '분석', '조사', '연구'
        ]
    
    def extract_keywords(self, content: str, top_n: int = 10) -> List[str]:
        """본문에서 키워드 추출"""
        if not content:
            return []
            
        # TF-IDF 기반 키워드 추출
        tfidf_matrix = self.vectorizer.fit_transform([content])
        feature_names = self.vectorizer.get_feature_names_out()
        
        # TF-IDF 점수가 높은 순으로 정렬
        scores = tfidf_matrix.toarray()[0]
        keyword_scores = list(zip(feature_names, scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 상위 N개 키워드 반환 (점수가 0.1 이상인 키워드만)
        return [keyword for keyword, score in keyword_scores[:top_n] if score >= 0.1]
    
    def analyze_content_patterns(self, content: str) -> Dict[str, Any]:
        """본문의 패턴 분석"""
        if not content:
            return {}
            
        # 문장 분리
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # 문장 길이 분석
        sentence_lengths = [len(s) for s in sentences]
        
        # 키워드 빈도 분석
        words = self._tokenize(content)
        word_freq = Counter(words)
        
        return {
            'sentence_count': len(sentences),
            'avg_sentence_length': sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0,
            'max_sentence_length': max(sentence_lengths) if sentence_lengths else 0,
            'min_sentence_length': min(sentence_lengths) if sentence_lengths else 0,
            'top_keywords': dict(word_freq.most_common(10))
        } 