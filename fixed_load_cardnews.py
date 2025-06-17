def load_generated_card_news():
    """생성된 카드뉴스 목록 로드 - summary_cards.json 사용"""
    import json
    from pathlib import Path
    from datetime import datetime
    
    card_news_list = []
    
    # summary_cards.json 로드
    try:
        with open('data/card_news/json/summary_cards.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            cards = data.get('cards', [])
            
            for card in cards:
                # 카테고리 매핑
                category_map = {
                    '태양광': ('solar', '태양광'),
                    'ESS': ('ess', 'ESS'),
                    '정책': ('policy', '정책'),
                    'VPP': ('vpp', 'VPP'),
                    '재생에너지': ('renewable', '재생에너지'),
                    '기술': ('tech', '기술'),
                    '시장': ('market', '시장'),
                    '일반': ('general', '일반')
                }
                
                category_name = card.get('category', '일반')
                category_info = category_map.get(category_name, ('general', '일반'))
                
                # 날짜 처리
                date = card.get('date', '')
                if not date:
                    # 파일명에서 날짜 추출 시도
                    file_name = card.get('file_path', '')
                    date_match = file_name.split('_')[-1].replace('.html', '')
                    if len(date_match) == 8 and date_match.isdigit():
                        date = f"{date_match[:4]}-{date_match[4:6]}-{date_match[6:8]}"
                    else:
                        date = datetime.now().strftime("%Y-%m-%d")
                
                card_news_list.append({
                    "title": card.get('title', ''),
                    "date": date,
                    "category": category_info[0],
                    "category_name": category_info[1],
                    "file_path": f"output/card_news/html/{card.get('file_path', '')}",
                    "summary": card.get('summary', ''),
                    "source": "전기신문",
                    "keywords": card.get('keywords', [])
                })
    
    except FileNotFoundError:
        # summary_cards.json이 없으면 기존 방식으로 폴백
        html_dir = Path("output/card_news/html")
        for html_file in html_dir.glob("detail_*.html"):
            filename = html_file.stem
            parts = filename.replace("detail_", "").rsplit("_", 1)
            
            if len(parts) == 2:
                title = parts[0].replace("-", " ")
                date_str = parts[1]
                
                try:
                    if len(date_str) == 8:
                        date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                    else:
                        date = "2025-06-10"
                except:
                    date = "2025-06-10"
                
                card_news_list.append({
                    "title": title,
                    "date": date,
                    "category": "general",
                    "category_name": "일반",
                    "file_path": f"output/card_news/html/{html_file.name}",
                    "summary": f"{title}에 대한 상세한 분석과 전망을 담은 카드뉴스입니다.",
                    "source": "전기신문",
                    "keywords": []
                })
    
    # 날짜순 정렬 (최신순)
    card_news_list.sort(key=lambda x: x['date'], reverse=True)
    
    return card_news_list
