# 카드뉴스 생성 시스템 구조 및 데이터 플로우

## 🏗️ 시스템 아키텍처

### [ARCH-001] 전체 시스템 구조
```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│  Section Logic   │────▶│ Card Generator  │
│ (Frontend)      │     │  (Business)      │     │ (Output)        │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │                         │
         ▼                       ▼                         ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Notion Client   │     │ Analytics Engine │     │ Claude/Test API │
│ (Data Source)   │     │ (Intelligence)   │     │ (Generation)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### [FLOW-001] 데이터 타입 플로우
```
1. 사용자 입력 (UI)
   └─▶ st.multiselect() → List[str]
   
2. 섹션 추천 (Logic)
   └─▶ recommend_sections() → List[Tuple[str, int]]
   
3. 섹션 최적화 (Analytics)
   └─▶ get_optimized_sections() → List[str] | List[Tuple] | Mixed
   
4. 데이터 저장 (Storage)
   └─▶ save_selection_analytics() → JSON (normalized)
   
5. 카드뉴스 생성 (Generation)
   └─▶ generate_card_news() → HTML string
```

### [FLOW-002] 문제 발생 지점
```
❌ P1: save_selection_analytics() - section_id가 list일 때
❌ P2: templates.get(theme_name) - theme_name이 list일 때
❌ P3: 기타 딕셔너리 키 접근 시 unhashable type 오류
```

## 📁 주요 파일 구조

### [FILE-001] Frontend Layer
- `card_news_app_integrated.py` - 메인 Streamlit 앱

### [FILE-002] Logic Layer
- `card_news/section_selector.py` - 섹션 선택 로직
- `card_news/section_config.py` - 섹션 설정
- `card_news/section_analytics.py` - 분석 엔진

### [FILE-003] Integration Layer
- `card_news/analytics_integration.py` - 분석 통합
- `card_news/test_mode_generator.py` - 테스트 모드

### [FILE-004] Generation Layer
- `card_news_generator.py` - 실제 생성 로직

## 🔄 데이터 변환 매트릭스

| 단계 | 함수 | 입력 타입 | 출력 타입 | 문제점 |
|------|------|-----------|-----------|---------|
| [CONV-001] | st.multiselect | - | List[str] | - |
| [CONV-002] | recommend_sections | Dict | List[Tuple[str, int]] | - |
| [CONV-003] | get_optimized_sections | List[Tuple] | List[str] | 불일치 |
| [CONV-004] | save_selection_analytics | Mixed | JSON | TypeError |
| [CONV-005] | generate_card_news | Mixed | HTML | TypeError |

## 🚨 크리티컬 이슈

### [ISSUE-001] 타입 불일치
- 여러 함수가 서로 다른 타입 기대/반환
- 명확한 타입 계약 부재

### [ISSUE-002] 방어적 프로그래밍 부재
- 입력값 검증 없음
- 타입 변환 로직 산재

### [ISSUE-003] 중앙 검증 시스템 부재
- 각 함수가 개별적으로 타입 처리
- 일관성 없는 오류 처리
