# 🚀 GitHub Pages 설정 가이드

## 1️⃣ GitHub Pages 활성화 방법

### 브라우저에서:
1. https://github.com/zwtiger04/AI-Agent-Full-Stack-Developer
2. **Settings** 탭 클릭
3. 왼쪽 메뉴에서 **Pages** 클릭
4. **Source** 섹션에서:
   - Source: `Deploy from a branch` 선택
   - Branch: `main` 선택
   - Folder: `/ (root)` 선택
5. **Save** 버튼 클릭

### 확인 방법:
- 몇 분 후 상단에 녹색 체크와 함께 메시지 표시:
  ```
  ✅ Your site is live at https://zwtiger04.github.io/AI-Agent-Full-Stack-Developer/
  ```

## 2️⃣ 테스트 방법

### GitHub Pages가 활성화되면:
```bash
# 브라우저에서 직접 확인
https://zwtiger04.github.io/AI-Agent-Full-Stack-Developer/card_news/20250608/slide_01.png
```

### 또는 터미널에서:
```bash
curl -I https://zwtiger04.github.io/AI-Agent-Full-Stack-Developer/card_news/20250608/slide_01.png
```

## 3️⃣ 카드뉴스 업로드

### GitHub Pages 활성화 후:
```bash
python3 card_news_uploader_pages.py
```

## 📌 중요 사항

1. **첫 배포는 10분 정도 걸릴 수 있습니다**
2. **이후 업데이트는 1-2분 내 반영됩니다**
3. **Private 리포지토리도 GitHub Pages는 공개됩니다**
4. **card_news 폴더의 이미지만 공개되고 코드는 비공개로 유지됩니다**

## 🔍 문제 해결

### 404 오류가 나는 경우:
1. GitHub Pages가 아직 배포 중입니다 (10분 대기)
2. URL 확인 (대소문자 구분)
3. 파일이 main 브랜치에 있는지 확인

### 이미지가 안 보이는 경우:
1. GitHub Pages URL로 직접 접속해서 확인
2. Notion 새로고침
3. 다른 브라우저에서 테스트
