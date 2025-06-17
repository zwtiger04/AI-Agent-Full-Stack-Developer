#!/bin/bash
# 카드뉴스 생성 전 안전 체크 스크립트

echo "🔍 카드뉴스 생성 전 안전 체크를 시작합니다..."
echo ""

# Python 환경 활성화
source venv/bin/activate

# 테스트 실행
python3 test_cardnews_safe.py

echo ""
echo "✅ 검증이 완료되었습니다!"
echo ""
echo "다음 단계:"
echo "1. 위 결과에서 모든 기사가 '✅ 검증 통과!'인지 확인하세요"
echo "2. 오류가 있다면 수정 후 다시 실행하세요"
echo "3. 모든 검증이 통과하면 http://localhost:8501 에서 카드뉴스를 생성하세요"
echo ""
echo "💡 팁: 이 스크립트는 실제 API를 호출하지 않으므로 안전합니다!"
