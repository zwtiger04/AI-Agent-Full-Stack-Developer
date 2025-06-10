#!/bin/bash
# 🎨 카드뉴스 생성 UI 실행 스크립트

echo "🎨 카드뉴스 생성 UI를 시작합니다..."
echo "📍 브라우저에서 http://localhost:8501 접속"
echo "🛑 종료하려면 Ctrl+C"
echo ""

# Streamlit 실행
streamlit run card_news_app.py --server.port 8501 --server.address localhost
