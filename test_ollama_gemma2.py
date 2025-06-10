#!/usr/bin/env python3
"""Ollama Gemma2 작동 테스트"""

import requests
import json

# Ollama API 설정
OLLAMA_API_URL = 'http://localhost:11434/v1/chat/completions'
OLLAMA_MODEL = 'gemma2:9b-instruct-q5_K_M'

# 테스트 기사
test_content = """
한국전력이 차세대 ESS(에너지저장장치) 개발을 위해 1조원 규모의 투자를 발표했다. 
이번 투자는 재생에너지 확대에 따른 전력망 안정성 확보를 위한 것으로, 
2030년까지 100GWh 규모의 ESS를 구축할 예정이다. 
특히 리튬인산철(LFP) 배터리를 활용한 대용량 ESS 개발에 집중하며, 
AI 기반 운영 최적화 시스템도 함께 도입한다.
"""

print("🧪 Ollama Gemma2 테스트 시작...")
print(f"📍 API URL: {OLLAMA_API_URL}")
print(f"🤖 모델: {OLLAMA_MODEL}")
print("-" * 50)

# 한줄요약 테스트
try:
    print("\n📝 한줄요약 생성 중...")
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": "당신은 전력산업 전문 기자입니다. 기사의 핵심을 정확하고 간결하게 요약해주세요."},
                {"role": "user", "content": f"다음 기사를 100-300자 사이의 한 문장으로 요약해주세요:\n\n{test_content}\n\n한줄요약:"}
            ],
            "stream": False
        },
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        summary = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        print(f"✅ 성공!\n요약: {summary}")
    else:
        print(f"❌ 실패: HTTP {response.status_code}")
        print(f"응답: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ 오류 발생: {str(e)}")

print("\n" + "=" * 50)
print("💡 Ollama가 정상 작동하지 않는다면:")
print("1. Ollama 실행 확인: systemctl status ollama")
print("2. 모델 다운로드: ollama pull gemma2:9b-instruct-q5_K_M")
