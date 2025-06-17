import re

# 파일 읽기
with open('card_news_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 현재 import 섹션 찾기
import_section = """import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime, date
import anthropic
from typing import List, Dict, Optional
from update_summary import add_to_summary, update_summary_date
import re
from card_news.section_selector import SectionSelector  # 섹션 선택기 추가
from card_news.section_config import SectionConfig    # 섹션 설정 추가"""

# 새로운 import 섹션
new_import_section = """# 1. 표준 라이브러리
import os
import json
import re
import time
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Union, Tuple, Any

# 2. 서드파티 라이브러리
import streamlit as st
from anthropic import Anthropic  # 변경: import anthropic → from anthropic import Anthropic
from dotenv import load_dotenv

# 3. 프로젝트 내부 모듈 - 타입 시스템
from card_news.types import Article, Section, ThemeData
from card_news.validators import validate_sections, validate_article
from card_news.decorators import fully_validated

# 4. 프로젝트 내부 모듈 - 기능 모듈
from card_news.section_selector import SectionSelector
from card_news.section_config import SectionConfig
from card_news.test_mode_generator import TestModeGenerator
from card_news.analytics_integration import AnalyticsDashboard

# 5. 레거시 모듈 (점진적 마이그레이션)
from update_summary import add_to_summary, update_summary_date"""

# import 섹션 교체
content = content.replace(import_section, new_import_section)

# anthropic 사용 부분 변경
# self.anthropic_client = anthropic.Anthropic → self.anthropic_client = Anthropic
content = re.sub(r'anthropic\.Anthropic', 'Anthropic', content)

# 상수 추가 (import 섹션 다음에)
constants_section = """

# 비용 상수 (2025년 6월 기준)
COST_PER_REQUEST = 0.555  # USD
COST_PER_REQUEST_KRW = 750  # KRW

# 파일 경로 상수
COST_TRACKING_FILE = 'cost_tracking.json'
PENDING_CARDNEWS_FILE = 'pending_cardnews.json'
PROCESSED_ARTICLES_FILE = 'processed_articles.json'
GENERATED_HISTORY_FILE = 'generated_cardnews_history.json'
SECTION_STYLES_PATH = 'card_news/section_styles.css'
"""

# import 섹션 뒤에 상수 추가
import_end_pattern = r'from update_summary import add_to_summary, update_summary_date'
content = re.sub(import_end_pattern, import_end_pattern + constants_section, content)

# self.cost_file = 'cost_tracking.json' → self.cost_file = COST_TRACKING_FILE 변경
content = re.sub(r"self\.cost_file = 'cost_tracking\.json'", "self.cost_file = COST_TRACKING_FILE", content)
content = re.sub(r"self\.pending_file = 'pending_cardnews\.json'", "self.pending_file = PENDING_CARDNEWS_FILE", content)
content = re.sub(r"self\.processed_file = 'processed_articles\.json'", "self.processed_file = PROCESSED_ARTICLES_FILE", content)

# 파일 저장
with open('card_news_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Phase 1.1 완료: Import 구조가 통합되었습니다!")
print("\n변경 내용:")
print("1. Import 구조 표준화 완료")
print("2. anthropic.Anthropic → Anthropic 변경")
print("3. 타입 시스템 import 추가")
print("4. 파일 경로 상수화")
