import streamlit as st
from card_news.section_analytics import SectionAnalytics
import plotly.express as px
import pandas as pd

def create_analytics_dashboard():
    """독립적인 분석 대시보드"""
    
    st.set_page_config(page_title="카드뉴스 분석 대시보드", layout="wide")
    
    analytics = SectionAnalytics()
    
    # 1. 실시간 메트릭
    st.header("📊 실시간 분석 대시보드")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # 메트릭 카드
    with col1:
        st.metric(
            "오늘 생성된 카드뉴스", 
            "12개",
            "+3 vs 어제"
        )
    
    with col2:
        st.metric(
            "평균 정확도",
            "78%",
            "+5%"
        )
    
    # 2. 섹션 성능 히트맵
    st.subheader("🔥 섹션 성능 히트맵")
    
    # 시간대별 섹션 사용 패턴
    patterns = analytics.get_temporal_patterns('hourly')
    df = pd.DataFrame(patterns).T.fillna(0)
    
    fig = px.imshow(df, 
                    labels=dict(x="섹션", y="시간대", color="사용 횟수"),
                    aspect="auto")
    st.plotly_chart(fig, use_container_width=True)
    
    # 3. A/B 테스트 결과
    st.subheader("🧪 A/B 테스트")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**기존 트리거**: '프로세스', '절차'")
        st.metric("평균 점수", "4.2", "-1.3")
        
    with col2:
        st.success("**새 트리거**: '단계별', '실행계획'")
        st.metric("평균 점수", "7.8", "+3.6")
    
    # 4. 실시간 피드백
    st.subheader("💬 실시간 피드백")
    
    # 최근 생성된 카드뉴스의 섹션 점수
    data = analytics.load_data()
    recent = data['selections'][-5:]  # 최근 5개
    
    for selection in recent:
        with st.expander(f"기사 {selection['article_id']} - {selection['timestamp'][:10]}"):
            for section, score in selection['scores'].items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(section)
                with col2:
                    if score >= 8:
                        st.success(f"{score}점")
                    elif score >= 6:
                        st.warning(f"{score}점")
                    else:
                        st.error(f"{score}점")

if __name__ == "__main__":
    create_analytics_dashboard()
