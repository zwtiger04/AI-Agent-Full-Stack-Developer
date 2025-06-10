# 개선된 AI 콘텐츠 업데이트 모듈
import time
import re
import traceback
import requests
import os
from dotenv import load_dotenv
from googletrans import Translator

# .env 파일에서 환경변수 로드
load_dotenv()

# Ollama API 엔드포인트 설정
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/v1/chat/completions')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'gemma2:9b-instruct-q5_K_M')

# googletrans-py Translator 객체 초기화
translator = Translator()

def clean_article_content(content: str) -> str:
    """기사 내용을 정제합니다."""
    if not content:
        return ""
    
    # 1. 불필요한 공백 제거
    content = ' '.join(content.split())
    
    # 2. 특수문자 처리
    content = content.replace('&nbsp;', ' ')
    
    # 3. 중복된 마침표 제거
    content = content.replace('..', '.')
    
    return content

def extract_key_sentences(content: str, max_sentences: int = 10) -> list:
    """
    🔍 기사에서 중요한 문장들을 추출합니다.
    - 숫자가 포함된 문장 우선
    - 인용문이 포함된 문장
    - 키워드가 포함된 문장
    """
    if not content:
        return []
    
    # 전력산업 관련 중요 키워드
    IMPORTANT_KEYWORDS = [
        '재생에너지', 'VPP', 'ESS', '태양광', '풍력', 
        '전력', 'MW', 'GW', '에너지', '탄소', 
        '정책', '투자', '사업', '계획', '추진'
    ]
    
    # 문장 분리
    sentences = re.split(r'[.!?]\s+', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # 문장 점수 계산
    scored_sentences = []
    for sent in sentences:
        score = 0
        
        # 숫자 포함 시 가중치
        if re.search(r'\d+', sent):
            score += 3
        
        # 인용문 포함 시 가중치
        if '"' in sent or '″' in sent:
            score += 2
        
        # 중요 키워드 포함 시 가중치
        for keyword in IMPORTANT_KEYWORDS:
            if keyword in sent:
                score += 2
                
        # 문장 길이 가중치 (너무 짧거나 긴 문장 패널티)
        if 50 <= len(sent) <= 200:
            score += 1
            
        scored_sentences.append((score, sent))
    
    # 점수 높은 순으로 정렬
    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    
    # 상위 문장들 반환
    return [sent for _, sent in scored_sentences[:max_sentences]]

def generate_enhanced_summary(content: str, use_llm: bool = True) -> str:
    """
    🚀 개선된 한줄 요약 생성
    - 더 구체적인 프롬프트
    - 중요 문장 우선 전달
    - 후처리 강화
    """
    if not use_llm or not content:
        return generate_one_line_summary_rule_based(content)
    
    try:
        # 중요 문장 추출
        key_sentences = extract_key_sentences(content, max_sentences=5)
        key_content = ' '.join(key_sentences) if key_sentences else content[:1000]
        
        # 개선된 프롬프트
        korean_prompt = f"""당신은 전력산업 전문 기자입니다. 다음 기사의 핵심을 한 문장으로 요약하세요.

요약 규칙:
1. 반드시 한국어로만 작성
2. 가장 중요한 정보 포함 (누가, 무엇을, 왜)
3. 구체적인 수치나 규모 포함
4. 100-150자 이내
5. "~다", "~했다"로 끝나는 완전한 문장

기사 핵심 내용:
{key_content}

한줄 요약:"""

        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": "당신은 한국의 전력산업 전문 기자입니다. 오직 한국어로만 답변하세요."},
                    {"role": "user", "content": korean_prompt}
                ],
                "temperature": 0.3,  # 더 일관된 결과를 위해 낮은 온도
                "stream": False
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            summary = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            
            # 후처리: 불필요한 부분 제거
            summary = summary.replace('한줄 요약:', '').replace('요약:', '').strip()
            summary = re.sub(r'^[-•*]\s*', '', summary)  # 불릿 포인트 제거
            
            # 길이 조정
            if len(summary) > 150:
                summary = summary[:147] + '...'
                
            return summary
            
    except Exception as e:
        print(f"[Enhanced Summary] 오류 발생: {str(e)}")
        return generate_one_line_summary_rule_based(content)

