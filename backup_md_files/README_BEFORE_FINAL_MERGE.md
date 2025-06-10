# 🔌 AI-Agent-Full-Stack-Developer

전력산업 뉴스 자동 크롤링 및 카드뉴스 생성 시스템

## 🚀 Quick Start

```bash
# 1. 뉴스 크롤링
python main.py

# 2. 카드뉴스 생성 (Level 2)
python3 run_level2.py
```

## 📊 주요 기능

### 1. **뉴스 크롤링** 🔍
- 전기신문 자동 크롤링
- 키워드 필터링 (재생에너지, VPP, ESS 등)
- 노션 데이터베이스 자동 저장

### 2. **AI 요약** 🤖
- 규칙 기반 요약 (기본)
- LLM 기반 요약 (Ollama + Gemma2)
- 사용자 관심 기반 AI 추천

### 3. **카드뉴스 생성** 🎨
- 관심 기사 자동 감지
- Claude API로 HTML 생성
- 비용 관리 ($0.555/기사)

## 📁 프로젝트 구조

```
├── main.py                 # 크롤링 메인
├── run_level2.py          # 카드뉴스 시스템
├── crawlers/              # 크롤러 모듈
├── notion/                # 노션 연동
├── card_news_app.py       # Streamlit UI
└── INTEGRATED_PROJECT_GUIDE.md  # 📌 상세 문서
```

## 🔧 환경 설정

```bash
# .env 파일 필수 설정
NOTION_API_KEY=your_key
NOTION_PARENT_PAGE_ID=2002360b26038007a59fcda976552022
ANTHROPIC_API_KEY=your_claude_key
GITHUB_TOKEN=your_pat
```

## 📚 상세 문서

모든 상세 정보는 [INTEGRATED_PROJECT_GUIDE.md](./INTEGRATED_PROJECT_GUIDE.md)를 참고하세요.

---

## 🔒 보안 주의사항

- **절대 `.env` 파일을 Git에 커밋하지 마세요!**
- API 키는 정기적으로 로테이션하세요.

## 📞 Links

- **GitHub**: [zwtiger04/AI-Agent-Full-Stack-Developer](https://github.com/zwtiger04/AI-Agent-Full-Stack-Developer)
- **전기신문**: [electimes.com](https://www.electimes.com)

---

*최종 업데이트: 2025-06-10*