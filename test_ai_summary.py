#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 AI 요약 기능 테스트 스크립트
한글화 문제를 진단하기 위한 테스트
"""

import sys
sys.path.append('/home/zwtiger/AI-Agent-Full-Stack-Developer')

from ai_update_content import generate_one_line_summary_with_llm, generate_key_content

# 테스트용 기사 내용
test_content = """
한국전력공사는 8일 재생에너지 확대를 위한 새로운 정책을 발표했다. 
이번 정책에는 ESS(에너지저장장치) 설치 지원과 VPP(가상발전소) 구축 계획이 포함되어 있다.
태양광 발전소와 연계한 출력제어 개선 방안도 함께 제시됐다.
전력감독원은 이번 정책이 전력시장 안정화에 기여할 것으로 기대한다고 밝혔다.
"""

print("=" * 60)
print("🧪 AI 요약 기능 테스트")
print("=" * 60)

# 1. LLM 사용 요약 테스트
print("\n1️⃣ LLM 사용 한줄요약 테스트:")
print("-" * 40)
summary_llm = generate_one_line_summary_with_llm(test_content, use_llm=True)
print(f"결과: {summary_llm}")

# 2. 규칙 기반 요약 테스트
print("\n2️⃣ 규칙 기반 한줄요약 테스트:")
print("-" * 40)
summary_rule = generate_one_line_summary_with_llm(test_content, use_llm=False)
print(f"결과: {summary_rule}")

# 3. LLM 사용 핵심 내용 테스트
print("\n3️⃣ LLM 사용 핵심 내용 테스트:")
print("-" * 40)
key_llm = generate_key_content(test_content, use_llm=True)
print(f"결과: {key_llm[:200]}...")  # 처음 200자만 출력

# 4. 규칙 기반 핵심 내용 테스트
print("\n4️⃣ 규칙 기반 핵심 내용 테스트:")
print("-" * 40)
key_rule = generate_key_content(test_content, use_llm=False)
print(f"결과: {key_rule[:200]}...")  # 처음 200자만 출력

print("\n" + "=" * 60)
print("✅ 테스트 완료")