def generate_detailed_key_content(content: str, use_llm: bool = True) -> str:
    """
    📊 상세하고 구조화된 핵심 내용 생성
    - 카테고리별 정리
    - 더 많은 정보 포함
    - 읽기 쉬운 구조
    """
    if not use_llm or not content:
        return generate_key_content_rule_based(content)
    
    try:
        # 전체 내용 사용 (2000자까지)
        full_content = content[:2000]
        
        # 구조화된 프롬프트
        korean_prompt = f"""당신은 전력산업 전문 분석가입니다. 다음 기사를 분석하여 핵심 내용을 정리하세요.

분석 형식:
📌 주요 내용
- (가장 중요한 핵심 사실 3-4개)

💡 세부 정보
- (구체적인 수치, 규모, 일정 등)

🔍 배경 및 의미
- (이 소식이 중요한 이유, 업계 영향)

📊 관련 정보
- (추가로 알아야 할 맥락이나 연관 정보)

주의사항:
1. 반드시 한국어로만 작성
2. 각 항목당 2-3문장으로 구체적으로 작성
3. 전문용어는 쉽게 설명
4. 수치와 규모는 정확히 포함

기사 전문:
{full_content}

분석 결과:"""

        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": "당신은 한국의 전력산업 전문가입니다. 전문적이면서도 이해하기 쉽게 설명하세요. 반드시 한국어로만 답변하세요."},
                    {"role": "user", "content": korean_prompt}
                ],
                "temperature": 0.5,  # 창의성과 일관성의 균형
                "max_tokens": 1000,
                "stream": False
            },
            timeout=90  # 더 긴 응답을 위해 타임아웃 증가
        )

        if response.status_code == 200:
            result = response.json()
            key_content = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            
            # 후처리: 형식 정리
            key_content = re.sub(r'\*\*(.+?)\*\*', r'\1', key_content)  # 볼드 제거
            key_content = key_content.replace('분석 결과:', '').strip()
            
            # 이모지가 없으면 추가
            if '📌' not in key_content:
                sections = key_content.split('\n\n')
                if len(sections) >= 1:
                    sections[0] = '📌 주요 내용\n' + sections[0]
                if len(sections) >= 2:
                    sections[1] = '💡 세부 정보\n' + sections[1]
                if len(sections) >= 3:
                    sections[2] = '🔍 배경 및 의미\n' + sections[2]
                key_content = '\n\n'.join(sections)
            
            return key_content[:1900]  # Notion 제한
            
    except Exception as e:
        print(f"[Detailed Content] 오류 발생: {str(e)}")
        return generate_key_content_rule_based(content)

# 기존 함수들 (호환성 유지)
def generate_one_line_summary_rule_based(content: str) -> str:
    """기사 내용의 첫 문장을 추출하여 한 줄로 요약합니다 (규칙 기반)."""
    if not content:
        return ""
    
    sentences = re.split(r'[.?!\n]', content)
    sentences = [s.strip() for s in sentences if s.strip()]
    summary = sentences[0] if sentences else ""
    return summary[:200]

def generate_key_content_rule_based(content: str) -> str:
    """기사 내용의 첫 2~3 문단을 추출하여 핵심 내용으로 사용합니다 (규칙 기반)."""
    if not content:
        return ""
    
    paragraphs = re.split(r'\n{2,}', content)
    key_paragraphs = paragraphs[:3]
    key_content = "\n\n".join(key_paragraphs)
    return key_content[:1000]

# 기존 함수명 유지 (하위 호환성)
def generate_one_line_summary_with_llm(content: str, use_llm: bool = True) -> str:
    """기존 함수명 유지하면서 개선된 함수 호출"""
    return generate_enhanced_summary(content, use_llm)

def generate_key_content(content: str, use_llm: bool = True) -> str:
    """기존 함수명 유지하면서 개선된 함수 호출"""
    return generate_detailed_key_content(content, use_llm)
