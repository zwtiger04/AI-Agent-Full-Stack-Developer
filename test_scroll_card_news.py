#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 스크롤 카드뉴스 테스트
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 테스트용 더미 데이터
test_articles = [
    {
        'page_id': 'test1',
        'title': '🔋 ESS 화재 예방 신기술 개발 활발',
        'summary': 'ESS 화재 사고를 예방하기 위한 AI 기반 모니터링 시스템과 신소재 배터리 기술이 주목받고 있습니다.',
        'key_points': '• AI 기반 실시간 화재 예측 시스템 개발\n• 고체전해질 배터리로 안전성 향상\n• 열폭주 방지 신소재 분리막 적용',
        'keywords': ['ESS', '안전', 'AI', '신기술'],
        'source': '전기신문',
        'ai_recommend': True,
        'url': 'https://example.com/article1'
    },
    {
        'page_id': 'test2',
        'title': '☀️ 재생에너지 출력제어 해법 모색',
        'summary': '재생에너지 출력제어 문제 해결을 위해 ESS 연계와 수요반응(DR) 프로그램이 대안으로 떠오르고 있습니다.',
        'key_points': '• 제주도 재생에너지 출력제어율 15% 돌파\n• ESS 연계 통한 잉여전력 저장 방안\n• 실시간 요금제와 DR 프로그램 확대',
        'keywords': ['재생에너지', '출력제어', 'ESS', 'DR'],
        'source': '전기신문',
        'ai_recommend': True,
        'url': 'https://example.com/article2'
    },
    {
        'page_id': 'test3',
        'title': '🏭 VPP 사업 본격화, 전력시장 판도 변화',
        'summary': '가상발전소(VPP) 사업이 본격화되면서 분산에너지 자원의 통합 관리와 전력거래가 활성화되고 있습니다.',
        'key_points': '• 소규모 분산자원 통합 관리 플랫폼 구축\n• P2P 전력거래 시범사업 확대\n• 중개사업자 라이선스 발급 증가',
        'keywords': ['VPP', '분산에너지', '전력거래', 'P2P'],
        'source': '전기신문',
        'ai_recommend': False,
        'interest': True,
        'url': 'https://example.com/article3'
    }
]

def test_scroll_system():
    """스크롤 시스템 테스트"""
    print("🧪 스크롤 카드뉴스 테스트 시작!")
    print("=" * 50)
    
    try:
        # 스크롤 시스템 임포트
        from html_card_news.scroll_detail_generator import ScrollDetailGenerator
        from html_card_news.enhanced_card_system import EnhancedCardNewsSystem
        
        # 시스템 초기화
        detail_generator = ScrollDetailGenerator()
        system = EnhancedCardNewsSystem()
        system.detail_generator = detail_generator
        
        print(f"\n📰 테스트 기사 {len(test_articles)}개로 카드뉴스 생성 중...")
        
        # 카드뉴스 생성
        result = system.generate_complete_system(test_articles)
        
        if result.get('summary'):
            print("\n✅ 카드뉴스 생성 성공!")
            print(f"📁 요약 파일: {result['summary']}")
            print(f"📁 상세 파일 개수: {len(result.get('details', {}))}")
            
            # 생성된 파일 확인
            output_dir = system.output_dir
            print(f"\n📂 생성된 파일들:")
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    print(f"  - {os.path.join(root, file)}")
        else:
            print("❌ 카드뉴스 생성 실패!")
            
    except ImportError as e:
        print(f"❌ 필요한 모듈을 찾을 수 없습니다: {e}")
        print("\n필요한 패키지 설치가 필요할 수 있습니다:")
        print("pip install jinja2 matplotlib pillow")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scroll_system()
