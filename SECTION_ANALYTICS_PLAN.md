# section_analytics.py 구현 계획

## 개요
- **작업 ID**: SECTION-007
- **목적**: 섹션 사용 패턴 추적 및 분석
- **연계**: SECTION-003의 save_selection_analytics()와 데이터 호환

## 클래스 구조

```python
class SectionAnalytics:
    def __init__(self):
        self.data_file = 'card_news/section_analytics.json'
        self.config = SectionConfig()
        
    # 데이터 관리
    def load_data(self) -> Dict
    def save_data(self, data: Dict)
    def add_selection(self, article_id: str, sections: List, scores: Dict)
    
    # 기본 분석
    def get_section_usage_stats(self) -> Dict[str, Dict]
        # 반환: {section_id: {count, avg_score, percentage}}
    
    def get_temporal_patterns(self, period: str = 'daily') -> Dict
        # 반환: 시간대별 섹션 사용 패턴
    
    def get_keyword_section_correlation(self) -> Dict[str, List]
        # 반환: {keyword: [most_used_sections]}
    
    # 고급 분석
    def analyze_selection_accuracy(self) -> float
        # 선택된 섹션의 평균 점수로 정확도 측정
    
    def find_underutilized_sections(self) -> List[str]
        # 사용률이 낮은 섹션 찾기
    
    def suggest_trigger_improvements(self) -> Dict[str, List[str]]
        # 트리거 단어 개선 제안
    
    # 리포트 생성
    def generate_weekly_report(self) -> str
        # 주간 리포트 생성 (Markdown)
    
    def create_visualization(self, chart_type: str = 'usage') -> plt.Figure
        # matplotlib 차트 생성
    
    def export_insights(self, format: str = 'json') -> Union[Dict, str]
        # 인사이트 내보내기
```

## 데이터 구조

### 입력 (section_analytics.json)
```json
{
  "selections": [
    {
      "article_id": "article_123",
      "timestamp": "2025-06-11T23:30:00",
      "sections": ["statistics", "timeline", "policy"],
      "scores": {"statistics": 8, "timeline": 8, "policy": 4},
      "article_keywords": ["재생에너지", "2030", "정책"]  // 추가 필드
    }
  ],
  "section_counts": {
    "statistics": 15,
    "timeline": 12,
    "policy": 10
  }
}
```

### 출력 예시

#### 1. 사용 통계
```json
{
  "statistics": {
    "count": 15,
    "percentage": 25.0,
    "avg_score": 6.5,
    "trend": "increasing"
  }
}
```

#### 2. 주간 리포트
```markdown
# 카드뉴스 섹션 분석 리포트
기간: 2025-06-05 ~ 2025-06-11

## 🏆 가장 많이 사용된 섹션
1. 통계/현황 (25%)
2. 기술 상세 (20%)
3. 추진 일정 (15%)

## 📊 섹션별 평균 점수
- 기술 상세: 8.5점
- 통계/현황: 6.5점
- 비교 분석: 5.2점

## 💡 개선 제안
- '도전 과제' 섹션 사용률 5% → 트리거 단어 추가 제안
- '비교' 트리거에 "국내외", "글로벌" 추가 권장
```

## 시각화 기능

### 1. 섹션 사용률 파이 차트
```python
def create_usage_pie_chart(self):
    # matplotlib으로 섹션별 사용률 시각화
```

### 2. 시간대별 추이 라인 차트
```python
def create_temporal_line_chart(self):
    # 일별/주별 섹션 사용 추이
```

### 3. 히트맵
```python
def create_keyword_section_heatmap(self):
    # 키워드-섹션 상관관계 히트맵
```

## 통합 연계

### 1. card_news_app.py 연계 (SECTION-005)
```python
# 분석 결과 표시 추가
analytics = SectionAnalytics()
stats = analytics.get_section_usage_stats()
st.sidebar.metric("가장 인기 섹션", top_section)
```

### 2. section_config.py 최적화 (SECTION-002)
```python
# 트리거 단어 자동 업데이트
suggestions = analytics.suggest_trigger_improvements()
# config 파일에 제안사항 반영
```

### 3. 피드백 루프
```python
# 사용자 피드백 수집
def collect_feedback(article_id: str, rating: int):
    # 선택된 섹션의 만족도 추적
```

## 테스트 계획

### 1. 단위 테스트
- test_data_loading()
- test_statistics_calculation()
- test_report_generation()

### 2. 통합 테스트
- 실제 section_analytics.json 파일로 테스트
- 시각화 출력 확인
- 리포트 생성 검증

## 구현 우선순위
1. 기본 데이터 로드/저장 (필수)
2. 사용 통계 분석 (필수)
3. 주간 리포트 생성 (필수)
4. 시각화 기능 (선택)
5. 트리거 개선 제안 (선택)

---
이 계획을 기반으로 다음 대화창에서 section_analytics.py를 구현하세요.
