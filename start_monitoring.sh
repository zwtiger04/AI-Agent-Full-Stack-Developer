#!/bin/bash
# 🔍 관심 기사 모니터링 백그라운드 실행 스크립트

echo "🚀 관심 기사 모니터링을 백그라운드에서 시작합니다..."

# 기존 프로세스 종료
pkill -f "watch_interested_articles.py"

# 새로 시작
nohup python3 watch_interested_articles.py --interval 300 > logs/monitor.log 2>&1 &

echo "✅ 모니터링이 시작되었습니다!"
echo "📋 로그 확인: tail -f logs/monitor.log"
echo "🛑 종료하려면: pkill -f watch_interested_articles.py"
