#!/usr/bin/env python3
"""
Claude.ai 반자동화 도구
노션의 관심 기사를 프롬프트로 변환하여 클립보드에 복사
"""
import json
import pyperclip
import os
from datetime import datetime

from card_news_paths import get_path_str
def load_pending_articles():
    """대기 중인 기사 로드"""
    pending_file = get_path_str('pending_cardnews')
    if not os.path.exists(pending_file):
        return []
    
    try:
        with open(pending_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"기사 로드 실패: {str(e)}")
        return []

def generate_claude_prompt(article):
    """Claude.ai용 프롬프트 생성"""
    title = article['title']
    keywords = ', '.join(article.get('keywords', []))
    content = article.get('content', '')
    
    prompt = f"""당신은 전력 산업 전문 카드뉴스 디자이너입니다. 아래 기사를 바탕으로 Enhanced 스타일의 5페이지 카드뉴스를 HTML로 만들어주세요.

[Enhanced 스타일 가이드]
1. Pretendard 폰트 사용 (font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif)
2. 5개 섹션 구조: 
   - 섹션 1: 핵심 인사이트 (눈길을 끄는 헤드라인 + 3줄 핵심 요약)
   - 섹션 2: 주요 통계/수치 (인포그래픽, 차트)
   - 섹션 3: 타임라인/발전 과정 (시각적 타임라인)
   - 섹션 4: 전문가 의견/시사점 (인용구 스타일)
   - 섹션 5: 미래 전망/결론 (향후 전망과 CTA)

3. 카테고리별 색상 테마:
   - 재생에너지/태양광/풍력: #10B981 (그린)
   - VPP/전력중개: #06B6D4 (민트)
   - ESS/전력저장: #8B5CF6 (퍼플)
   - 전력시장/정책: #3B82F6 (블루)
   - 전력망/인프라: #1E40AF (네이비)

4. 필수 포함 요소:
   - 풍부한 CSS 애니메이션 (fade-in, slide-up, count-up 등)
   - Chart.js를 활용한 데이터 시각화
   - 반응형 디자인
   - 고품질 그래디언트와 그림자 효과
   - 인터랙티브 호버 효과

[기사 정보]
제목: {title}
키워드: {keywords}

내용:
{content}

위 내용을 바탕으로 완전한 HTML 파일을 생성해주세요. 
- 모든 CSS는 <style> 태그 내에
- 모든 JavaScript는 <script> 태그 내에
- Chart.js CDN 링크 포함
- Pretendard 폰트 CDN 링크 포함
- 한글 주석 포함"""
    
    return prompt

def main():
    """메인 실행 함수"""
    articles = load_pending_articles()
    
    if not articles:
        print("❌ 대기 중인 기사가 없습니다.")
        return
    
    print("📰 대기 중인 기사 목록:")
    for i, article in enumerate(articles):
        print(f"{i+1}. {article['title']}")
    
    choice = input("\n프롬프트를 생성할 기사 번호를 선택하세요 (0: 전체): ")
    
    if choice == '0':
        # 전체 기사 프롬프트 생성
        print("\n⚠️  전체 기사는 개별적으로 Claude.ai에 입력해야 합니다.")
        for i, article in enumerate(articles):
            prompt = generate_claude_prompt(article)
            filename = f"claude_prompt_{i+1}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(prompt)
            print(f"✅ {filename} 생성 완료")
    else:
        # 선택한 기사 프롬프트 생성
        idx = int(choice) - 1
        if 0 <= idx < len(articles):
            article = articles[idx]
            prompt = generate_claude_prompt(article)
            
            # 클립보드에 복사
            try:
                pyperclip.copy(prompt)
                print("\n✅ 프롬프트가 클립보드에 복사되었습니다!")
                print("🌐 https://claude.ai 에서 붙여넣기(Ctrl+V) 하세요.")
            except:
                # 클립보드 복사 실패 시 파일로 저장
                filename = f"claude_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(prompt)
                print(f"\n✅ 프롬프트가 {filename}에 저장되었습니다.")
            
            print(f"\n📋 생성된 카드뉴스 저장 방법:")
            print(f"1. Claude.ai에서 HTML 생성 후 복사")
            print(f"2. 파일명: detail_{article['title'].replace(' ', '_')}.html")
            print(f"3. 저장 위치: /home/zwtiger/AI-Agent-Full-Stack-Developer/detailed/")

if __name__ == "__main__":
    main()
