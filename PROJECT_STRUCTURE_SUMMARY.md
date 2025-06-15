# 📂 프로젝트 구조 및 파일 요약

## 🆕 최신 업데이트 (2025-06-15)

### 새로 추가된 파일들
```
card_news/
├── section_analytics.py         # 섹션 사용 패턴 분석
├── analytics_integration.py     # Streamlit 대시보드 통합
card_news_app_integrated.py      # 통합된 Streamlit UI
run_integrated_cardnews.py       # 통합 실행 스크립트
```

### 주요 문서 업데이트
- **README.md**: 분석 대시보드 기능 추가
- **INTEGRATED_PROJECT_GUIDE.md**: 통합 시스템 사용법 추가
- **SECTION_SYSTEM_WORK_LOG.md**: 섹션 시스템 작업 내역 정리

## 📊 시스템 흐름도

```
1. 뉴스 크롤링 (main.py)
   ↓
2. 노션 저장 (notion_client.py)
   ↓
3. 관심 기사 선택 (노션에서 체크)
   ↓
4. 카드뉴스 생성 시스템
   ├── 기존: card_news_app.py
   └── 🆕 통합: card_news_app_integrated.py
       ├── 섹션 추천 (section_selector.py)
       ├── 품질 평가 (analytics_integration.py)
       └── 자동 최적화 (section_analytics.py)
```

## 🚀 실행 명령어 모음

### 기본 작업
```bash
# 환경 활성화
source venv/bin/activate

# 뉴스 크롤링
python main.py

# 카드뉴스 생성 (기존)
python3 run_level2.py

# 🆕 카드뉴스 생성 (통합)
python3 run_integrated_cardnews.py
```

### 개별 실행
```bash
# 모니터링만
python3 watch_interested_articles.py

# UI만 (기존)
streamlit run card_news_app.py

# 🆕 UI만 (통합)
streamlit run card_news_app_integrated.py
```

## 📈 주요 개선사항

1. **섹션 기반 구성**: 18개 섹션으로 체계적 카드뉴스 구성
2. **AI 최적화**: 데이터 기반 섹션 추천 및 자동 개선
3. **품질 평가**: 사용자 피드백 수집 및 학습
4. **분석 대시보드**: 실시간 성능 모니터링 및 인사이트

## 💡 다음 단계

1. 데이터 수집 (1-2주)
2. 성능 분석 및 임계값 조정
3. A/B 테스트 기능 추가
4. 머신러닝 모델 고도화

---
*최종 업데이트: 2025-06-15*
