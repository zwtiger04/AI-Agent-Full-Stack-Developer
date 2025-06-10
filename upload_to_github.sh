#!/bin/bash
# 카드뉴스 GitHub 업로드 스크립트

cd /home/zwtiger/AI-Agent-Full-Stack-Developer

# Git 추가
git add docs/card_news/
git add /home/zwtiger/AI-Agent-Full-Stack-Developer/docs/card_news/20250608

# 커밋
git commit -m "Add card news for 2025-06-08"

# 푸시
git push origin main

echo "✅ GitHub 업로드 완료!"
echo "📍 GitHub Pages에서 확인: https://zwtiger04.github.io/AI-Agent-Full-Stack-Developer/card_news/20250608/"
