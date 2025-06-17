"""
카드뉴스 시스템 타입 정의
작성일: 2025-06-15
목적: 시스템 전반의 타입 일관성 보장
"""

from typing import Union, List, Tuple, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

# 기본 타입 정의
SectionId = str
SectionScore = int
SectionTuple = Tuple[SectionId, SectionScore]
SectionList = List[SectionId]
MixedSectionData = Union[SectionId, SectionTuple, Dict[str, Any]]

# 테마 타입 정의
ThemeName = str  # 'modern', 'eco', 'tech' 등
ColorTheme = Dict[str, str]  # {'primary': '#...', 'secondary': '#...', 'gradient': '...'}
ThemeData = Union[ThemeName, ColorTheme]

@dataclass
class Section:
    """섹션 데이터 표준 모델"""
    id: str
    score: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_any(cls, data: Any) -> 'Section':
        """어떤 형태의 데이터도 Section 객체로 변환"""
        if isinstance(data, str):
            return cls(id=data, score=0)
        elif isinstance(data, (tuple, list)) and len(data) >= 1:
            # 첫 번째 요소가 리스트인 경우 처리
            section_id = str(data[0]) if not isinstance(data[0], list) else str(data[0][0])
            score = int(data[1]) if len(data) > 1 and isinstance(data[1], (int, float)) else 0
            return cls(id=section_id, score=score)
        elif isinstance(data, dict):
            return cls(
                id=str(data.get('id', data.get('section_id', ''))),
                score=int(data.get('score', 0)),
                metadata=data.get('metadata', {})
            )
        elif isinstance(data, Section):
            return data
        else:
            raise ValueError(f"Cannot convert {type(data).__name__} to Section: {data}")
    
    def to_string(self) -> str:
        """문자열로 변환"""
        return self.id
    
    def to_tuple(self) -> SectionTuple:
        """튜플로 변환"""
        return (self.id, self.score)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'score': self.score,
            'metadata': self.metadata
        }

@dataclass
class Article:
    """기사 데이터 표준 모델"""
    id: str
    title: str
    content: str
    summary: str = ""
    keywords: List[str] = field(default_factory=list)
    url: Optional[str] = None
    date: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Article':
        """딕셔너리에서 Article 객체 생성 (한글 키 지원)"""
        return cls(
            id=str(data.get('id', data.get('page_id', ''))),
            title=str(data.get('title', data.get('제목', ''))),
            content=str(data.get('content', data.get('핵심 내용', ''))),
            summary=str(data.get('summary', data.get('한줄요약', ''))),
            keywords=data.get('keywords', data.get('키워드', [])),
            url=data.get('url', data.get('바로가기', None)),
            date=data.get('date', data.get('날짜', None)),
            metadata={k: v for k, v in data.items() 
                     if k not in ['id', 'page_id', 'title', 'content', 'summary', 
                                  'keywords', 'url', 'date', '제목', '핵심 내용', 
                                  '한줄요약', '키워드', '바로가기', '날짜']}
        )

@dataclass
class GenerationRequest:
    """카드뉴스 생성 요청 표준 모델"""
    article: Article
    theme: ThemeData
    sections: List[Section]
    test_mode: bool = False
    optimization_enabled: bool = False
    
    def get_theme_name(self) -> str:
        """테마 이름 추출"""
        if isinstance(self.theme, str):
            return self.theme
        elif isinstance(self.theme, dict):
            # 색상 기반으로 테마 추론
            primary = self.theme.get('primary', '')
            if primary == '#10b981':
                return 'eco'
            elif primary == '#3b82f6':
                return 'tech'
            else:
                return 'modern'
        else:
            return 'modern'
    
    def get_section_ids(self) -> List[str]:
        """섹션 ID 리스트 반환"""
        return [section.id for section in self.sections]
