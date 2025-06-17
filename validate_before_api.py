from dotenv import load_dotenv
load_dotenv()
"""
카드뉴스 생성 전 사전 검증 모듈
API 호출 전에 모든 입력값과 상태를 검증하여 오류를 미리 방지
"""

import json
import os
from typing import Dict, List, Tuple, Optional, Any

class CardNewsValidator:
    """카드뉴스 생성 전 검증 클래스"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_article_structure(self, article: Dict) -> bool:
        """기사 데이터 구조 검증"""
        required_fields = ['page_id', 'title', 'url', 'content']
        missing_fields = []
        
        for field in required_fields:
            if field not in article:
                missing_fields.append(field)
                
        if missing_fields:
            self.errors.append(f"기사 데이터에 필수 필드가 없습니다: {missing_fields}")
            return False
            
        # 필드 타입 검증
        if not isinstance(article.get('page_id'), str):
            self.errors.append("page_id는 문자열이어야 합니다")
            return False
            
        if not article.get('title'):
            self.errors.append("제목이 비어있습니다")
            return False
            
        if not article.get('content'):
            self.errors.append("내용이 비어있습니다")
            return False
            
        return True
        
    def validate_emphasis_sections(self, emphasis: Any) -> Tuple[bool, List]:
        """강조 섹션 데이터 검증 및 정규화"""
        normalized_sections = []
        
        # emphasis가 None인 경우
        if emphasis is None:
            self.warnings.append("강조 섹션이 선택되지 않았습니다")
            return True, []
            
        # 리스트인지 확인
        if not isinstance(emphasis, list):
            self.errors.append(f"emphasis는 리스트여야 합니다. 현재 타입: {type(emphasis)}")
            return False, []
            
        # 각 섹션 검증
        for idx, section in enumerate(emphasis):
            # 문자열인 경우 (섹션 ID만 있는 경우)
            if isinstance(section, str):
                normalized_sections.append(section)
            # 튜플이나 리스트인 경우
            elif isinstance(section, (tuple, list)):
                if len(section) >= 1:
                    normalized_sections.append(section[0])
                else:
                    self.errors.append(f"섹션 {idx}가 비어있습니다")
                    return False, []
            # 딕셔너리인 경우
            elif isinstance(section, dict):
                if 'id' in section:
                    normalized_sections.append(section['id'])
                elif 'section_id' in section:
                    normalized_sections.append(section['section_id'])
                else:
                    self.errors.append(f"섹션 {idx}에 ID가 없습니다")
                    return False, []
            else:
                self.errors.append(f"섹션 {idx}의 형식이 잘못되었습니다: {type(section)}")
                return False, []
                
        return True, normalized_sections
        
    def validate_api_keys(self) -> bool:
        """API 키 존재 여부 검증"""
        if not os.environ.get('ANTHROPIC_API_KEY'):
            self.errors.append("ANTHROPIC_API_KEY가 설정되지 않았습니다")
            return False
        return True
        
    def validate_cost_limit(self, current_cost: float, daily_limit: float = 10.0) -> bool:
        """비용 한도 검증"""
        if current_cost >= daily_limit:
            self.errors.append(f"일일 비용 한도 초과: ${current_cost:.2f} / ${daily_limit:.2f}")
            return False
        return True
        
    def validate_all(self, article: Dict, emphasis: Any, current_daily_cost: float = 0) -> Tuple[bool, Dict]:
        """모든 검증 수행"""
        self.errors = []
        self.warnings = []
        
        # 1. API 키 검증
        api_valid = self.validate_api_keys()
        
        # 2. 기사 구조 검증
        article_valid = self.validate_article_structure(article)
        
        # 3. 강조 섹션 검증 및 정규화
        emphasis_valid, normalized_emphasis = self.validate_emphasis_sections(emphasis)
        
        # 4. 비용 한도 검증
        cost_valid = self.validate_cost_limit(current_daily_cost)
        
        # 결과 반환
        is_valid = api_valid and article_valid and emphasis_valid and cost_valid
        
        result = {
            'valid': is_valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'normalized_emphasis': normalized_emphasis,
            'validation_details': {
                'api_key': api_valid,
                'article_structure': article_valid,
                'emphasis_sections': emphasis_valid,
                'cost_limit': cost_valid
            }
        }
        
        return is_valid, result


def test_validation():
    """검증 기능 테스트"""
    validator = CardNewsValidator()
    
    # 테스트 데이터
    test_article = {
        'page_id': 'test-123',
        'title': '테스트 기사',
        'url': 'https://example.com',
        'content': '테스트 내용'
    }
    
    # 다양한 emphasis 형식 테스트
    test_cases = [
        ['section1', 'section2'],  # 문자열 리스트
        [('section1', 1), ('section2', 2)],  # 튜플 리스트
        [{'id': 'section1'}, {'id': 'section2'}],  # 딕셔너리 리스트
        None,  # None
        'invalid',  # 잘못된 형식
    ]
    
    print("=== 카드뉴스 검증 테스트 ===\n")
    
    for idx, emphasis in enumerate(test_cases):
        print(f"테스트 케이스 {idx + 1}: {emphasis}")
        is_valid, result = validator.validate_all(test_article, emphasis, 5.0)
        print(f"  - 유효성: {is_valid}")
        if result['errors']:
            print(f"  - 오류: {result['errors']}")
        if result['warnings']:
            print(f"  - 경고: {result['warnings']}")
        if is_valid:
            print(f"  - 정규화된 섹션: {result['normalized_emphasis']}")
        print()


if __name__ == "__main__":
    test_validation()
