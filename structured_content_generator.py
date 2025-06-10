#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 구조화된 콘텐츠 생성기
- 노션 데이터를 구조화된 형태로 분석
- 카드 뉴스용 핵심 인사이트 추출
"""

from typing import Dict, List, Any
from datetime import datetime
import pandas as pd
from collections import Counter
import re

class StructuredContentGenerator:
    """구조화된 콘텐츠를 생성하는 클래스"""
    
    def __init__(self):
        """초기화"""
        self.category_keywords = {
            '태양광': ['태양광', '태양전지', 'PV', '모듈'],
            'ESS': ['ESS', '에너지저장', '배터리', 'BESS'],
            '전력망': ['전력망', '송전', '배전', '계통'],
            '재생에너지': ['재생에너지', '신재생', 'RE100', '탄소중립'],
            'VPP': ['VPP', '가상발전소', '분산자원', 'DR'],
            '정책': ['정책', '법안', '규제', '정부', '전력감독원'],
            '시장': ['전력시장', '전력거래', 'SMP', 'REC']
        }
        
    def analyze_articles(self, articles: List[Dict]) -> Dict[str, Any]:
        """기사 목록을 분석하여 구조화된 데이터 생성
        
        Args:
            articles: 노션에서 가져온 기사 리스트
            
        Returns:
            구조화된 분석 결과
        """
        
        analysis = {
            'summary': self._generate_summary(articles),
            'categories': self._analyze_categories(articles),
            'trends': self._extract_trends(articles),
            'key_insights': self._extract_key_insights(articles),
            'statistics': self._calculate_statistics(articles),
            'top_articles': self._select_top_articles(articles)
        }
        
        return analysis
    
    def _generate_summary(self, articles: List[Dict]) -> Dict[str, Any]:
        """전체 요약 정보 생성"""
        return {
            'total_articles': len(articles),
            'period': self._get_period(articles),
            'main_theme': self._extract_main_theme(articles)
        }
    
    def _analyze_categories(self, articles: List[Dict]) -> Dict[str, int]:
        """카테고리별 기사 분류"""
        category_count = Counter()
        
        for article in articles:
            # 제목과 한줄요약에서 카테고리 추출
            text = f"{article.get('title', '')} {article.get('summary', '')}"
            categories = self._extract_categories(text)
            
            for category in categories:
                category_count[category] += 1
                
        return dict(category_count.most_common())
    
    def _extract_categories(self, text: str) -> List[str]:
        """텍스트에서 카테고리 추출"""
        found_categories = []
        
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    found_categories.append(category)
                    break
                    
        return found_categories if found_categories else ['기타']
    
    def _extract_trends(self, articles: List[Dict]) -> List[Dict[str, str]]:
        """주요 트렌드 추출"""
        trends = []
        
        # 키워드 빈도 분석
        keyword_counter = Counter()
        for article in articles:
            keywords = article.get('keywords', [])
            keyword_counter.update(keywords)
        
        # 상위 5개 트렌드
        for keyword, count in keyword_counter.most_common(5):
            trend = {
                'keyword': keyword,
                'count': count,
                'description': f"{keyword} 관련 이슈가 {count}건 보도됨"
            }
            trends.append(trend)
            
        return trends
    
    def _extract_key_insights(self, articles: List[Dict]) -> List[str]:
        """핵심 인사이트 추출"""
        insights = []
        
        # AI 추천 기사 우선
        ai_recommended = [a for a in articles if a.get('ai_recommend', False)]
        
        if ai_recommended:
            insights.append(f"🤖 AI가 주목한 기사 {len(ai_recommended)}건")
            
        # 관심 표시된 기사
        interested = [a for a in articles if a.get('interest', False)]
        if interested:
            insights.append(f"⭐ 사용자 관심 기사 {len(interested)}건")
            
        # 카테고리별 특징
        categories = self._analyze_categories(articles)
        if categories:
            top_category = list(categories.keys())[0]
            insights.append(f"📊 {top_category} 분야가 가장 활발 ({categories[top_category]}건)")
            
        return insights[:5]  # 최대 5개
    
    def _calculate_statistics(self, articles: List[Dict]) -> Dict[str, Any]:
        """통계 정보 계산"""
        return {
            'total': len(articles),
            'ai_recommended': len([a for a in articles if a.get('ai_recommend', False)]),
            'user_interested': len([a for a in articles if a.get('interest', False)]),
            'avg_keywords': sum(len(a.get('keywords', [])) for a in articles) / max(len(articles), 1)
        }
    
    def _select_top_articles(self, articles: List[Dict], count: int = 3) -> List[Dict]:
        """주요 기사 선정"""
        # 우선순위: 1) 사용자 관심 2) AI 추천 3) 최신
        
        # 관심 표시된 기사
        interested = [a for a in articles if a.get('interest', False)]
        
        # AI 추천 기사
        ai_recommended = [a for a in articles if a.get('ai_recommend', False) and not a.get('interest', False)]
        
        # 나머지 기사 (날짜순)
        others = [a for a in articles if not a.get('interest', False) and not a.get('ai_recommend', False)]
        
        # 합치기
        top_articles = (interested + ai_recommended + others)[:count]
        
        return top_articles
    
    def _get_period(self, articles: List[Dict]) -> str:
        """기사 기간 추출"""
        if not articles:
            return "데이터 없음"
            
        # 날짜 파싱 시도
        dates = []
        for article in articles:
            date_str = article.get('published_date')
            if date_str:
                try:
                    # ISO 형식 날짜 파싱
                    if 'T' in str(date_str):
                        date = datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
                    else:
                        date = datetime.strptime(str(date_str), '%Y-%m-%d')
                    dates.append(date)
                except:
                    pass
                    
        if not dates:
            return datetime.now().strftime("%Y년 %m월")
            
        min_date = min(dates)
        max_date = max(dates)
        
        if min_date.date() == max_date.date():
            return min_date.strftime("%Y년 %m월 %d일")
        else:
            return f"{min_date.strftime('%m/%d')} ~ {max_date.strftime('%m/%d')}"
    
    def _extract_main_theme(self, articles: List[Dict]) -> str:
        """주요 테마 추출"""
        if not articles:
            return "전력산업 동향"
            
        # 가장 많이 언급된 키워드
        keyword_counter = Counter()
        for article in articles:
            keywords = article.get('keywords', [])
            keyword_counter.update(keywords)
            
        if keyword_counter:
            main_keyword = keyword_counter.most_common(1)[0][0]
            return f"{main_keyword} 중심의 전력산업 동향"
        else:
            return "전력산업 종합 동향"


# 테스트용 메인 함수
if __name__ == "__main__":
    # 예시 데이터
    sample_articles = [
        {
            'title': '태양광 발전 효율 20% 향상',
            'summary': '새로운 기술로 태양광 패널 효율성 대폭 개선',
            'keywords': ['태양광', '효율성', '신기술'],
            'ai_recommend': True,
            'interest': False
        },
        {
            'title': 'ESS 화재 안전 기준 강화',
            'summary': '정부, ESS 설치 및 운영 안전 규정 개정',
            'keywords': ['ESS', '안전', '정책'],
            'ai_recommend': False,
            'interest': True
        }
    ]
    
    generator = StructuredContentGenerator()
    analysis = generator.analyze_articles(sample_articles)
    
    print("📊 구조화된 콘텐츠 분석 결과:")
    print(f"요약: {analysis['summary']}")
    print(f"카테고리: {analysis['categories']}")
    print(f"트렌드: {analysis['trends']}")
    print(f"인사이트: {analysis['key_insights']}")
