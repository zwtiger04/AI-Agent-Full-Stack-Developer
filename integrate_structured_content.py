#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 구조화된 콘텐츠를 기존 시스템에 통합하는 가이드
"""

# 1. 기존 v2를 업데이트하여 구조화된 콘텐츠 사용
def update_existing_v2():
    """기존 card_news_generator_v2.py 업데이트 방법"""
    
    # Step 1: import 추가
    # from structured_content_generator import StructuredContentGenerator
    
    # Step 2: __init__에 추가
    # self.content_generator = StructuredContentGenerator()
    
    # Step 3: 새로운 메서드 추가
    """
    def generate_weekly_report(self):
        '''주간 리포트 형식의 카드뉴스 생성'''
        # 전체 기사 가져오기
        database_id = self.notion.get_weekly_database_id()
        all_articles = self.notion.get_all_articles_from_db(database_id)
        
        # 구조화된 분석
        analysis = self.content_generator.analyze_articles(all_articles)
        
        # 카드 생성
        cards = []
        cards.append(self._create_weekly_summary_card(analysis))
        cards.append(self._create_category_chart(analysis))
        cards.append(self._create_trend_analysis(analysis))
        
        # 주요 기사 카드 추가
        for article in analysis['top_articles']:
            cards.append(self.create_article_card(article))
            
        return cards
    """

# 2. 실행 스크립트 수정
def update_run_script():
    """run_card_news_upload.py 수정 예시"""
    
    script_content = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""개선된 카드뉴스 실행 스크립트"""

from card_news_generator_v2 import CardNewsGeneratorV2
from structured_content_generator import StructuredContentGenerator

def main():
    generator = CardNewsGeneratorV2()
    generator.content_generator = StructuredContentGenerator()
    
    # 옵션 1: 관심 기사만 (기존 방식)
    # generator.generate_card_news()
    
    # 옵션 2: 주간 리포트 (새로운 방식)
    generator.generate_weekly_report()

if __name__ == "__main__":
    main()
'''
    
    with open('run_structured_cards.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ 실행 스크립트 생성됨: run_structured_cards.py")

# 3. 점진적 마이그레이션 계획
def migration_plan():
    """단계별 마이그레이션 계획"""
    
    plan = """
📋 구조화된 콘텐츠 마이그레이션 계획

1️⃣ 현재 단계 (완료):
   - 구조화된 콘텐츠 생성기 개발 ✅
   - 기본 분석 기능 구현 ✅
   - 테스트 완료 ✅

2️⃣ 다음 단계 (시각화 개선):
   - 차트/그래프 라이브러리 통합
   - 인터랙티브 요소 추가
   - 애니메이션 효과 고려

3️⃣ 최종 단계 (디자인 업그레이드):
   - 모던한 색상 팔레트 적용
   - 그라데이션 및 효과 추가
   - 반응형 레이아웃 고려

💡 추천 작업 순서:
1. structured_content_generator.py를 프로젝트에 추가
2. card_news_generator_v2.py에 import 추가
3. 새로운 generate_weekly_report() 메서드 추가
4. 테스트 실행
5. 점진적으로 기능 확장
"""
    
    return plan

if __name__ == "__main__":
    print("🔗 구조화된 콘텐츠 통합 가이드")
    print("=" * 50)
    
    # 실행 스크립트 생성
    update_run_script()
    
    # 마이그레이션 계획 출력
    print(migration_plan())
    
    print("\n✨ 추천 명령어:")
    print("1. 테스트: python3 test_structured_cards.py")
    print("2. 실행: python3 run_structured_cards.py")
    print("3. 기존 실행: python3 run_card_news_upload.py")
