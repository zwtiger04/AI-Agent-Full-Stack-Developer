import sys

# 파일 읽기
with open('INTEGRATED_PROJECT_GUIDE.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 보안 주의사항 섹션 찾기
insert_position = -1
for i, line in enumerate(lines):
    if '## 🔒 보안 주의사항' in line:
        # 다음 ## 섹션을 찾거나 파일 끝까지
        for j in range(i+1, len(lines)):
            if lines[j].startswith('## ') or lines[j].startswith('---'):
                insert_position = j
                break
        if insert_position == -1:
            # 다음 섹션이 없으면 보안 섹션 끝에 추가
            for j in range(i+1, len(lines)):
                if lines[j].strip() == '':
                    continue
                if j+1 < len(lines) and lines[j+1].strip() == '':
                    insert_position = j+2
                    break

# 코딩 표준 내용 추가
coding_standards = '''
## 📏 코딩 표준 및 규칙 [STANDARDS-001]

### 1. 클래스/메서드 명명 규칙 [STD-NAMING-001]

#### CostManager 클래스
```python
class CostManager:
    def __init__(self)
    def load_costs(self) -> dict
    def save_costs(self) -> None
    def add_cost(self, amount: float) -> None
    def get_daily_cost(self) -> float      # NOT get_today_cost()
    def get_monthly_cost(self) -> float    # NOT get_month_cost()
    def can_generate(self, daily_limit: float = 10, monthly_limit: float = 50) -> tuple
```

#### CardNewsGenerator 클래스
```python
class CardNewsGenerator:
    def __init__(self, api_key: str)       # API 키는 생성자에서 받기
    def get_color_theme(self, keyword: str) -> Dict[str, str]  # NOT get_color_scheme()
    def generate_card_news(self, article: Union[Dict, Article], 
                          theme: Union[str, Dict], 
                          sections: List[str]) -> str
```

#### 기사 로드 함수
```python
# 전역 함수로 통일
def load_interested_articles() -> List[Dict]    # 관심 기사 로드
def save_generated_card_news(article_id: str, file_path: str) -> None
```

### 2. Import 표준 [STD-IMPORTS-001]

#### 필수 Import 구조
```python
# 1. 표준 라이브러리
import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Tuple, Any

# 2. 서드파티 라이브러리
import streamlit as st
from anthropic import Anthropic  # NOT import anthropic
from dotenv import load_dotenv

# 3. 프로젝트 내부 모듈
from card_news.types import Article, Section, ThemeData
from card_news.validators import validate_sections, validate_article
from card_news.decorators import fully_validated
from card_news.section_selector import SectionSelector
from card_news.section_config import SectionConfig
from card_news.test_mode_generator import TestModeGenerator
from card_news.analytics_integration import AnalyticsDashboard

# 4. 레거시 모듈 (점진적 마이그레이션)
from update_summary import add_to_summary, update_summary_date
```

### 3. 파일 구조 표준 [STD-FILES-001]

#### 데이터 파일 규칙
```python
# 설정 파일
COST_TRACKING_FILE = 'cost_tracking.json'              # 비용 추적
PENDING_CARDNEWS_FILE = 'pending_cardnews.json'        # 대기 중 기사
PROCESSED_ARTICLES_FILE = 'processed_articles.json'    # 처리 완료 기사
GENERATED_HISTORY_FILE = 'generated_cardnews_history.json'  # 생성 이력

# 디렉토리 구조
OUTPUT_DIR = 'card_news/'                   # 카드뉴스 출력
SECTION_STYLES_PATH = 'card_news/section_styles.css'
ANALYTICS_DATA_DIR = 'analytics_data/'      # 분석 데이터
LOGS_DIR = 'logs/'                         # 로그 파일
```

#### 파일 접근 패턴
```python
# 파일 읽기 표준
def load_json_file(filepath: str, default: Any = None) -> Any:
    """JSON 파일 로드 표준 함수"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default if default is not None else {}
    except json.JSONDecodeError:
        st.error(f"JSON 파싱 오류: {filepath}")
        return default if default is not None else {}

# 파일 쓰기 표준
def save_json_file(filepath: str, data: Any) -> bool:
    """JSON 파일 저장 표준 함수"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"파일 저장 실패: {str(e)}")
        return False
```

### 4. 통합 시 체크리스트 [STD-INTEGRATION-001]

#### 코드 통합 전 확인사항
- [ ] 메서드명 일치 확인 (위 명명 규칙 참조)
- [ ] Import 구조 확인 (표준 Import 구조 준수)
- [ ] 파일 경로 상수화 확인
- [ ] 타입 힌트 추가 여부
- [ ] 에러 처리 패턴 일관성
- [ ] 로깅 규칙 준수

#### 통합 후 테스트
- [ ] 비용 계산 정확성
- [ ] 기사 로드/저장 기능
- [ ] UI 렌더링 정상 작동
- [ ] 타입 검증 통과
- [ ] 모든 파일 경로 접근 가능

'''

# 내용 삽입
if insert_position != -1:
    lines.insert(insert_position, coding_standards)
    print(f"✅ 코딩 표준이 {insert_position}번째 줄에 추가되었습니다!")
else:
    # 파일 끝에 추가
    lines.append(coding_standards)
    print("✅ 코딩 표준이 파일 끝에 추가되었습니다!")

# 파일 저장
with open('INTEGRATED_PROJECT_GUIDE.md', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ INTEGRATED_PROJECT_GUIDE.md 파일이 업데이트되었습니다!")
