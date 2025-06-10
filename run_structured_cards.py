
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
