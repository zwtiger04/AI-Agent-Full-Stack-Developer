#!/usr/bin/env python3
"""
analytics_integration.py의 get_optimized_sections 함수 수정
데이터 타입 일관성 확보
"""

import re

# 파일 읽기
with open('card_news/analytics_integration.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 함수 시그니처 수정
content = re.sub(
    r'def get_optimized_sections\(self, article_keywords: List\[str\], \s*original_sections: List\[str\]\)',
    'def get_optimized_sections(self, article_keywords: List[str], \n                             original_sections: Union[List[str], List[Tuple[str, int]]])',
    content
)

# 2. import 추가 (Union이 없는 경우)
if 'from typing import' in content and 'Union' not in content:
    content = re.sub(
        r'from typing import ([^)]+)',
        lambda m: f"from typing import {m.group(1)}, Union" if 'Union' not in m.group(1) else m.group(0),
        content
    )

# 함수 본문 수정
old_body = """        reliability = self.analytics.get_section_reliability()
        optimized = []
        reasons = {}
        
        # 1. 고성능 섹션 우선 포함
        for section in original_sections:
            if reliability.get(section, 0) >= 0.7:  # 신뢰도 70% 이상
                optimized.append(section)
            else:
                # 2. 저성능 섹션은 대체 섹션 찾기
                alternative = self._find_alternative_section(section, article_keywords)
                if alternative:
                    optimized.append(alternative)
                    reasons[alternative] = f"{section} 대신 추천 (신뢰도: {reliability.get(alternative, 0):.1%})"
        
        # 3. 키워드 기반 추가 섹션 제안
        for keyword in article_keywords[:3]:  # 상위 3개 키워드만
            best_sections = self.analytics.get_best_sections_for_keyword(keyword, top_n=2)
            for section, score in best_sections:
                if section not in optimized and len(optimized) < 5:
                    optimized.append(section)
                    reasons[section] = f"키워드 '{keyword}' 매칭 (점수: {score:.1f})"
        
        return optimized[:5], reasons  # 최대 5개 섹션"""

new_body = """        reliability = self.analytics.get_section_reliability()
        optimized = []
        reasons = {}
        
        # original_sections 정규화 (문자열 리스트로 변환)
        normalized_sections = []
        for section in original_sections:
            if isinstance(section, str):
                normalized_sections.append(section)
            elif isinstance(section, (tuple, list)) and len(section) > 0:
                # 튜플이나 리스트의 첫 번째 요소 사용
                section_id = section[0]
                # section_id가 리스트인 경우 처리
                if isinstance(section_id, list):
                    section_id = str(section_id[0]) if section_id else 'unknown'
                normalized_sections.append(str(section_id))
            else:
                continue
        
        # 1. 고성능 섹션 우선 포함
        for section in normalized_sections:
            if reliability.get(section, 0) >= 0.7:  # 신뢰도 70% 이상
                optimized.append(section)
            else:
                # 2. 저성능 섹션은 대체 섹션 찾기
                alternative = self._find_alternative_section(section, article_keywords)
                if alternative:
                    optimized.append(alternative)
                    reasons[alternative] = f"{section} 대신 추천 (신뢰도: {reliability.get(alternative, 0):.1%})"
        
        # 3. 키워드 기반 추가 섹션 제안
        for keyword in article_keywords[:3]:  # 상위 3개 키워드만
            best_sections = self.analytics.get_best_sections_for_keyword(keyword, top_n=2)
            for section_tuple in best_sections:
                # 튜플에서 섹션 ID 추출
                if isinstance(section_tuple, tuple) and len(section_tuple) >= 2:
                    section = str(section_tuple[0])
                    score = section_tuple[1]
                else:
                    continue
                    
                if section not in optimized and len(optimized) < 5:
                    optimized.append(section)
                    reasons[section] = f"키워드 '{keyword}' 매칭 (점수: {score:.1f})"
        
        # 최종 반환값도 문자열 리스트임을 보장
        return [str(s) for s in optimized[:5]], reasons  # 최대 5개 섹션"""

# 코드 교체
content = content.replace(old_body, new_body)

# 파일 저장
with open('card_news/analytics_integration.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ analytics_integration.py 수정 완료")
