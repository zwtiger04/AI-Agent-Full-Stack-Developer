# 💡 다음 대화창용 간단 프롬프트

새 대화창에 아래 내용을 복사해서 시작하세요:

---

전력산업 카드뉴스 시스템 테스트를 진행하려고 합니다.

## 현재 상황
- 위치: WSL Ubuntu `/home/zwtiger/AI-Agent-Full-Stack-Developer`
- 완료: 섹션 시스템 & 분석 대시보드 통합 구현
- 목표: 전체 워크플로우 테스트

## 테스트 단계
1. 신규 뉴스 크롤링
2. 관심 뉴스 체크 (수동)
3. 스트림릿으로 상세 카드뉴스 생성
4. 요약 카드뉴스 연동 확인
5. 템플릿 검토 및 피드백

## 시작 명령어
```bash
cd /home/zwtiger/AI-Agent-Full-Stack-Developer
source venv/bin/activate

# 현재 관심 기사 확인
cat pending_cardnews.json | python3 -m json.tool | head -20

# 필요한 작업 선택:
# 1) 크롤링: python main.py
# 2) 카드뉴스 생성: python3 run_integrated_cardnews.py
```

자세한 내용은 `NEXT_TEST_SESSION_PROMPT.md` 파일을 참고하세요.
