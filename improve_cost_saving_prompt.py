# 비용 절감 모드 프롬프트도 개선
import re

with open('card_news_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 비용 절감 모드 프롬프트 찾아서 개선
cost_saving_prompt = '''전력 산업 카드뉴스를 5페이지로 만들어주세요.

[구조]
1. 핵심 인사이트 (헤드라인 + 3줄 요약)
2. 주요 수치 (인포그래픽)
3. 타임라인 (주요 이벤트)
4. 시사점 (전문가 의견)
5. 미래 전망 (결론)

[디자인]
- Pretendard 폰트
- 카테고리별 색상 (재생에너지:#10B981, VPP:#06B6D4, ESS:#8B5CF6, 정책:#3B82F6, 전력망:#1E40AF)
- 각 섹션 독립적 구성
- 차트/그래프 포함
- 애니메이션 효과'''

# 비용 절감 모드 프롬프트 교체
pattern = r'(prompt = f"""전력 산업 전문가로서[^"]*""")'
replacement = f'prompt = f"""{cost_saving_prompt}\n\n제목: {{title}}\n키워드: {{keywords_str}}\n내용: {{content[:1000]}}...  # 내용 일부만 전송"""'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('card_news_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 비용 절감 모드 프롬프트도 개선 완료")
