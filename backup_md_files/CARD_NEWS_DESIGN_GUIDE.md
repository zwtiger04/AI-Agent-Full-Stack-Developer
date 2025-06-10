# 🎨 전력산업 카드뉴스 상세 페이지 제작 가이드

## 📅 프로젝트 정보
- **제작일**: 2025년 6월 9일
- **제작자**: Claude AI (Anthropic)
- **협력자**: KJ (프로젝트 오너)
- **프로젝트 위치**: 
  - WSL: `/home/zwtiger/AI-Agent-Full-Stack-Developer`
  - Windows: `C:\Users\KJ\Desktop\EnhancedCardNews\detailed\`

## 🎯 프로젝트 목표
전력산업 관련 뉴스를 시각적으로 매력적이고 정보 전달력이 뛰어난 상세 페이지로 제작

## 🎨 디자인 원칙

### 1. 색상 테마 선택
- **각 기사의 성격에 맞는 고유한 색상 조합 사용**
  - ESS/배터리: 초록색/파란색 (에너지, 친환경)
  - 태양광: 노란색/주황색 (태양, 따뜻함)
  - 정책/제도: 파란색/보라색 (공식적, 신뢰)
  - 문제/도전: 빨간색/주황색 (경고, 주의)
  - 환경/기후: 녹색 (자연, 지속가능성)
  - 국제비교: 국가 상징색 활용

### 2. 히어로 섹션
```css
/* 기본 구조 */
.hero {
    background: linear-gradient(135deg, #시작색 0%, #중간색 50%, #끝색 100%);
    min-height: 500px;
    /* 애니메이션 배경 효과 추가 */
}

/* 제목 그라데이션 */
.hero h1 {
    background: linear-gradient(45deg, #색상1, #색상2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
```

### 3. 필수 구성 요소

#### 섹션 구조
1. **히어로 섹션**: 제목, 메타정보, 배경 애니메이션
2. **핵심 인사이트**: 주요 메시지 강조
3. **상세 분석**: 카드, 차트, 타임라인 등
4. **데이터 시각화**: 통계, 비교, 진행상황
5. **전문가 의견/전망**: 인용구, 미래 예측

#### 인터랙티브 요소
- **호버 효과**: transform, box-shadow, 색상 변화
- **스크롤 애니메이션**: Intersection Observer 활용
- **카운터 애니메이션**: 숫자 증가 효과
- **프로그레스 바**: 진행률 표시

### 4. 반응형 디자인
```css
@media (max-width: 768px) {
    /* 모바일 최적화 */
    .section { padding: 30px 20px; }
    .grid { grid-template-columns: 1fr; }
}
```

## 📊 주요 컴포넌트 패턴

### 1. 정보 카드
```html
<div class="info-card">
    <span class="icon">아이콘</span>
    <h3 class="title">제목</h3>
    <p class="description">설명</p>
</div>
```

### 2. 타임라인
```html
<div class="timeline">
    <div class="timeline-line"></div>
    <div class="timeline-item">
        <div class="timeline-marker"></div>
        <div class="timeline-content">
            <div class="timeline-date">날짜</div>
            <h4>제목</h4>
            <p>내용</p>
        </div>
    </div>
</div>
```

### 3. 통계 표시
```html
<div class="stat-card">
    <div class="stat-value">수치</div>
    <div class="stat-label">라벨</div>
    <div class="stat-change">변화율</div>
</div>
```

### 4. 비교 테이블
```html
<table class="comparison-table">
    <thead>
        <tr>
            <th>구분</th>
            <th>A</th>
            <th>B</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="category">항목</td>
            <td>값A</td>
            <td>값B</td>
        </tr>
    </tbody>
</table>
```

## 🎯 품질 체크리스트

### 필수 요소
- [ ] 고유한 색상 테마
- [ ] 히어로 섹션 애니메이션
- [ ] 홈 버튼 (우상단 고정)
- [ ] 핵심 메시지 섹션
- [ ] 최소 3개 이상의 시각화 요소
- [ ] 반응형 디자인
- [ ] 인터랙티브 효과
- [ ] 전문가 의견 또는 전망

### 기술적 요구사항
- [ ] Pretendard 폰트 사용
- [ ] CSS 애니메이션 활용
- [ ] JavaScript 인터랙션
- [ ] 모바일 최적화
- [ ] 다크 테마 (#0a0a0a 배경)

## 📁 파일 구조
```
EnhancedCardNews/
├── enhanced_summary_20250609_170159.html  # 메인 요약 페이지
└── detailed/                               # 상세 페이지 폴더
    ├── detail_기사제목_ID.html            # 각 기사별 상세 페이지
    └── ...
```

## 🔄 다음 대화에서 이어가기

### 현재 상태
- ✅ 10개 기사 모두 상세 페이지 제작 완료
- ✅ 각 기사별 고유한 디자인 테마 적용
- ✅ 인터랙티브 요소 및 애니메이션 구현

### 남은 작업
1. 메인 요약 페이지(`enhanced_summary_20250609_170159.html`) 업데이트
   - 10개 기사 모두 링크 연결
   - 카드 디자인 개선
   - 필터링 기능 추가

2. 추가 개선사항
   - 기사 간 네비게이션
   - 검색 기능
   - 공유 기능
   - 인쇄 최적화

### 주요 변수 및 설정
- **노션 parent_page_id**: 2002360b26038007a59fcda976552022
- **GitHub 저장소**: zwtiger04/AI-Agent-Full-Stack-Developer
- **작업 폴더**: /home/zwtiger/AI-Agent-Full-Stack-Developer

### 스타일 가이드 요약
1. **색상**: 각 주제별 고유 색상 (ESS-초록/파란, 태양광-노랑/주황 등)
2. **레이아웃**: 히어로 → 핵심인사이트 → 상세분석 → 데이터 → 전망
3. **애니메이션**: fadeInUp, 호버효과, 카운터, 프로그레스바
4. **폰트**: Pretendard
5. **배경**: 다크테마 (#0a0a0a)

이 문서를 참고하여 동일한 품질의 상세 페이지를 계속 제작할 수 있습니다.

## 🤖 크롤러 프로젝트와 카드뉴스 프로젝트 통합 (2025년 6월 9일)

### Level 2 자동화 시스템 구현 완료

#### 구현된 기능
1. **자동 크롤링**: 전기신문 → Gemma2 LLM 요약 → 노션 저장
2. **관심 기사 모니터링**: 5분마다 체크, 17개 발견
3. **카드뉴스 생성 UI**: Streamlit 기반, Claude API 활용
4. **비용 안전장치**: 
   - 사전 고지 (체크박스)
   - 한도 관리 (일 $10, 월 $50)
   - 실시간 추적

#### 주요 파일
- `watch_interested_articles.py`: 관심 기사 모니터링
- `card_news_app.py`: 카드뉴스 생성 UI (비용 안전장치 포함)
- `run_level2.py`: 통합 실행 스크립트
- `pending_cardnews.json`: 대기 중인 17개 기사
- `cost_tracking.json`: 비용 추적 파일

#### 실행 방법
```bash
# 전체 시스템 실행
python3 run_level2.py

# UI만 테스트
streamlit run card_news_app.py
```

#### API 키 설정 상태
- ✅ ANTHROPIC_API_KEY: .env에 설정됨
- ✅ Ollama: Gemma2 모델 작동 확인

### 다음 대화에서 테스트하기
- Streamlit UI 접속하여 카드뉴스 생성 테스트
- 비용 안전장치 작동 확인
- 생성된 HTML 품질 검토

