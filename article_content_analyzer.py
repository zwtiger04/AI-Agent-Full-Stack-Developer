#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📰 개별 기사 심층 분석기
- 기사 내용을 대주제와 소주제로 구조화
- 핵심 정보 추출 및 정리
"""

import re
from typing import Dict, List, Any
from collections import Counter

class ArticleContentAnalyzer:
    """개별 기사를 심층 분석하는 클래스"""
    
    def __init__(self):
        """초기화"""
        self.section_keywords = {
            '배경': ['배경', '현황', '상황', '문제', '이슈'],
            '핵심내용': ['발표', '개발', '도입', '추진', '시행', '계획'],
            '효과': ['효과', '기대', '전망', '예상', '목표', '성과'],
            '세부사항': ['구체적', '세부', '내용', '방안', '계획'],
            '의미': ['의미', '중요', '의의', '가치', '영향']
        }
        
    def analyze_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """개별 기사를 심층 분석"""
        
        # 기본 정보
        title = article.get('title', '')
        summary = article.get('summary', '')
        key_points = article.get('key_points', '')
        content = f"{title} {summary} {key_points}"
        
        # 분석 수행
        analysis = {
            'original': article,
            'main_theme': self._extract_main_theme(title, summary),
            'sub_themes': self._extract_sub_themes(content),
            'key_facts': self._extract_key_facts(key_points),
            'structure': self._analyze_structure(content),
            'entities': self._extract_entities(content),
            'numbers': self._extract_numbers(content)
        }
        
        return analysis
    
    def _extract_main_theme(self, title: str, summary: str) -> Dict[str, str]:
        """대주제 추출"""
        
        # 제목에서 핵심 동사/명사 추출
        main_action = ''
        main_subject = ''
        
        # 동사 패턴
        action_patterns = [
            r'(\w+) 발표', r'(\w+) 추진', r'(\w+) 도입', 
            r'(\w+) 개발', r'(\w+) 구축', r'(\w+) 시행',
            r'(\w+) 강화', r'(\w+) 확대', r'(\w+) 개선'
        ]
        
        for pattern in action_patterns:
            match = re.search(pattern, title)
            if match:
                main_action = match.group(0)
                break
                
        # 주체 추출 (기관, 기업명)
        entities = re.findall(r'([가-힣]+(?:전력|에너지|기술|산업|공사|청|부|원|단))', title)
        if entities:
            main_subject = entities[0]
            
        # 대주제 구성
        if main_action and main_subject:
            theme = f"{main_subject}의 {main_action}"
        elif main_action:
            theme = main_action
        else:
            # 제목의 첫 구절을 대주제로
            theme = title.split(',')[0].split('...')[0]
            
        return {
            'theme': theme,
            'category': self._categorize_theme(title),
            'focus': self._identify_focus(title, summary)
        }
    
    def _extract_sub_themes(self, content: str) -> List[Dict[str, str]]:
        """소주제 추출 (3-4개)"""
        
        sub_themes = []
        
        # 1. 문장을 분석해서 주요 포인트 추출
        sentences = re.split(r'[.!?]\s*', content)
        
        # 중요 문장 패턴
        important_patterns = [
            r'첫째|둘째|셋째',
            r'먼저|다음으로|마지막으로',
            r'특히|주목할|핵심은',
            r'목표|계획|예정',
            r'효과|결과|성과',
            r'\d+%|\d+억|\d+MW'  # 숫자가 포함된 문장
        ]
        
        important_sentences = []
        for sentence in sentences:
            for pattern in important_patterns:
                if re.search(pattern, sentence):
                    important_sentences.append(sentence.strip())
                    break
                    
        # 2. 중요 문장을 소주제로 변환
        for i, sentence in enumerate(important_sentences[:4]):  # 최대 4개
            # 문장을 간결하게 요약
            if len(sentence) > 50:
                # 핵심 구문만 추출
                key_phrase = self._extract_key_phrase(sentence)
            else:
                key_phrase = sentence
                
            sub_theme = {
                'order': i + 1,
                'title': self._create_sub_theme_title(key_phrase),
                'content': key_phrase,
                'type': self._classify_sub_theme(sentence)
            }
            sub_themes.append(sub_theme)
            
        # 3. 소주제가 부족하면 키워드 기반으로 추가
        if len(sub_themes) < 3:
            keywords = self._extract_keywords(content)
            for keyword in keywords:
                if len(sub_themes) >= 4:
                    break
                sub_theme = {
                    'order': len(sub_themes) + 1,
                    'title': keyword,
                    'content': f"{keyword} 관련 내용",
                    'type': 'keyword'
                }
                sub_themes.append(sub_theme)
                
        return sub_themes
    
    def _extract_key_facts(self, key_points: str) -> List[str]:
        """핵심 사실 추출"""
        
        facts = []
        
        # 개조식 문장 분리
        lines = key_points.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('•') or line.startswith('-') or line.startswith('·'):
                fact = line[1:].strip()
                if fact:
                    facts.append(fact)
            elif line and len(line) < 100:  # 짧은 문장은 팩트로 간주
                facts.append(line)
                
        return facts[:5]  # 최대 5개
    
    def _analyze_structure(self, content: str) -> Dict[str, Any]:
        """콘텐츠 구조 분석"""
        
        structure = {
            'has_numbers': bool(re.search(r'\d+', content)),
            'has_quotes': bool(re.search(r'["""''"]', content)),
            'has_future_plan': bool(re.search(r'예정|계획|목표|전망', content)),
            'has_comparison': bool(re.search(r'대비|비교|증가|감소|상승|하락', content)),
            'complexity': 'high' if len(content) > 500 else 'medium' if len(content) > 200 else 'low'
        }
        
        return structure
    
    def _extract_entities(self, content: str) -> Dict[str, List[str]]:
        """주요 개체명 추출"""
        
        entities = {
            'organizations': [],
            'technologies': [],
            'locations': [],
            'dates': []
        }
        
        # 기관/기업
        org_pattern = r'([가-힣]+(?:전력|에너지|기술|산업|공사|청|부|원|단|社|사))'
        entities['organizations'] = list(set(re.findall(org_pattern, content)))[:3]
        
        # 기술/제품
        tech_keywords = ['태양광', 'ESS', 'VPP', '배터리', '인버터', '스마트그리드', 'AI', 'IoT']
        for keyword in tech_keywords:
            if keyword in content:
                entities['technologies'].append(keyword)
                
        # 지역
        location_pattern = r'([가-힣]+(?:시|도|구|군|읍|면|동))'
        entities['locations'] = list(set(re.findall(location_pattern, content)))[:3]
        
        # 날짜
        date_pattern = r'(\d{4}년|\d{1,2}월|\d{1,2}일)'
        entities['dates'] = list(set(re.findall(date_pattern, content)))[:3]
        
        return entities
    
    def _extract_numbers(self, content: str) -> List[Dict[str, str]]:
        """핵심 수치 정보 추출"""
        
        numbers = []
        
        # 다양한 숫자 패턴
        patterns = [
            (r'(\d+(?:\.\d+)?)\s*MW', 'power', 'MW'),
            (r'(\d+(?:\.\d+)?)\s*kW', 'power', 'kW'),
            (r'(\d+(?:\.\d+)?)\s*%', 'percentage', '%'),
            (r'(\d+(?:,\d{3})*)\s*억\s*원', 'money', '억원'),
            (r'(\d+(?:,\d{3})*)\s*원', 'money', '원'),
            (r'(\d+)\s*년', 'year', '년'),
            (r'(\d+)\s*개', 'count', '개'),
            (r'(\d+)\s*명', 'people', '명')
        ]
        
        for pattern, num_type, unit in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # 주변 문맥 추출
                context_pattern = rf'[\w\s]{{0,20}}{match}\s*{unit}[\w\s]{{0,20}}'
                context_match = re.search(context_pattern, content)
                if context_match:
                    context = context_match.group().strip()
                else:
                    context = f"{match} {unit}"
                    
                numbers.append({
                    'value': match,
                    'unit': unit,
                    'type': num_type,
                    'context': context
                })
                
        # 중복 제거 및 상위 5개만 반환
        seen = set()
        unique_numbers = []
        for num in numbers:
            key = f"{num['value']}_{num['unit']}"
            if key not in seen:
                seen.add(key)
                unique_numbers.append(num)
                
        return unique_numbers[:5]
    
    def _categorize_theme(self, title: str) -> str:
        """주제 카테고리 분류"""
        
        categories = {
            '정책/규제': ['정책', '규제', '법안', '제도', '정부', '청', '부'],
            '기술개발': ['개발', '기술', '혁신', '연구', '특허', 'R&D'],
            '사업/투자': ['투자', '사업', '구축', '건설', '착공', '준공'],
            '시장동향': ['시장', '거래', '가격', '수요', '공급', '전망'],
            '협력/제휴': ['협력', '제휴', 'MOU', '협약', '파트너십'],
            '성과/실적': ['성과', '실적', '달성', '증가', '성장']
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in title:
                    return category
                    
        return '일반'
    
    def _identify_focus(self, title: str, summary: str) -> str:
        """초점 식별"""
        
        combined = f"{title} {summary}".lower()
        
        if any(word in combined for word in ['미래', '계획', '예정', '목표']):
            return '미래전망'
        elif any(word in combined for word in ['문제', '과제', '해결', '대응']):
            return '문제해결'
        elif any(word in combined for word in ['성과', '달성', '완료', '실적']):
            return '성과발표'
        elif any(word in combined for word in ['도입', '시작', '착수', '개시']):
            return '신규도입'
        else:
            return '현황보고'
    
    def _extract_key_phrase(self, sentence: str) -> str:
        """문장에서 핵심 구문 추출"""
        
        # 불필요한 수식어 제거
        remove_patterns = [
            r'이에 따라|따라서|그러나|하지만|또한|아울러',
            r'한편|특히|실제로|사실상',
            r'것으로 알려졌다|것으로 전해졌다|고 밝혔다|고 전했다'
        ]
        
        result = sentence
        for pattern in remove_patterns:
            result = re.sub(pattern, '', result)
            
        # 핵심 동사구 찾기
        verb_patterns = [
            r'(\w+을?\s*\w+(?:한다|했다|할\s*예정이다))',
            r'(\w+(?:를|을)?\s*\w+하기로\s*했다)'
        ]
        
        for pattern in verb_patterns:
            match = re.search(pattern, result)
            if match:
                return match.group().strip()
                
        # 패턴이 없으면 앞 50자만 반환
        return result[:50] + '...' if len(result) > 50 else result
    
    def _create_sub_theme_title(self, phrase: str) -> str:
        """소주제 제목 생성"""
        
        # 긴 문장을 짧은 제목으로
        if len(phrase) > 20:
            # 핵심 명사구 추출
            nouns = re.findall(r'([가-힣]+(?:화|성|도|안|책|업))', phrase)
            if nouns:
                return nouns[0]
            else:
                return phrase[:15] + '...'
        else:
            return phrase
    
    def _classify_sub_theme(self, sentence: str) -> str:
        """소주제 유형 분류"""
        
        if re.search(r'\d+%|\d+억|\d+MW', sentence):
            return 'data'
        elif re.search(r'목표|계획|예정', sentence):
            return 'plan'
        elif re.search(r'효과|기대|전망', sentence):
            return 'effect'
        elif re.search(r'문제|과제|어려움', sentence):
            return 'challenge'
        else:
            return 'fact'
    
    def _extract_keywords(self, content: str) -> List[str]:
        """키워드 추출"""
        
        # 단어 빈도 분석
        words = re.findall(r'[가-힣]{2,}', content)
        word_freq = Counter(words)
        
        # 불용어 제거
        stopwords = ['있다', '없다', '하다', '되다', '이다', '그리고', '또한', '하지만']
        for stopword in stopwords:
            word_freq.pop(stopword, None)
            
        # 상위 키워드 반환
        return [word for word, count in word_freq.most_common(5)]


# 테스트
if __name__ == "__main__":
    analyzer = ArticleContentAnalyzer()
    
    # 샘플 기사
    sample = {
        'title': '한전, 제주 재생에너지 출력제어 해결 위한 ESS 300MW 구축 추진',
        'summary': '한국전력공사가 제주도의 재생에너지 출력제어 문제 해결을 위해 300MW 규모의 ESS를 구축한다고 발표했다.',
        'key_points': '• 2026년까지 300MW ESS 구축\n• 총 사업비 5000억원 투입\n• 출력제어율 30%에서 10%로 감소 기대\n• 지역 주민 일자리 500개 창출',
        'source': '전기신문'
    }
    
    analysis = analyzer.analyze_article(sample)
    
    print("📊 기사 분석 결과")
    print("=" * 50)
    print(f"\n🎯 대주제: {analysis['main_theme']['theme']}")
    print(f"   카테고리: {analysis['main_theme']['category']}")
    print(f"   초점: {analysis['main_theme']['focus']}")
    
    print("\n📌 소주제:")
    for sub in analysis['sub_themes']:
        print(f"   {sub['order']}. {sub['title']} ({sub['type']})")
        
    print("\n💡 핵심 사실:")
    for fact in analysis['key_facts']:
        print(f"   • {fact}")
        
    print("\n🔢 주요 수치:")
    for num in analysis['numbers']:
        print(f"   • {num['value']} {num['unit']}: {num['context']}")
