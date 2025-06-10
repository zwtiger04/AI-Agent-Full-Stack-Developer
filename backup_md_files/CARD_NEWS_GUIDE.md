# 📸 카드뉴스 GitHub 업로드 & Notion 연동 가이드

## 🚀 빠른 시작

### 1. 환경 설정
`.env` 파일에 GitHub PAT 추가:
```bash
echo "GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx" >> .env
```

### 2. 단일 이미지 업로드
```python
from card_news_uploader import CardNewsUploader

uploader = CardNewsUploader()
image_url = uploader.upload_image_to_github("card_news/images/sample.jpg")
```

### 3. 폴더 전체 업로드 (추천!)
```python
from card_news_uploader import CardNewsUploader

uploader = CardNewsUploader()
uploader.upload_card_news_folder(
    "card_news/images/20250608_전력산업",
    title="2025년 6월 전력산업 동향",
    description="이번 주 전력산업의 주요 이슈를 카드뉴스로 정리했습니다.",
    keywords=["전력산업", "재생에너지", "ESS", "VPP"]
)
```

## 📁 폴더 구조
```
card_news/
├── images/
│   └── 20250608_전력산업/
│       ├── 01_표지.png
│       ├── 02_재생에너지현황.png
│       └── 03_결론.png
└── upload_history.json  # 업로드 기록 자동 저장
```

## 🎨 이미지 파일 규칙
- 지원 형식: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- 파일명은 순서대로 정렬 (01_, 02_ 등 추천)
- 한글 파일명 사용 가능

## 🔗 업로드된 이미지 URL
GitHub에 업로드되면 다음 형식의 URL이 생성됩니다:
```
https://raw.githubusercontent.com/zwtiger04/AI-Agent-Full-Stack-Developer/main/card_news/20250608/image.png
```

## 📝 Notion 페이지 자동 생성
- 현재 주차 데이터베이스에 자동 추가
- 제목: [카드뉴스] + 지정한 제목
- 이미지들이 순서대로 표시
- 키워드 자동 태깅

## 🛠️ 문제 해결
1. **GitHub PAT 오류**: PAT 권한에 `repo` 체크 필요
2. **Notion API 오류**: 데이터베이스 권한 확인
3. **이미지 업로드 실패**: 파일 크기 확인 (100MB 이하)
