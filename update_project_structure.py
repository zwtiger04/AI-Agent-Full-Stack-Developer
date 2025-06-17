# 프로젝트 구조 업데이트
import re

# 파일 읽기
with open('INTEGRATED_PROJECT_GUIDE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 기존 프로젝트 구조 찾기
old_structure = r'''├── 📊 데이터
│   ├── feedback/              # AI 모델 데이터
│   ├── logs/                  # 실행 로그
│   ├── pending_cardnews.json  # 대기 중인 기사
│   └── cost_tracking.json     # 비용 추적'''

new_structure = r'''├── 📊 데이터
│   ├── data/card_news/
│   │   ├── json/              # JSON 데이터 파일
│   │   └── analytics/         # 분석 데이터
│   ├── output/card_news/
│   │   ├── html/              # 실제 카드뉴스
│   │   └── test/              # 테스트 카드뉴스
│   ├── feedback/              # AI 모델 데이터
│   └── logs/                  # 실행 로그'''

content = content.replace(old_structure, new_structure)

# 파일 저장
with open('INTEGRATED_PROJECT_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 프로젝트 구조 업데이트 완료!")
