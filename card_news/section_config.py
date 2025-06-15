"""
통일된 섹션 설정 모듈
"""
from typing import Dict, List, Optional, Any


class SectionConfig:
    """통일된 섹션 설정 클래스"""
    
    # 모든 섹션 통합 정의 (통일된 구조)
    ALL_SECTIONS = {
        # 필수 섹션들
        'intro': {
            'id': 'intro',
            'name': '타이틀/서론',
            'title': '타이틀/서론',  # 하위 호환성
            'description': '카드뉴스의 시작, 주제 소개',
            'type': 'required',
            'position': 1,
            'style': 'title-intro',
            'icon': '🎯',
            'min_items': 1,
            'max_items': 1
        },
        'conclusion': {
            'id': 'conclusion',
            'name': '전문가 의견/시사점',
            'title': '전문가 의견/시사점',  # 하위 호환성
            'description': '전문가 의견과 미래 시사점',
            'type': 'required',
            'position': 99,
            'style': 'expert-opinion',
            'icon': '💡',
            'min_items': 1,
            'max_items': 1
        },
        
        # 선택 섹션들
        'background': {
            'id': 'background',
            'name': '배경 설명',
            'title': '배경 설명',  # 하위 호환성
            'description': '기술적/정책적 배경 설명',
            'type': 'optional',
            'trigger_words': ['배경', '역사', '발전', '도입', '시작', '기원', '탄생', '과거'],
            'min_items': 3,
            'max_items': 5,
            'style': 'background-section',
            'icon': '📚'
        },
        'technical': {
            'id': 'technical',
            'name': '기술 상세',
            'title': '기술 상세',  # 하위 호환성
            'description': '기술적 세부사항 설명',
            'type': 'optional',
            'trigger_words': ['기술', '시스템', '메커니즘', '원리', '구조', '설계', 'AI', '알고리즘', '효율', 'kW', 'MW', 'GW'],
            'min_items': 3,
            'max_items': 6,
            'style': 'technical-section',
            'icon': '⚙️'
        },
        'comparison': {
            'id': 'comparison',
            'name': '비교 분석',
            'title': '비교 분석',  # 하위 호환성
            'description': '기존 대비 개선점, 타사/타국 비교',
            'type': 'optional',
            'trigger_words': ['비교', '대비', '개선', '차이', '우위', '경쟁', 'vs', '대조'],
            'min_items': 3,
            'max_items': 5,
            'style': 'comparison-section',
            'icon': '📊'
        },
        'statistics': {
            'id': 'statistics',
            'name': '통계/수치',
            'title': '통계/수치',  # 하위 호환성
            'description': '구체적인 숫자와 데이터 제시',
            'type': 'optional',
            'trigger_words': ['통계', '수치', '데이터', '%', '억원', '만원', 'MW', 'GW', '증가', '감소', '성장'],
            'min_items': 3,
            'max_items': 5,
            'style': 'statistics-section',
            'icon': '📈'
        },
        'challenges': {
            'id': 'challenges',
            'name': '도전 과제',
            'title': '도전 과제',  # 하위 호환성
            'description': '현재 직면한 문제점과 과제',
            'type': 'optional',
            'trigger_words': ['문제', '과제', '어려움', '장애', '한계', '리스크', '우려', '걱정'],
            'min_items': 2,
            'max_items': 4,
            'style': 'challenges-section',
            'icon': '⚠️'
        },
        'solutions': {
            'id': 'solutions',
            'name': '해결 방안',
            'title': '해결 방안',  # 하위 호환성
            'description': '문제 해결을 위한 방안 제시',
            'type': 'optional',
            'trigger_words': ['해결', '방안', '대책', '전략', '계획', '추진', '노력', '방법'],
            'min_items': 3,
            'max_items': 5,
            'style': 'solutions-section',
            'icon': '💡'
        },
        'benefits': {
            'id': 'benefits',
            'name': '기대 효과',
            'title': '기대 효과',  # 하위 호환성
            'description': '긍정적 효과와 이점',
            'type': 'optional',
            'trigger_words': ['효과', '이점', '장점', '혜택', '이익', '긍정', '개선', '향상'],
            'min_items': 3,
            'max_items': 5,
            'style': 'benefits-section',
            'icon': '✨'
        },
        'process': {
            'id': 'process',
            'name': '추진 과정',
            'title': '추진 과정',  # 하위 호환성
            'description': '단계별 진행 과정 설명',
            'type': 'optional',
            'trigger_words': ['과정', '단계', '절차', '진행', '프로세스', '추진', '계획', '로드맵'],
            'min_items': 3,
            'max_items': 6,
            'style': 'process-section',
            'icon': '🔄'
        },
        'examples': {
            'id': 'examples',
            'name': '사례 소개',
            'title': '사례 소개',  # 하위 호환성
            'description': '실제 적용 사례나 예시',
            'type': 'optional',
            'trigger_words': ['사례', '예시', '적용', '활용', '실제', '현장', '케이스', '경험'],
            'min_items': 2,
            'max_items': 4,
            'style': 'examples-section',
            'icon': '📝'
        },
        'impact': {
            'id': 'impact',
            'name': '파급 효과',
            'title': '파급 효과',  # 하위 호환성
            'description': '산업/사회적 영향과 파급력',
            'type': 'optional',
            'trigger_words': ['영향', '파급', '변화', '혁신', '전환', '미래', '산업', '사회'],
            'min_items': 2,
            'max_items': 4,
            'style': 'impact-section',
            'icon': '🌊'
        },
        'regulation': {
            'id': 'regulation',
            'name': '정책/규제',
            'title': '정책/규제',  # 하위 호환성
            'description': '관련 정책과 규제 사항',
            'type': 'optional',
            'trigger_words': ['정책', '규제', '법', '제도', '기준', '가이드라인', '정부', '지원'],
            'min_items': 2,
            'max_items': 4,
            'style': 'regulation-section',
            'icon': '📋'
        },
        'policy': {
            'id': 'policy',
            'name': '정책 동향',
            'title': '정책 동향',  # 하위 호환성
            'description': '관련 정책과 정부 동향',
            'type': 'optional',
            'trigger_words': ['정책', '정부', '부처', '계획', '전략', '추진', '발표', '대책'],
            'min_items': 2,
            'max_items': 4,
            'style': 'policy-section',
            'icon': '🏛️'
        },

        'stakeholders': {
            'id': 'stakeholders',
            'name': '이해관계자',
            'title': '이해관계자',  # 하위 호환성
            'description': '관련 기업/기관/단체 소개',
            'type': 'optional',
            'trigger_words': ['기업', '업체', '기관', '단체', '협회', '파트너', '관계자', '참여'],
            'min_items': 2,
            'max_items': 4,
            'style': 'stakeholders-section',
            'icon': '🤝'
        },
        'timeline': {
            'id': 'timeline',
            'name': '추진 일정',
            'title': '추진 일정',  # 하위 호환성
            'description': '시간대별 추진 계획',
            'type': 'optional',
            'trigger_words': ['일정', '계획', '예정', '목표', '년도', '분기', '월', '시기'],
            'min_items': 3,
            'max_items': 5,
            'style': 'timeline-section',
            'icon': '📅'
        },
        'future': {
            'id': 'future',
            'name': '향후 전망',
            'title': '향후 전망',  # 하위 호환성
            'description': '미래 발전 방향과 전망',
            'type': 'optional',
            'trigger_words': ['전망', '미래', '향후', '예측', '기대', '발전', '성장', '확대'],
            'min_items': 2,
            'max_items': 4,
            'style': 'future-section',
            'icon': '🔮'
        },
        'significance': {
            'id': 'significance',
            'name': '의미와 가치',
            'title': '의미와 가치',  # 하위 호환성
            'description': '이 소식의 중요성과 의미',
            'type': 'optional',
            'trigger_words': ['의미', '가치', '중요', '의의', '시사점', '함의', '핵심', '포인트'],
            'min_items': 2,
            'max_items': 3,
            'style': 'significance-section',
            'icon': '⭐'
        }
    }
    
    # 하위 호환성을 위한 속성들
    @property
    def SECTIONS(self):
        """하위 호환성을 위한 프로퍼티"""
        return self.ALL_SECTIONS
    
    @property
    def REQUIRED_SECTIONS(self):
        """하위 호환성을 위한 필수 섹션"""
        # 기존 형식으로 변환 (숫자 키 사용)
        required = {}
        for section_id, section in self.ALL_SECTIONS.items():
            if section.get('type') == 'required':
                position = section.get('position', 1)
                required[position] = {
                    'title': section['title'],
                    'description': section['description'],
                    'position': 'first' if position == 1 else 'last',
                    'style': section['style']
                }
        return required
    
    @property
    def OPTIONAL_SECTIONS(self):
        """하위 호환성을 위한 선택 섹션"""
        optional = {}
        for section_id, section in self.ALL_SECTIONS.items():
            if section.get('type') == 'optional':
                optional[section_id] = section
        return optional
    
    @classmethod
    def get_all_sections(cls) -> Dict[str, Dict]:
        """모든 섹션 정보 반환"""
        return cls.ALL_SECTIONS
    
    @classmethod
    def get_section_info(cls, section_id: str) -> Optional[Dict]:
        """특정 섹션 정보 반환"""
        return cls.ALL_SECTIONS.get(section_id)
    
    @classmethod
    def get_required_sections(cls) -> List[str]:
        """필수 섹션 ID 목록 반환"""
        return [sid for sid, info in cls.ALL_SECTIONS.items() 
                if info.get('type') == 'required']
    
    @classmethod
    def get_optional_sections(cls) -> List[str]:
        """선택 섹션 ID 목록 반환"""
        return [sid for sid, info in cls.ALL_SECTIONS.items() 
                if info.get('type') == 'optional']
    
    @classmethod
    def get_section_by_position(cls, position: int) -> Optional[str]:
        """위치로 섹션 찾기"""
        for sid, info in cls.ALL_SECTIONS.items():
            if info.get('position') == position:
                return sid
        return None
    
    @classmethod
    def get_section_name(cls, section_id: str) -> str:
        """섹션 이름 반환 (안전하게)"""
        section = cls.ALL_SECTIONS.get(section_id, {})
        return section.get('name', section.get('title', section_id))
