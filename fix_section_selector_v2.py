#!/usr/bin/env python3
"""
section_selector.py의 save_selection_analytics 함수 수정
TypeError: unhashable type: 'list' 해결
"""

import re

# 파일 읽기
with open('card_news/section_selector.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 수정할 부분 찾기
old_code = """        # 섹션별 사용 횟수 업데이트
        for section in selected_sections:
            # 다양한 형식 처리
            if isinstance(section, str):
                section_id = section
            elif isinstance(section, (tuple, list)) and len(section) > 0:
                section_id = section[0]
            elif isinstance(section, dict):
                section_id = section.get('id', section.get('section_id', ''))
            else:
                continue
                
            if section_id:
                analytics_data['section_counts'][section_id] = analytics_data['section_counts'].get(section_id, 0) + 1"""

new_code = """        # 섹션별 사용 횟수 업데이트 (정규화된 데이터 사용)
        for section_tuple in normalized_sections:
            section_id = section_tuple[0]  # 이미 문자열로 변환됨
            
            # 추가 안전장치: section_id가 여전히 리스트인 경우 처리
            if isinstance(section_id, list):
                section_id = str(section_id[0]) if section_id else ''
            elif not isinstance(section_id, str):
                section_id = str(section_id)
                
            if section_id:
                analytics_data['section_counts'][section_id] = analytics_data['section_counts'].get(section_id, 0) + 1"""

# 코드 교체
content = content.replace(old_code, new_code)

# 파일 저장
with open('card_news/section_selector.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ section_selector.py 수정 완료")
