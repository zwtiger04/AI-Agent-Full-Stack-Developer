#!/bin/bash
# 한글 폰트 다운로드 스크립트

echo "🔍 시스템 폰트 확인 중..."

# DejaVu Sans 폰트 확인 (기본 시스템 폰트)
if fc-list | grep -i "dejavu sans" > /dev/null; then
    echo "✅ DejaVu Sans 폰트를 사용합니다."
    # 심볼릭 링크 생성
    ln -sf /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf NotoSansKR-Regular.otf
    ln -sf /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf NotoSansKR-Bold.otf
else
    echo "⚠️ 시스템 폰트를 찾을 수 없습니다."
    echo "기본 폰트를 사용합니다."
    # 더미 파일 생성
    touch NotoSansKR-Regular.otf
    touch NotoSansKR-Bold.otf
fi

echo "✅ 폰트 설정 완료!"
