#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 구조화된 콘텐츠 생성기
- 핵심 주제 추출
- 소주제 분류
- 데이터 시각화 요소 추출
"""

import os
import re
import json
import requests
from typing import Dict, List, Any

class StructuredContentGenerator:
    def __init__(self):
        # Ollama 설정
        self.ollama_url = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/v1/chat/completions')
        self.model = os.getenv('OLLAMA_MODEL', 'mistral:7b-instruct-v0.2-q5_k_m')
        
    def generate_structured_summary(self, article_content: str) -> Dict[str, Any]:
        """구조화된 요약 생성"""
        
        # 프롬프트 설계
        prompt = f"""다음 기사를 분석하여 구조화된 요약을 만들어주세요.

기사 내용:
{article_content[:2000]}

다음 형식으로 답변해주세요:

1. 핵심 주제: (한 문장으로 핵심 메시지)

2. 주요 포인트:
- 포인트1: (구체적인 내용)
- 포인트2: (구체적인 내용)
- 포인트3: (구체적인 내용)

3. 핵심 데이터:
- 수치1: (구체적인 숫자와 의미)
- 수치2: (구체적인 숫자와 의미)

4. 시사점: (이 기사가 전력산업에 미치는 영향)
"""
        
        try:
            # Ollama API 호출
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "당신은 전력산업 전문 분석가입니다. 기사를 체계적으로 분석하여 핵심을 추출해주세요."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                
                # 구조화된 데이터로 파싱
                return self._parse_structured_content(content)
            else:
                print(f"Ollama API 오류: {response.status_code}")
                return self._fallback_summary(article_content)
                
        except Exception as e:
            print(f"요약 생성 중 오류: {str(e)}")
            return self._fallback_summary(article_content)
            
    def _parse_structured_content(self, content: str) -> Dict[str, Any]:
        """생성된 텍스트를 구조화된 데이터로 파싱"""
        structured = {
            'core_topic': '',
            'main_points': [],
            'key_data': [],
            'implications': ''
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if '핵심 주제:' in line:
                structured['core_topic'] = line.split('핵심 주제:')[-1].strip()
            elif '주요 포인트:' in line:
                current_section = 'points'
            elif '핵심 데이터:' in line:
                current_section = 'data'
            elif '시사점:' in line:
                current_section = 'implications'
            elif line.startswith('-') and current_section:
                content = line[1:].strip()
                if current_section == 'points':
                    structured['main_points'].append(content)
                elif current_section == 'data':
                    structured['key_data'].append(content)
            elif current_section == 'implications' and line:
                structured['implications'] += line + ' '
                
        return structured
        
    def _fallback_summary(self, content: str) -> Dict[str, Any]:
        """규칙 기반 폴백 요약"""
        sentences = re.split(r'[.!?]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return {
            'core_topic': sentences[0] if sentences else '내용 없음',
            'main_points': sentences[1:4] if len(sentences) > 1 else [],
            'key_data': self._extract_numbers(content),
            'implications': '추가 분석 필요'
        }
        
    def _extract_numbers(self, text: str) -> List[str]:
        """텍스트에서 숫자 데이터 추출"""
        # 숫자와 단위가 포함된 패턴 찾기
        patterns = [
            r'\d+(?:\.\d+)?%',  # 퍼센트
            r'\d+(?:,\d{3})*(?:\.\d+)?(?:원|달러|MW|GW|kWh)',  # 단위 포함
            r'\d{4}년',  # 연도
        ]
        
        results = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            results.extend(matches)
            
        return results[:5]  # 최대 5개까지
        
    def extract_visualization_data(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """시각화를 위한 데이터 추출"""
        viz_data = {
            'timeline': [],  # 시간대별 데이터
            'categories': {},  # 카테고리별 분포
            'trends': [],  # 트렌드 데이터
            'comparisons': []  # 비교 데이터
        }
        
        # 카테고리별 분류
        for article in articles:
            for keyword in article.get('keywords', []):
                viz_data['categories'][keyword] = viz_data['categories'].get(keyword, 0) + 1
                
        # 날짜별 분류
        date_counts = {}
        for article in articles:
            if article.get('published_date'):
                date_str = str(article['published_date'])[:10]
                date_counts[date_str] = date_counts.get(date_str, 0) + 1
                
        viz_data['timeline'] = [
            {'date': date, 'count': count} 
            for date, count in sorted(date_counts.items())
        ]
        
        # AI 추천 vs 일반
        ai_count = sum(1 for a in articles if a.get('ai_recommend'))
        viz_data['comparisons'] = [
            {'label': 'AI 추천', 'value': ai_count},
            {'label': '일반', 'value': len(articles) - ai_count}
        ]
        
        return viz_data

# 사용 예시
if __name__ == "__main__":
    generator = StructuredContentGenerator()
    
    # 테스트 기사
    test_content = """
    한국에너지기술연구원은 차세대 페로브스카이트 태양전지 기술을 개발해 
    에너지 변환 효율 30%를 달성했다고 발표했다. 이는 기존 실리콘 태양전지 
    대비 50% 이상 제조비용을 절감할 수 있으며, 2025년 상용화를 목표로 하고 있다.
    
    연구팀은 새로운 소재 조합과 제조 공정 최적화를 통해 안정성과 효율성을 
    동시에 확보했다. 특히 고온 다습한 환경에서도 90% 이상의 효율을 유지할 수 
    있어 실제 환경에서의 적용 가능성을 입증했다.
    """
    
    # 구조화된 요약 생성
    summary = generator.generate_structured_summary(test_content)
    print("구조화된 요약:")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
