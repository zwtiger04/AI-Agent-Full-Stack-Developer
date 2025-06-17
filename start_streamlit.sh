#!/bin/bash
echo "🚀 Streamlit 카드뉴스 생성 앱 시작 중..."
echo "📍 작업 디렉토리: $(pwd)"
echo ""
echo "⚠️  주의사항:"
echo "1. 카드뉴스 생성 시 기사당 약 $0.555 (750원)의 비용이 발생합니다"
echo "2. 브라우저에서 http://localhost:8501 로 접속하세요"
echo "3. 종료하려면 Ctrl+C를 누르세요"
echo ""

# 가상환경 활성화
source venv/bin/activate

# Streamlit 실행
streamlit run card_news_app.py --server.port 8501

