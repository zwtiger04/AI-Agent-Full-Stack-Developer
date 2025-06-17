# 카드뉴스 생성 프롬프트 개선
import re

with open('card_news_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Enhanced 스타일 가이드에 맞춘 개선된 프롬프트
enhanced_prompt = '''당신은 전력 산업 전문 카드뉴스 디자이너입니다. 주어진 기사를 바탕으로 시각적으로 매력적이고 정보가 풍부한 5페이지 카드뉴스를 만들어주세요.

[중요 지침]
1. Pretendard 폰트 사용 (font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif)
2. 5개 섹션 구조: 핵심 인사이트 → 주요 통계/수치 → 타임라인/발전 과정 → 전문가 의견/시사점 → 미래 전망/결론
3. 카테고리별 색상 테마 적용
4. 애니메이션과 인터랙티브 요소 포함
5. 각 섹션은 독립적으로 이해 가능하되 전체적으로 하나의 스토리 구성

[카테고리별 색상 테마]
- 재생에너지/태양광/풍력: #10B981 (그린)
- VPP/전력중개: #06B6D4 (민트)
- ESS/전력저장: #8B5CF6 (퍼플)
- 전력시장/정책: #3B82F6 (블루)
- 전력망/인프라: #1E40AF (네이비)
- 기타: #6B7280 (그레이)

[필수 포함 요소]
1. 섹션 1 (핵심 인사이트):
   - 눈길을 끄는 헤드라인
   - 핵심 메시지 3줄 요약
   - 관련 아이콘 또는 일러스트레이션
   - 부드러운 페이드인 애니메이션

2. 섹션 2 (주요 통계/수치):
   - 인포그래픽 스타일의 숫자 시각화
   - 전년 대비 증감률
   - 차트나 그래프 (Chart.js 활용)
   - 숫자 카운트업 애니메이션

3. 섹션 3 (타임라인/발전 과정):
   - 시간 순서대로 주요 이벤트 정리
   - 비주얼 타임라인 디자인
   - 각 단계별 아이콘
   - 스크롤 기반 애니메이션

4. 섹션 4 (전문가 의견/시사점):
   - 인용구 스타일의 전문가 코멘트
   - 업계에 미치는 영향 분석
   - 관련 이해관계자 언급
   - 타이핑 효과 애니메이션

5. 섹션 5 (미래 전망/결론):
   - 향후 전망과 예측
   - 핵심 시사점 정리
   - Call to Action
   - 공유 버튼과 관련 링크

[디자인 요구사항]
- 반응형 디자인 (모바일/태블릿/데스크톱)
- 고품질 그래디언트와 그림자 효과
- 적절한 여백과 타이포그래피
- 접근성 고려 (색상 대비, 폰트 크기)
- 인쇄 가능한 레이아웃

[기술 요구사항]
- 순수 HTML/CSS/JavaScript 사용
- Chart.js를 통한 데이터 시각화
- CSS 애니메이션과 트랜지션
- 시맨틱 HTML 구조
- 주석 포함 (한글)'''

# 프롬프트 교체
pattern = r'(prompt = f"""[^"]*""")'
replacement = f'prompt = f"""{enhanced_prompt}\n\n기사 제목: {{title}}\n키워드: {{keywords_str}}\n기사 내용:\n{{content}}"""'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('card_news_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 카드뉴스 생성 프롬프트 개선 완료")
