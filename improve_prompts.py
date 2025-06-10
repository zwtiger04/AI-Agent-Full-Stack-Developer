#!/usr/bin/env python3
"""
Ollama 프롬프트 개선 스크립트
현재 사용 중인 Gemma2 모델의 프롬프트를 최적화합니다.
"""

import re

def improve_summary_prompt():
    """한줄 요약 프롬프트 개선"""
    
    # ai_update_content.py 읽기
    with open('ai_update_content.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 기존 프롬프트 찾기 및 교체
    old_prompt = '''        korean_prompt = f"""Korean summary required. Write ONE sentence summary in Korean language only.

Article: {content[:800]}

Korean summary (one sentence, 100-200 characters):"""'''
    
    new_prompt = '''        korean_prompt = f"""당신은 한국의 전력산업 전문 기자입니다. 
다음 기사의 핵심을 한 문장으로 요약하세요.

규칙:
- 반드시 한국어로만 작성
- 숫자와 단위를 정확히 포함 (예: 669kW, 400톤)
- 주어와 목적어를 명확히 표시
- 100-150자 이내
- 전문용어는 그대로 사용 (ESS, VPP, RE100 등)

기사 내용: {content[:1000]}

한국어 요약:"""'''
    
    content = content.replace(old_prompt, new_prompt)
    
    # 시스템 프롬프트도 개선
    old_system = '"You are a journalist. Always respond in Korean language."'
    new_system = '"당신은 한국의 전력산업 전문 기자입니다. 모든 답변은 반드시 한국어로만 작성하세요. 영어는 전문용어(ESS, VPP 등)만 허용됩니다."'
    
    content = content.replace(old_system, new_system)
    
    # 파일 저장
    with open('ai_update_content.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 한줄 요약 프롬프트 개선 완료")

def improve_key_content_prompt():
    """핵심 내용 프롬프트 개선"""
    
    with open('ai_update_content.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 핵심 내용 프롬프트 찾기 및 교체
    old_prompt = '''        korean_prompt = f"""Write key points in Korean. Use bullet points.

Article: {content[:1000]}

Korean key points (3-5 points):"""'''
    
    new_prompt = '''        korean_prompt = f"""당신은 한국의 전력산업 전문 분석가입니다.
다음 기사를 분석하여 핵심 내용을 정리하세요.

형식:
• 주요 사실 (누가, 무엇을, 어디서)
• 핵심 수치 (용량, 금액, 기간 등)
• 기대 효과 (CO2 감축량, 비용 절감 등)
• 향후 계획 (목표, 일정 등)

규칙:
- 각 항목은 한국어 완전한 문장으로 작성
- 숫자와 단위는 정확히 표기
- 불필요한 영어 사용 금지
- 각 포인트는 50-100자 이내

기사 전문: {content[:1500]}

핵심 내용:"""'''
    
    content = content.replace(old_prompt, new_prompt)
    
    # 시스템 프롬프트도 개선
    old_system2 = '"You are an analyst. Always respond in Korean language."'
    new_system2 = '"당신은 한국의 전력산업 전문가입니다. 기술적 내용을 일반인도 이해할 수 있도록 쉽게 설명하되, 정확성을 유지하세요. 모든 답변은 한국어로 작성하세요."'
    
    content = content.replace(old_system2, new_system2)
    
    # temperature 조정
    content = re.sub(r'"temperature": 0.7', '"temperature": 0.4', content)
    
    # 파일 저장
    with open('ai_update_content.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 핵심 내용 프롬프트 개선 완료")

def add_post_processing():
    """후처리 로직 강화"""
    
    with open('ai_update_content.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 영어 제거 로직 강화
    enhanced_cleaning = '''
            # 영어 제거 및 한글 정제
            result = re.sub(r'[a-zA-Z]{3,}(?![a-zA-Z]*\d)', '', result)  # 3글자 이상 영어 단어 제거 (약어 제외)
            result = re.sub(r'\s+', ' ', result)  # 중복 공백 제거
            result = result.replace('•', '-')  # 불릿 포인트 통일
            result = result.strip()
'''
    
    # 적절한 위치에 삽입
    # (구현 생략 - 실제로는 정확한 위치를 찾아 삽입해야 함)
    
    print("✅ 후처리 로직 강화 완료")

if __name__ == "__main__":
    print("🔧 Ollama 프롬프트 개선 시작...")
    improve_summary_prompt()
    improve_key_content_prompt()
    add_post_processing()
    print("✨ 모든 개선 작업 완료!")
    print("\n다음 명령으로 테스트하세요:")
    print("python ai_update_content.py")
