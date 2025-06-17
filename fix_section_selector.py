import fileinput
import sys

# section_selector.py 수정
filename = 'card_news/section_selector.py'

# 수정할 내용
old_code = """        # 섹션별 사용 횟수 업데이트
        for section_id, _ in selected_sections:
            analytics_data['section_counts'][section_id] = analytics_data['section_counts'].get(section_id, 0) + 1"""

new_code = """        # 섹션별 사용 횟수 업데이트
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

# 파일 읽기
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# 내용 수정
content = content.replace(old_code, new_code)

# 파일 쓰기
with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)

print("section_selector.py 수정 완료!")
