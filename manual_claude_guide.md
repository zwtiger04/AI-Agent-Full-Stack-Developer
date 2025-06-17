# Claude AI 수동 카드뉴스 생성 가이드

## 1. 준비 단계
1. https://claude.ai 접속
2. 카드뉴스를 만들 기사 정보 준비

## 2. 프롬프트 템플릿

### 상세 카드뉴스 생성 프롬프트:
```
당신은 전력 산업 전문 카드뉴스 디자이너입니다. 아래 기사를 바탕으로 Enhanced 스타일의 5페이지 카드뉴스를 HTML로 만들어주세요.

[Enhanced 스타일 가이드]
1. Pretendard 폰트 사용
2. 5개 섹션 구조: 핵심 인사이트 → 주요 통계 → 타임라인 → 전문가 의견 → 미래 전망
3. 카테고리별 색상 테마 (재생에너지:#10B981, VPP:#06B6D4, ESS:#8B5CF6 등)
4. 풍부한 애니메이션 효과
5. Chart.js를 활용한 데이터 시각화

[기사 정보]
제목: {기사 제목}
키워드: {키워드들}
내용: {기사 본문}

완전한 HTML 파일로 생성해주세요. CDN 링크 포함, 모든 스타일과 스크립트 인라인으로 작성.
```

### 요약 카드뉴스 항목 생성 프롬프트:
```
아래 카드뉴스들의 요약 정보를 제공해드릴게요. 각 카드뉴스를 요약 페이지에 표시할 수 있도록 다음 형식으로 정리해주세요:

카드뉴스 1:
- 제목: {제목}
- 카테고리: {VPP/ESS/재생에너지 등}
- 한줄 요약: {50자 이내}
- 파일명: {detailed/ 폴더 내 파일명}

위 정보를 바탕으로 improved_summary.html에 추가할 HTML 코드를 생성해주세요.
```

## 3. 자동화 연동 방법

### Step 1: Claude.ai에서 생성
1. 위 프롬프트 사용하여 카드뉴스 생성
2. 생성된 HTML 복사

### Step 2: 로컬에 저장
```bash
# WSL에서
cd /home/zwtiger/AI-Agent-Full-Stack-Developer/detailed
nano new_cardnews.html
# HTML 붙여넣기 후 저장

# Windows로 복사
cp new_cardnews.html /mnt/c/Users/KJ/Desktop/EnhancedCardNews/detailed/
```

### Step 3: 요약 페이지 업데이트
```bash
python3 update_summary.py
```

## 4. 품질 체크리스트
- [ ] 5개 섹션 모두 포함
- [ ] 카테고리별 색상 테마 적용
- [ ] 애니메이션 효과 작동
- [ ] 차트/그래프 표시
- [ ] 모바일 반응형
- [ ] Pretendard 폰트 적용

## 5. 일괄 처리 스크립트

여러 기사를 한번에 처리하려면:
```python
# batch_claude_template.py
articles = [
    {
        "title": "기사 제목 1",
        "keywords": ["VPP", "전력중개"],
        "content": "기사 내용..."
    },
    # 더 많은 기사들...
]

for article in articles:
    print(f"\n=== {article['title']} ===")
    print(f"키워드: {', '.join(article['keywords'])}")
    print("위 프롬프트에 이 정보를 넣어서 Claude.ai에 입력하세요.")
    print("-" * 50)
```
