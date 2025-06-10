#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📤 구조화된 카드뉴스 결과를 노션에 업로드
"""

import os
import json
from datetime import datetime
from notion.notion_client import NotionClient

def upload_to_notion():
    """노션에 분석 결과 페이지 생성"""
    
    # 가장 최근 결과 찾기
    output_dir = 'structured_cards_output'
    files = sorted([f for f in os.listdir(output_dir) if f.endswith('_metadata.json')])
    
    if not files:
        print("❌ 업로드할 결과가 없습니다.")
        return
        
    latest_metadata = files[-1]
    timestamp = latest_metadata.replace('_metadata.json', '')
    
    # 메타데이터 로드
    with open(os.path.join(output_dir, latest_metadata), 'r', encoding='utf-8') as f:
        metadata = json.load(f)
        
    print(f"📄 메타데이터 로드: {latest_metadata}")
    
    # 노션 클라이언트 초기화
    notion = NotionClient()
    parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')
    
    # 페이지 내용 구성
    content = f"""# 📊 전력산업 위클리 리포트 (구조화된 분석)

## 📅 생성 정보
- **생성 시간**: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}
- **분석 기간**: {metadata['analysis']['period']}
- **총 기사 수**: {metadata['total_articles']}건

## 🎯 주요 테마
{metadata['analysis']['main_theme']}

## 📂 카테고리별 분포
"""
    
    for category, count in metadata['analysis']['categories'].items():
        bar = "█" * (count // 2)  # 간단한 막대 그래프
        content += f"- **{category}**: {bar} {count}건\n"
        
    content += f"\n## 💡 핵심 인사이트\n"
    for insight in metadata['analysis']['insights']:
        content += f"- {insight}\n"
        
    content += f"\n## 🎨 생성된 카드\n"
    content += f"총 {metadata['cards_generated']}장의 카드가 생성되었습니다.\n\n"
    
    # 생성된 파일 목록
    card_files = [f for f in os.listdir(output_dir) if f.startswith(timestamp) and f.endswith('.png')]
    for card_file in sorted(card_files):
        card_type = card_file.replace(f"{timestamp}_", "").replace(".png", "")
        content += f"- ✅ {card_type.replace('_', ' ').title()}\n"
        
    content += f"\n## 📁 파일 위치\n"
    content += f"`{os.path.abspath(output_dir)}`\n"
    
    content += f"\n---\n"
    content += f"*이 리포트는 AI 기반 구조화된 분석 시스템으로 자동 생성되었습니다.*"
    
    # 노션 페이지 생성
    try:
        page_data = {
            "parent": {"page_id": parent_page_id},
            "properties": {
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": f"[구조화된 분석] 위클리 리포트 - {datetime.now().strftime('%Y.%m.%d')}"
                            }
                        }
                    ]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": content}
                            }
                        ]
                    }
                }
            ]
        }
        
        result = notion.client.pages.create(**page_data)
        page_url = result.get('url', '')
        
        print(f"\n✅ 노션 페이지 생성 완료!")
        print(f"📎 페이지 URL: {page_url}")
        
        # 이미지 업로드 안내
        print(f"\n💡 생성된 카드 이미지들:")
        for card_file in sorted(card_files):
            print(f"   - {card_file}")
        print(f"\n📌 이미지는 {output_dir} 폴더에서 확인할 수 있습니다.")
        
    except Exception as e:
        print(f"❌ 노션 페이지 생성 실패: {str(e)}")

if __name__ == "__main__":
    upload_to_notion()
