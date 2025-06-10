#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 전력산업 카드뉴스 생성기 - Streamlit UI
- 관심 기사를 시각적인 HTML 카드뉴스로 변환
- Claude AI를 활용한 자동 생성
"""

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
import anthropic
from typing import List, Dict, Optional
import re

# 페이지 설정
st.set_page_config(
    page_title="⚡ 전력산업 카드뉴스 생성기",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    .article-card {
        background: #f3f4f6;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 4px solid #3b82f6;
    }
    .keyword-tag {
        background: #e0e7ff;
        color: #3730a3;
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        font-size: 0.875rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


class CardNewsGenerator:
    """카드뉴스 생성 클래스"""
    
    def __init__(self):
        """초기화"""
        self.anthropic_client = None
        self.pending_file = 'pending_cardnews.json'
        self.processed_file = 'processed_articles.json'
        self.output_dir = Path("detailed")
        self.output_dir.mkdir(exist_ok=True)
        
    def setup_api(self, api_key: str):
        """Claude API 설정"""
        try:
            self.anthropic_client = anthropic.Anthropic(api_key=api_key)
            return True
        except Exception as e:
            st.error(f"API 설정 실패: {str(e)}")
            return False
    
    def load_pending_articles(self) -> List[Dict]:
        """대기 중인 기사 로드"""
        try:
            if os.path.exists(self.pending_file):
                with open(self.pending_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"기사 로드 실패: {str(e)}")
        return []
    
    def mark_as_processed(self, page_id: str):
        """처리 완료 표시"""
        # processed_articles.json 업데이트
        processed = []
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r') as f:
                processed = json.load(f)
        
        if page_id not in processed:
            processed.append(page_id)
            
        with open(self.processed_file, 'w') as f:
            json.dump(processed, f, ensure_ascii=False, indent=2)
        
        # pending_cardnews.json에서 제거
        pending = self.load_pending_articles()
        pending = [a for a in pending if a['page_id'] != page_id]
        
        with open(self.pending_file, 'w') as f:
            json.dump(pending, f, ensure_ascii=False, indent=2)
    
    def determine_color_theme(self, article: Dict) -> Dict[str, str]:
        """기사 주제에 따른 색상 테마 자동 결정"""
        keywords = ' '.join(article.get('keywords', [])) + ' ' + article.get('title', '')
        
        if any(kw in keywords for kw in ['ESS', '배터리', '저장']):
            return {
                'primary': '#10b981',  # 초록
                'secondary': '#3b82f6',  # 파랑
                'gradient': 'linear-gradient(135deg, #10b981 0%, #3b82f6 100%)'
            }
        elif any(kw in keywords for kw in ['태양광', '태양', 'PV']):
            return {
                'primary': '#f59e0b',  # 노랑
                'secondary': '#f97316',  # 주황
                'gradient': 'linear-gradient(135deg, #f59e0b 0%, #f97316 100%)'
            }
        elif any(kw in keywords for kw in ['정책', '제도', '법안', '규제']):
            return {
                'primary': '#3b82f6',  # 파랑
                'secondary': '#8b5cf6',  # 보라
                'gradient': 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)'
            }
        elif any(kw in keywords for kw in ['문제', '위기', '도전', '해결']):
            return {
                'primary': '#ef4444',  # 빨강
                'secondary': '#f97316',  # 주황
                'gradient': 'linear-gradient(135deg, #ef4444 0%, #f97316 100%)'
            }
        else:  # 기본값
            return {
                'primary': '#6366f1',  # 인디고
                'secondary': '#8b5cf6',  # 보라
                'gradient': 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)'
            }
    
    def generate_card_news(self, article: Dict, color_theme: Dict, emphasis: List[str]) -> str:
        """Claude API를 통한 카드뉴스 생성"""
        
        # 강조 요소 프롬프트 생성
        emphasis_prompt = ""
        if emphasis:
            emphasis_prompt = f"\n\n특별히 강조할 요소:\n" + "\n".join([f"- {e}" for e in emphasis])
        
        prompt = f"""당신은 전력산업 전문 웹 디자이너입니다. 다음 기사를 기반으로 시각적으로 매력적인 HTML 카드뉴스를 만들어주세요.

[기사 정보]
제목: {article['title']}
요약: {article['summary']}
핵심내용: {article['content']}
키워드: {', '.join(article.get('keywords', []))}
원문 URL: {article.get('url', '')}

[색상 테마]
- 주 색상: {color_theme['primary']}
- 보조 색상: {color_theme['secondary']}
- 그라데이션: {color_theme['gradient']}

