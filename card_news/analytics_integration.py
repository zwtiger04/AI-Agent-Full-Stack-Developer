"""
분석 대시보드 통합 모듈 (Plotly 선택적 지원)
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
import json
from card_news.section_analytics import SectionAnalytics
from card_news.section_config import SectionConfig

# Plotly 선택적 import
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # st.warning은 함수 내에서만 호출되어야 함

class AnalyticsDashboard:
    """Streamlit UI용 분석 대시보드"""
    
    def __init__(self):
        self.analytics = SectionAnalytics()
        self.config = SectionConfig()
    
    def render_mini_dashboard(self, article_keywords: List[str]) -> Dict[str, float]:
        """미니 대시보드 렌더링 (신뢰도 점수 반환)"""
        if not PLOTLY_AVAILABLE:
            # Plotly 없이도 기본 신뢰도 점수는 반환
            return self.analytics.get_section_reliability()
            
        col1, col2 = st.columns(2)
        
        with col1:
            # 섹션별 성과 차트
            section_scores = self.analytics.get_section_performance()
            if section_scores:
                df = pd.DataFrame(
                    list(section_scores.items()),
                    columns=['섹션', '성과지수']
                ).sort_values('성과지수', ascending=True)
                
                fig = px.bar(df, x='성과지수', y='섹션', orientation='h',
                            title='섹션별 성과 지수')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 키워드 관련성
            if article_keywords:
                keyword_relevance = {}
                for keyword in article_keywords[:5]:  # 상위 5개만
                    relevance = self.analytics.get_keyword_relevance(keyword)
                    keyword_relevance[keyword] = relevance
                
                if keyword_relevance:
                    df_keywords = pd.DataFrame(
                        list(keyword_relevance.items()),
                        columns=['키워드', '관련성']
                    )
                    
                    fig = px.pie(df_keywords, values='관련성', names='키워드',
                                title='키워드 관련성')
                    st.plotly_chart(fig, use_container_width=True)
        
        # 신뢰도 점수 반환
        return self.analytics.get_section_reliability()
    
    def render_full_dashboard(self):
        """전체 분석 대시보드 렌더링"""
        st.header("📊 카드뉴스 생성 분석")
        
        if not PLOTLY_AVAILABLE:
            st.warning("📊 차트를 표시하려면 plotly를 설치하세요: `pip install plotly`")
            # 기본 통계만 표시
            stats = self.analytics.get_basic_stats()
            if stats:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("총 생성 수", stats.get('total_generated', 0))
                with col2:
                    st.metric("평균 섹션 수", f"{stats.get('avg_sections', 0):.1f}")
                with col3:
                    st.metric("선호 테마", stats.get('favorite_theme', 'N/A'))
            return
        
        # Plotly가 있을 때의 전체 대시보드
        tabs = st.tabs(["개요", "섹션 분석", "시간대 분석", "품질 피드백"])
        
        with tabs[0]:
            self._render_overview()
        
        with tabs[1]:
            self._render_section_analysis()
        
        with tabs[2]:
            self._render_time_analysis()
        
        with tabs[3]:
            self._render_quality_feedback()
    
    def _render_overview(self):
        """개요 탭 렌더링"""
        if not PLOTLY_AVAILABLE:
            return
            
        stats = self.analytics.get_basic_stats()
        
        if not stats:
            st.info("아직 데이터가 없습니다.")
            return
        
        # 기본 메트릭
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 생성 수", stats['total_generated'])
        
        with col2:
            st.metric("오늘 생성", stats['today_generated'])
        
        with col3:
            st.metric("평균 섹션 수", f"{stats['avg_sections']:.1f}")
        
        with col4:
            st.metric("선호 테마", stats['favorite_theme'])
        
        # 일별 생성 추이
        daily_stats = self.analytics.get_daily_stats()
        if daily_stats:
            df_daily = pd.DataFrame(daily_stats)
            fig = px.line(df_daily, x='date', y='count', 
                         title='일별 카드뉴스 생성 추이',
                         markers=True)
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_section_analysis(self):
        """섹션 분석 탭 렌더링"""
        if not PLOTLY_AVAILABLE:
            return
            
        col1, col2 = st.columns(2)
        
        with col1:
            # 섹션 사용 빈도
            section_usage = self.analytics.get_section_usage()
            if section_usage:
                df = pd.DataFrame(
                    list(section_usage.items()),
                    columns=['섹션', '사용 횟수']
                ).sort_values('사용 횟수', ascending=False)
                
                fig = px.bar(df, x='섹션', y='사용 횟수',
                            title='섹션별 사용 빈도')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 섹션 조합 분석
            combinations = self.analytics.get_section_combinations()
            if combinations:
                top_combos = sorted(combinations.items(), 
                                  key=lambda x: x[1], 
                                  reverse=True)[:10]
                
                combo_names = [' + '.join(combo[0]) for combo in top_combos]
                combo_counts = [combo[1] for combo in top_combos]
                
                fig = px.pie(values=combo_counts, names=combo_names,
                            title='인기 섹션 조합 TOP 10')
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_time_analysis(self):
        """시간대 분석 탭 렌더링"""
        if not PLOTLY_AVAILABLE:
            return
            
        # 시간대별 생성 패턴
        hourly_stats = self.analytics.get_hourly_stats()
        if hourly_stats:
            df_hourly = pd.DataFrame(hourly_stats)
            fig = px.bar(df_hourly, x='hour', y='count',
                        title='시간대별 생성 패턴')
            st.plotly_chart(fig, use_container_width=True)
        
        # 요일별 패턴
        weekly_stats = self.analytics.get_weekly_stats()
        if weekly_stats:
            df_weekly = pd.DataFrame(weekly_stats)
            fig = px.bar(df_weekly, x='weekday', y='count',
                        title='요일별 생성 패턴')
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_quality_feedback(self):
        """품질 피드백 탭 렌더링"""
        if not PLOTLY_AVAILABLE:
            st.info("품질 평가 데이터를 표시하려면 plotly가 필요합니다.")
            return
            
        feedback_data = self.analytics.get_quality_feedback_summary()
        
        if not feedback_data:
            st.info("아직 품질 평가 데이터가 없습니다.")
            return
        
        # 전체 만족도
        avg_rating = feedback_data.get('average_rating', 0)
        st.metric("평균 만족도", f"{avg_rating:.1f} / 10")
        
        # 섹션별 평가
        section_ratings = feedback_data.get('section_ratings', {})
        if section_ratings:
            df_ratings = pd.DataFrame(
                list(section_ratings.items()),
                columns=['섹션', '평균 평점']
            ).sort_values('평균 평점', ascending=False)
            
            fig = px.bar(df_ratings, x='섹션', y='평균 평점',
                        title='섹션별 평균 평점',
                        color='평균 평점',
                        color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
    
    def get_optimized_sections(self, 
                              article_keywords: List[str], 
                              selected_sections: List[str],
                              num_sections: int = 5) -> Tuple[List[str], str]:
        """AI 기반 섹션 최적화"""
        try:
            # 키워드 기반 추천
            keyword_sections = set()
            for keyword in article_keywords:
                related = self.analytics.get_keyword_related_sections(keyword)
                keyword_sections.update(related[:2])  # 키워드당 상위 2개
            
            # 성과 기반 추천
            performance = self.analytics.get_section_performance()
            top_performers = sorted(performance.items(), 
                                  key=lambda x: x[1], 
                                  reverse=True)
            
            # 신뢰도 기반 필터링
            reliability = self.analytics.get_section_reliability()
            
            # 최종 선택
            optimized = []
            reasons = []
            
            # 1. 사용자 선택 중 신뢰도 높은 것
            for section in selected_sections:
                if reliability.get(section, 0) > 0.7:
                    optimized.append(section)
                    reasons.append(f"{section}: 사용자 선택 + 높은 신뢰도")
            
            # 2. 키워드 관련 섹션
            for section in keyword_sections:
                if section not in optimized and len(optimized) < num_sections:
                    optimized.append(section)
                    reasons.append(f"{section}: 키워드 관련성")
            
            # 3. 고성과 섹션
            for section, score in top_performers:
                if section not in optimized and len(optimized) < num_sections:
                    optimized.append(section)
                    reasons.append(f"{section}: 높은 성과 지수")
            
            # 4. 필수 섹션 확인
            if 'intro' not in optimized:
                optimized.insert(0, 'intro')
                reasons.insert(0, "intro: 필수 섹션")
            
            if 'conclusion' not in optimized and len(optimized) < num_sections:
                optimized.append('conclusion')
                reasons.append("conclusion: 필수 섹션")
            
            # 이유 설명 생성
            reason_text = "AI 최적화 이유:\\n" + "\\n".join(reasons[:5])
            
            return optimized[:num_sections], reason_text
            
        except Exception as e:
            # 오류 시 기본값 반환
            st.error(f"최적화 중 오류: {e}")
            return selected_sections[:num_sections], "최적화 실패 - 사용자 선택 유지"
    
    def render_quality_feedback(self, article_id: str):
        """품질 피드백 UI 렌더링"""
        st.subheader("📝 품질 평가")
        
        with st.form(f"feedback_{article_id}"):
            # 전체 만족도
            overall = st.slider("전체 만족도", 1, 10, 7)
            
            # 섹션별 평가
            st.write("섹션별 평가:")
            section_ratings = {}
            
            cols = st.columns(3)
            sections = list(self.config.ALL_SECTIONS.keys())
            
            for i, section in enumerate(sections):
                with cols[i % 3]:
                    rating = st.slider(
                        self.config.ALL_SECTIONS[section]['name'],
                        1, 10, 5,
                        key=f"rating_{article_id}_{section}"
                    )
                    section_ratings[section] = rating
            
            # 피드백 저장
            if st.form_submit_button("평가 저장"):
                self.analytics.save_quality_feedback(
                    article_id,
                    overall,
                    section_ratings
                )
                st.success("평가가 저장되었습니다!")


def extend_section_analytics():
    """SectionAnalytics 클래스 확장"""
    
    def save_quality_feedback(self, article_id: str, overall_rating: int, 
                            section_ratings: Dict[str, int]):
        """품질 피드백 저장"""
        feedback_file = "feedback/quality_feedback.json"
        
        try:
            with open(feedback_file, 'r', encoding='utf-8') as f:
                feedback_data = json.load(f)
        except:
            feedback_data = []
        
        feedback_data.append({
            'article_id': article_id,
            'timestamp': datetime.now().isoformat(),
            'overall_rating': overall_rating,
            'section_ratings': section_ratings
        })
        
        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, ensure_ascii=False, indent=2)
    
    def get_section_reliability(self) -> Dict[str, float]:
        """섹션별 신뢰도 점수 계산"""
        feedback_file = "feedback/quality_feedback.json"
        
        try:
            with open(feedback_file, 'r', encoding='utf-8') as f:
                feedback = json.load(f)
        except:
            feedback = []
        
        if not feedback:
            # 기본 신뢰도
            return {section: 0.5 for section in self.config.ALL_SECTIONS.keys()}
        
        # 평균 평점 계산
        section_scores = {}
        section_counts = {}
        
        for fb in feedback:
            overall = fb.get('overall_rating', 7)
            for section, rating in fb.get('section_ratings', {}).items():
                if section not in section_scores:
                    section_scores[section] = 0
                    section_counts[section] = 0
                
                # 전체 평점과 섹션 평점의 가중 평균
                weighted_score = (rating * 0.7 + overall * 0.3) / 10
                section_scores[section] += weighted_score
                section_counts[section] += 1
        
        reliability = {}
        for section in self.config.ALL_SECTIONS.keys():
            if section in section_counts and section_counts[section] > 0:
                reliability[section] = section_scores[section] / section_counts[section]
            else:
                reliability[section] = 0.5  # 기본값
        
        return reliability
    
    # 메서드 주입
    SectionAnalytics.save_quality_feedback = save_quality_feedback
    SectionAnalytics.get_section_reliability = get_section_reliability


# 모듈 로드 시 자동으로 확장
extend_section_analytics()

# 호환성을 위한 함수
def get_analytics_handler():
    """분석 핸들러 반환 (호환성 유지)"""
    if PLOTLY_AVAILABLE:
        return AnalyticsDashboard()
    else:
        return None
