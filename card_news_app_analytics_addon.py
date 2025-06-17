# card_news_app.py에 추가할 코드

# 1. Import 추가 (상단에)
from card_news.section_analytics import SectionAnalytics

# 2. 사이드바에 분석 메뉴 추가
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 분석 도구")
    
    if st.button("📈 섹션 사용 통계"):
        st.session_state.show_analytics = True
    
    if st.button("📋 주간 리포트"):
        st.session_state.show_weekly_report = True

# 3. 메인 화면에 분석 표시 (main() 함수 내)
if 'show_analytics' in st.session_state and st.session_state.show_analytics:
    st.header("📊 카드뉴스 섹션 분석")
    
    analytics = SectionAnalytics()
    
    # 사용 통계
    col1, col2, col3 = st.columns(3)
    
    data = analytics.load_data()
    with col1:
        st.metric("총 카드뉴스", len(data.get('selections', [])))
    
    with col2:
        accuracy = analytics.analyze_selection_accuracy()
        st.metric("시스템 정확도", f"{accuracy['overall_accuracy']*100:.0f}%")
    
    with col3:
        stats = analytics.get_section_usage_stats()
        most_used = max(stats.items(), key=lambda x: x[1]['count'])[0] if stats else "없음"
        st.metric("최다 사용 섹션", most_used)
    
    # 섹션별 사용 현황
    st.subheader("섹션별 사용 현황")
    stats = analytics.get_section_usage_stats()
    
    for section_id, stat in sorted(stats.items(), key=lambda x: x[1]['count'], reverse=True):
        section_name = SectionConfig.OPTIONAL_SECTIONS.get(section_id, {}).get('title', section_id)
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.progress(stat['percentage'] / 100)
            st.text(f"{section_name}")
        with col2:
            st.text(f"{stat['count']}회")
        with col3:
            st.text(f"{stat['percentage']}%")
        with col4:
            if stat['avg_score'] >= 8:
                st.text(f"⭐ {stat['avg_score']}")
            elif stat['avg_score'] >= 6:
                st.text(f"✅ {stat['avg_score']}")
            else:
                st.text(f"⚠️ {stat['avg_score']}")
    
    # 개선 제안
    st.subheader("💡 개선 제안")
    underutilized = analytics.find_underutilized_sections()
    
    for section in underutilized[:5]:
        with st.expander(f"⚠️ {section['section_name']} (사용률: {section['usage_rate']*100:.0f}%)"):
            st.write(f"**권고사항**: {section['recommendation']}")
            if 'avg_score' in section:
                st.write(f"**평균 점수**: {section['avg_score']}점")

# 4. 주간 리포트 표시
if 'show_weekly_report' in st.session_state and st.session_state.show_weekly_report:
    st.header("📋 주간 분석 리포트")
    
    analytics = SectionAnalytics()
    report = analytics.generate_weekly_report()
    
    # 리포트를 다운로드 가능하게
    st.download_button(
        label="📥 리포트 다운로드",
        data=report,
        file_name=f"weekly_report_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown"
    )
    
    # 리포트 내용 표시
    st.markdown(report)
    
    # 차트 생성 및 표시
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = analytics.create_visualization('usage')
        if fig1:
            st.pyplot(fig1)
    
    with col2:
        fig2 = analytics.create_visualization('accuracy')
        if fig2:
            st.pyplot(fig2)