[필수 요구사항]
1. 다크 테마 배경 (#0a0a0a)
2. Pretendard 폰트 사용
3. 반응형 디자인 (모바일 최적화)
4. 스크롤 애니메이션 (fadeInUp, slideIn 등)
5. 인터랙티브 요소 (hover 효과, 카운터 애니메이션)
{emphasis_prompt}

[구조]
1. 히어로 섹션: 제목, 날짜, 배경 애니메이션
2. 핵심 인사이트: 3-4개 주요 포인트 (아이콘 포함)
3. 상세 분석: 카드 형태로 정보 구성
4. 데이터 시각화: 관련 통계나 수치 표현
5. 전망/의견: 미래 전망이나 전문가 의견
6. 홈 버튼: 우상단 고정

완전한 HTML 파일을 생성해주세요. CSS는 <style> 태그 안에, JavaScript는 <script> 태그 안에 포함시켜주세요."""

        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=8000
            )
            
            # HTML 추출
            content = response.content[0].text
            
            # HTML 태그가 없으면 기본 구조 추가
            if not content.strip().startswith('<!DOCTYPE') and not content.strip().startswith('<html'):
                content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
</head>
<body>
{content}
</body>
</html>"""
            
            return content
            
        except Exception as e:
            st.error(f"카드뉴스 생성 실패: {str(e)}")
            return None


def main():
    """메인 앱 실행"""
    st.title("⚡ 전력산업 카드뉴스 생성기")
    st.markdown("관심 기사를 아름다운 카드뉴스로 변환합니다 🎨")
    
    # 생성기 초기화
    generator = CardNewsGenerator()
    
    # 사이드바 - API 설정
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # API 키 입력
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            help="Claude API 키를 입력하세요"
        )
        
        if api_key:
            if generator.setup_api(api_key):
                st.success("✅ API 연결 성공!")
            else:
                st.error("❌ API 연결 실패")
        else:
            st.warning("⚠️ API 키를 입력해주세요")
        
        st.divider()
        
        # 새로고침
        if st.button("🔄 기사 목록 새로고침"):
            st.rerun()
        
        # 통계
        st.header("📊 통계")
        pending = generator.load_pending_articles()
        st.metric("대기 중인 기사", f"{len(pending)}개")
    
    # 메인 컨텐츠
    if not api_key:
        st.info("👈 사이드바에서 API 키를 입력해주세요")
        return
    
    # 대기 중인 기사 로드
    articles = generator.load_pending_articles()
    
    if not articles:
        st.info("📭 카드뉴스로 만들 관심 기사가 없습니다.")
        st.markdown("노션에서 관심 있는 기사에 체크하면 여기에 표시됩니다.")
        return
    
    # 탭 생성
    tab1, tab2 = st.tabs(["📰 기사 목록", "📋 생성 기록"])
    
    with tab1:
        st.header("📰 관심 기사 목록")
        
        # 기사 표시
        for idx, article in enumerate(articles):
            with st.expander(f"**{article['title']}**", expanded=False):
                # 키워드 표시
                if article.get('keywords'):
                    keywords_html = ' '.join([
                        f'<span class="keyword-tag">{kw}</span>' 
                        for kw in article['keywords']
                    ])
                    st.markdown(keywords_html, unsafe_allow_html=True)
                
                # 요약
                st.markdown("**📝 요약:**")
                st.write(article['summary'])
                
                # 핵심 내용
                if article.get('content'):
                    st.markdown("**💡 핵심 내용:**")
                    st.text_area("", article['content'], height=150, disabled=True, key=f"content_{idx}")
                
                # 원문 링크
                if article.get('url'):
                    st.markdown(f"[🔗 원문 보기]({article['url']})")
                
                st.divider()
                
                # 생성 옵션
                col1, col2 = st.columns(2)
                
                with col1:
                    # 색상 테마 자동 결정
                    auto_theme = generator.determine_color_theme(article)
                    st.markdown(f"**자동 선택된 색상:**")
                    st.color_picker("주 색상", auto_theme['primary'], key=f"color1_{idx}", disabled=True)
                    st.color_picker("보조 색상", auto_theme['secondary'], key=f"color2_{idx}", disabled=True)
                
                with col2:
                    emphasis = st.multiselect(
                        "강조할 요소",
                        ["📊 차트/그래프", "📅 타임라인", "📋 비교 테이블", 
                         "💬 인용구", "🔢 통계 카운터", "🎯 인포그래픽"],
                        key=f"emphasis_{idx}"
                    )
                
                # 생성 버튼
                if st.button(f"🎨 카드뉴스 생성", key=f"generate_{idx}", type="primary"):
                    with st.spinner("🎨 카드뉴스 생성 중... (30초~1분 소요)"):
                        # 카드뉴스 생성
                        html_content = generator.generate_card_news(
                            article, auto_theme, emphasis
                        )
                        
                        if html_content:
                            st.success("✅ 카드뉴스 생성 완료!")
                            
                            # 미리보기
                            st.markdown("### 👁️ 미리보기")
                            st.components.v1.html(html_content, height=800, scrolling=True)
                            
                            # 저장
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                # 파일명 생성
                                safe_title = re.sub(r'[^\w\s-]', '', article['title'])[:50]
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                filename = f"detail_{safe_title}_{timestamp}.html"
                                filepath = generator.output_dir / filename
                                
                                if st.button("💾 저장", key=f"save_{idx}"):
                                    with open(filepath, 'w', encoding='utf-8') as f:
                                        f.write(html_content)
                                    
                                    st.success(f"✅ 저장 완료: {filename}")
                                    
                                    # 처리 완료 표시
                                    generator.mark_as_processed(article['page_id'])
                                    st.rerun()
                            
                            with col2:
                                # 다운로드
                                st.download_button(
                                    label="📥 다운로드",
                                    data=html_content,
                                    file_name=filename,
                                    mime="text/html",
                                    key=f"download_{idx}"
                                )
                            
                            with col3:
                                if st.button("🔄 다시 생성", key=f"regenerate_{idx}"):
                                    st.rerun()
    
    with tab2:
        st.header("📋 생성 기록")
        
        # 생성된 파일 목록
        if generator.output_dir.exists():
            files = sorted(generator.output_dir.glob("*.html"), key=lambda x: x.stat().st_mtime, reverse=True)
            
            if files:
                for file in files[:20]:  # 최근 20개만 표시
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(f"📄 {file.name}")
                    with col2:
                        if st.button("👁️ 보기", key=f"view_{file.name}"):
                            with open(file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            st.components.v1.html(content, height=800, scrolling=True)
            else:
                st.info("아직 생성된 카드뉴스가 없습니다.")


if __name__ == "__main__":
    main()
