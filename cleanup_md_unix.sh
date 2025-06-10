#!/bin/bash
# 중복 MD 파일 정리 스크립트
# 실행 전 백업을 권장합니다!

echo "🧹 중복 MD 파일 정리 시작..."
echo "📁 백업 폴더 생성 중..."

# 백업 폴더 생성
mkdir -p backup_md_files
backup_date=$(date +%Y%m%d_%H%M%S)

# 삭제할 파일 목록
files_to_delete=(
    "PROJECT_ANALYSIS.md"
    "AUTOMATION_FLOW_PLAN.md" 
    "LEVEL2_DETAILED_PLAN.md"
    "LEVEL2_USAGE_GUIDE.md"
    "NEXT_SESSION_PROMPT.md"
    "after_public.md"
)

# 백업 후 삭제
for file in "${files_to_delete[@]}"; do
    if [ -f "$file" ]; then
        echo "📦 백업 중: $file"
        cp "$file" "backup_md_files/${file}.backup_${backup_date}"
        echo "🗑️  삭제 중: $file"
        rm "$file"
    fi
done

# PROJECT_CONTEXT.md는 별도 처리 (카드뉴스 디자인 가이드로 변경)
if [ -f "PROJECT_CONTEXT.md" ]; then
    echo "📝 PROJECT_CONTEXT.md를 CARD_NEWS_DESIGN_GUIDE.md로 이름 변경"
    mv PROJECT_CONTEXT.md CARD_NEWS_DESIGN_GUIDE.md
fi

echo "✅ 정리 완료!"
echo ""
echo "📚 남은 MD 파일들:"
echo "  - README.md (프로젝트 소개)"
echo "  - INTEGRATED_PROJECT_GUIDE.md (통합 문서)"
echo "  - CARD_NEWS_QUICK_START.md (카드뉴스 빠른 시작)"
echo "  - CARD_NEWS_DESIGN_GUIDE.md (카드뉴스 디자인 가이드)"
echo "  - GITHUB_PAGES_SETUP.md (GitHub Pages 설정)"
echo ""
echo "💾 백업 파일 위치: backup_md_files/"
