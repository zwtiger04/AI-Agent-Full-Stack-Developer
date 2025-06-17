def load_generated_card_news():
    """생성된 카드뉴스 목록 로드 - 개선된 버전"""
    import json
    from pathlib import Path
    
    card_news_list = []
    html_dir = Path("output/card_news/html")
    
    # pending_cardnews.json 로드
    pending_data = {}
    try:
        with open('data/card_news/json/pending_cardnews.json', 'r', encoding='utf-8') as f:
            pending_articles = json.load(f)
            # 제목을 키로 하는 딕셔너리 생성
            for article in pending_articles:
                pending_data[article['title']] = article
    except:
        pending_data = {}
    
    # HTML 파일들에서 정보 추출
    for html_file in html_dir.glob("detail_*.html"):
        filename = html_file.stem
        parts = filename.replace("detail_", "").rsplit("_", 1)
        
        if len(parts) == 2:
            title_part = parts[0].replace("-", " ")
            date_str = parts[1]
            
            # 날짜 파싱
            try:
                if len(date_str) == 8:  # YYYYMMDD
                    date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                else:
                    date = "2025-06-10"
            except:
                date = "2025-06-10"
            
            # pending_cardnews.json에서 매칭되는 기사 찾기
            matched_article = None
            for title_key in pending_data:
                # 제목 유사도 체크 (완전 일치 또는 부분 일치)
                if title_part in title_key or title_key in title_part:
                    matched_article = pending_data[title_key]
                    break
            
            # 카테고리 결정 (키워드 기반)
            category = "general"
            category_name = "일반"
            
            if matched_article and 'keywords' in matched_article:
                keywords = matched_article['keywords']
                
                # 키워드 기반 카테고리 매핑
                if 'ESS' in keywords or '에너지저장' in keywords:
                    category = "ess"
                    category_name = "ESS"
                elif '태양광' in keywords:
                    category = "solar"
                    category_name = "태양광"
                elif 'VPP' in keywords or '가상발전' in keywords:
                    category = "vpp"
                    category_name = "VPP"
                elif '재생에너지' in keywords or '신재생' in keywords:
                    category = "renewable"
                    category_name = "재생에너지"
                elif '정책' in keywords or '기후에너지부' in keywords or '법' in keywords:
                    category = "policy"
                    category_name = "정책"
                elif '전력시장' in keywords or 'SMP' in keywords:
                    category = "market"
                    category_name = "시장"
                elif any(k in keywords for k in ['기술', '개발', '시스템', 'AI']):
                    category = "tech"
                    category_name = "기술"
            
            # 요약 결정
            if matched_article and 'summary' in matched_article:
                summary = matched_article['summary']
            else:
                summary = f"{title_part}에 대한 상세한 분석과 전망을 담은 카드뉴스입니다."
            
            # 제목 정리
            if matched_article and 'title' in matched_article:
                title = matched_article['title']
            else:
                title = title_part
            
            card_news_list.append({
                "title": title,
                "date": date,
                "category": category,
                "category_name": category_name,
                "file_path": f"output/card_news/html/{html_file.name}",
                "summary": summary,
                "source": "전기신문",
                "keywords": matched_article['keywords'] if matched_article else []
            })
    
    # 날짜순 정렬 (최신순)
    card_news_list.sort(key=lambda x: x['date'], reverse=True)
    
    return card_news_list
