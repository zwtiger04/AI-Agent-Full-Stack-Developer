# 🧪 전력산업 카드뉴스 시스템 테스트 세션

## 이전 작업 요약 (2025-06-15)
### 완료된 작업
1. **섹션 시스템 구현 완료**
   - 18개 섹션 타입 정의 (`card_news/section_config.py`)
   - AI 섹션 추천 시스템 (`card_news/section_selector.py`)
   - 섹션 사용 패턴 분석 (`card_news/section_analytics.py`)

2. **분석 대시보드 통합**
   - 실시간 대시보드 컴포넌트 (`card_news/analytics_integration.py`)
   - 통합 Streamlit UI (`card_news_app_integrated.py`)
   - 품질 평가 시스템 구현

3. **통합 실행 환경**
   - 원클릭 실행 스크립트 (`run_integrated_cardnews.py`)
   - 4개 탭 구조 (생성/분석/비용/안내)

## 현재 테스트 단계
### 테스트 목표
통합된 카드뉴스 시스템의 전체 워크플로우 검증

### 테스트 순서
1. **신규 뉴스 크롤링** ✅
   ```bash
   cd /home/zwtiger/AI-Agent-Full-Stack-Developer
   source venv/bin/activate
   python main.py
   ```

2. **관심 뉴스 체크** 🔄 (수동)
   - 노션에서 관심 기사 선택
   - "관심" 체크박스 표시

3. **상세 카드뉴스 생성** 🔄 (반자동)
   ```bash
   # 통합 시스템 실행
   python3 run_integrated_cardnews.py
   
   # 또는 직접 실행
   streamlit run card_news_app_integrated.py
   ```
   - 섹션 구성: "자동 추천 (AI 분석)" 선택
   - 품질 평가 입력

4. **요약 카드뉴스 연동** 🔄
   - 생성된 카드뉴스가 요약 페이지에 자동 추가
   - 링크 생성 확인

5. **템플릿 검토 및 피드백** 🔄 (수동)
   - 생성된 HTML 품질 검토
   - 섹션 구성 적절성 평가
   - 개선사항 도출

## 주요 확인 사항
### 기능 테스트
- [ ] 크롤링 정상 작동
- [ ] 노션 동기화 확인
- [ ] 관심 기사 로드
- [ ] AI 섹션 추천 정확도
- [ ] 카드뉴스 생성 품질
- [ ] 품질 평가 데이터 저장
- [ ] 분석 대시보드 표시

### 데이터 확인
```bash
# 크롤링 데이터
cat pending_cardnews.json | python3 -m json.tool | head -20

# 섹션 분석 데이터
cat section_analytics.json | python3 -m json.tool | head -20

# 비용 추적
cat cost_tracking.json

# 생성된 파일
ls -la detailed/*.html
```

## 환경 정보
- **작업 폴더**: `/home/zwtiger/AI-Agent-Full-Stack-Developer`
- **Python**: 3.10.12
- **가상환경**: venv
- **필수 환경변수**:
  - NOTION_API_KEY
  - ANTHROPIC_API_KEY
  - GITHUB_TOKEN (선택)

## 문제 발생 시 대처
### 크롤링 오류
```bash
tail -f logs/crawler_*.log
```

### Streamlit 오류
```bash
# 포트 확인
lsof -i :8501

# 프로세스 종료
pkill -f streamlit
```

### 데이터 복구
```bash
# 섹션 분석 데이터 백업 복원
cp section_analytics.json.backup section_analytics.json
```

## 다음 대화창에서 시작할 명령어
```bash
# 1. 환경 활성화
cd /home/zwtiger/AI-Agent-Full-Stack-Developer
source venv/bin/activate

# 2. 현재 상태 확인
ls -la pending_cardnews.json
cat pending_cardnews.json | python3 -m json.tool | head -20

# 3. 테스트 진행 상황에 따라:
# - 크롤링이 필요하면: python main.py
# - 카드뉴스 생성이 필요하면: python3 run_integrated_cardnews.py
```

---
**참고**: 이 프롬프트를 다음 대화창에 복사하여 테스트를 이어서 진행하세요.
