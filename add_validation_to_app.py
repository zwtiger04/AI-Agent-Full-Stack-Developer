import re

# card_news_app_integrated.py 파일 읽기
with open('card_news_app_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# import 섹션 찾기 및 수정
import_section = """import streamlit as st
import json
import os
from datetime import datetime
from card_news.card_news_generator import CardNewsGenerator
from card_news.section_selector import SectionSelector
import logging
from card_news.section_analytics import SectionAnalytics"""

new_import_section = """import streamlit as st
import json
import os
from datetime import datetime
from card_news.card_news_generator import CardNewsGenerator
from card_news.section_selector import SectionSelector
import logging
from card_news.section_analytics import SectionAnalytics
from validate_before_api import CardNewsValidator"""

content = content.replace(import_section, new_import_section)

# 생성 버튼 부분 찾아서 수정
# "🎨 카드뉴스 생성하기" 버튼 이후 코드 수정
old_pattern = r'if st\.button\("🎨 카드뉴스 생성하기".*?\):\s*\n\s*if st\.checkbox'
new_code = '''if st.button("🎨 카드뉴스 생성하기", key=f"generate_{idx}", type="primary"):
                            # 검증 단계 추가
                            validator = CardNewsValidator()
                            
                            # 현재 일일 비용 계산
                            today = datetime.now().strftime("%Y-%m-%d")
                            current_daily_cost = cost_tracker.get('daily', {}).get(today, 0)
                            
                            # 사전 검증 수행
                            is_valid, validation_result = validator.validate_all(
                                article, emphasis, current_daily_cost
                            )
                            
                            if not is_valid:
                                st.error("❌ 카드뉴스 생성 전 오류가 발견되었습니다:")
                                for error in validation_result['errors']:
                                    st.error(f"• {error}")
                                if validation_result['warnings']:
                                    for warning in validation_result['warnings']:
                                        st.warning(f"• {warning}")
                                st.info("💡 위 오류를 수정한 후 다시 시도해주세요.")
                            else:
                                # 정규화된 emphasis 사용
                                normalized_emphasis = validation_result['normalized_emphasis']
                                
                                if st.checkbox'''

# 정규 표현식으로 패턴 찾기
match = re.search(old_pattern, content, re.DOTALL)
if match:
    # 찾은 패턴을 새 코드로 교체
    content = re.sub(old_pattern, new_code, content, count=1, flags=re.DOTALL)

# 파일 저장
with open('card_news_app_integrated.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("card_news_app_integrated.py에 검증 기능 추가 완료!")
