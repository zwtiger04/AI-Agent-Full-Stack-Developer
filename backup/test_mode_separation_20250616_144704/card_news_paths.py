"""
카드뉴스 경로 관리 모듈
- 절대 경로 vs 상대 경로 문제 해결
- 확장성과 호환성 보장
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional, Union

class CardNewsPaths:
    """
    카드뉴스 파일 경로 관리 클래스
    
    장점:
    1. 절대 경로 사용으로 실행 위치 독립적
    2. 환경 변수로 커스터마이징 가능
    3. 다양한 환경(WSL, Docker, 서버) 지원
    4. 자동 마이그레이션 지원
    """
    
    def __init__(self, custom_root: Optional[Path] = None):
        """
        경로 초기화
        
        Args:
            custom_root: 커스텀 프로젝트 루트 (테스트용)
        """
        # 절대 경로 기반 - 실행 위치와 무관하게 동작
        if custom_root:
            self.PROJECT_ROOT = Path(custom_root).absolute()
        else:
            # __file__ 기반으로 프로젝트 루트 찾기
            self.PROJECT_ROOT = Path(__file__).parent.absolute()
        
        # 환경 변수 체크 (배포 환경 대응)
        if os.getenv('CARDNEWS_ROOT'):
            self.PROJECT_ROOT = Path(os.getenv('CARDNEWS_ROOT')).absolute()
        
        # 경로 설정 로드 또는 생성
        self.config_file = self.PROJECT_ROOT / 'config' / 'paths.json'
        self.paths = self._load_or_create_config()
        
    def _load_or_create_config(self) -> Dict[str, str]:
        """경로 설정 로드 또는 기본값 생성"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # files 섹션과 paths 섹션 병합
                files = config.get('files', {})
                paths = config.get('paths', {})
                
                # output 경로 추가
                if 'output' in paths:
                    files['output_html'] = paths['output'].get('html', '')
                    files['output_images'] = paths['output'].get('images', '')
                
                # logs 경로 추가
                if 'logs' in paths:
                    files['logs'] = paths['logs']
                    
                return files
        
        # 기본 경로 구조
        return self._create_default_paths()
    
    def _create_default_paths(self) -> Dict[str, str]:
        """기본 경로 구조 생성"""
        data_dir = self.PROJECT_ROOT / 'data' / 'card_news'
        output_dir = self.PROJECT_ROOT / 'output' / 'card_news'
        
        # 필수 디렉토리 생성
        (data_dir / 'json').mkdir(parents=True, exist_ok=True)
        (data_dir / 'analytics').mkdir(parents=True, exist_ok=True)
        (output_dir / 'html').mkdir(parents=True, exist_ok=True)
        
        return {
            # JSON 데이터 파일
            'cost_tracking': str(data_dir / 'json' / 'cost_tracking.json'),
            'pending_cardnews': str(data_dir / 'json' / 'pending_cardnews.json'),
            'processed_articles': str(data_dir / 'json' / 'processed_articles.json'),
            'generated_history': str(data_dir / 'json' / 'generated_cardnews_history.json'),
            
            # 분석 데이터
            'section_analytics': str(data_dir / 'analytics' / 'section_analytics.json'),
            
            # 출력 디렉토리
            'output_html': str(output_dir / 'html'),
            'output_images': str(output_dir / 'images'),
            
            # 로그
            'logs': str(self.PROJECT_ROOT / 'logs' / 'card_news')
        }
    
    def get(self, key: str) -> Path:
        """
        경로 가져오기
        
        Args:
            key: 경로 키 (예: 'cost_tracking', 'output_html')
            
        Returns:
            Path 객체
        """
        path_str = self.paths.get(key)
        if not path_str:
            raise KeyError(f"경로 키를 찾을 수 없습니다: {key}")
        
        return Path(path_str)
    
    def get_str(self, key: str) -> str:
        """문자열로 경로 반환"""
        return str(self.get(key))
    
    @property
    def output_dir(self) -> Path:
        """HTML 출력 디렉토리"""
        return self.get('output_html')
    
    @property
    def data_dir(self) -> Path:
        """데이터 디렉토리"""
        return self.get('pending_cardnews').parent
    
    def ensure_directories(self):
        """모든 필수 디렉토리 생성"""
        for key, path_str in self.paths.items():
            path = Path(path_str)
            if path.suffix:  # 파일인 경우
                path.parent.mkdir(parents=True, exist_ok=True)
            else:  # 디렉토리인 경우
                path.mkdir(parents=True, exist_ok=True)
    
    def migrate_legacy_files(self):
        """레거시 파일 자동 마이그레이션"""
        legacy_files = {
            self.PROJECT_ROOT / 'cost_tracking.json': self.get('cost_tracking'),
            self.PROJECT_ROOT / 'pending_cardnews.json': self.get('pending_cardnews'),
            self.PROJECT_ROOT / 'processed_articles.json': self.get('processed_articles'),
            self.PROJECT_ROOT / 'section_analytics.json': self.get('section_analytics')
        }
        
        migrated = []
        for old_path, new_path in legacy_files.items():
            if old_path.exists() and not Path(new_path).exists():
                old_path.rename(new_path)
                migrated.append(old_path.name)
        
        return migrated
    
    def get_windows_accessible_path(self, key: str) -> Optional[str]:
        """Windows에서 접근 가능한 경로 반환 (WSL 환경)"""
        path = self.get(key)
        
        # WSL 경로를 Windows 경로로 변환
        if str(path).startswith('/home/'):
            # /home/user/... -> //wsl$/Ubuntu/home/user/...
            wsl_path = str(path).replace('/home/', '//wsl$/Ubuntu/home/')
            return wsl_path.replace('/', '\\')
        
        return None
    
    def to_dict(self) -> Dict[str, Dict[str, str]]:
        """설정을 딕셔너리로 반환"""
        return {
            'paths': self.paths,
            'project_root': str(self.PROJECT_ROOT),
            'environment': {
                'is_wsl': os.path.exists('/proc/version') and 'microsoft' in open('/proc/version').read().lower(),
                'has_custom_root': bool(os.getenv('CARDNEWS_ROOT'))
            }
        }

# 전역 인스턴스 (싱글톤 패턴)
_paths_instance = None

def get_paths() -> CardNewsPaths:
    """전역 경로 인스턴스 반환"""
    global _paths_instance
    if _paths_instance is None:
        _paths_instance = CardNewsPaths()
        _paths_instance.ensure_directories()
        _paths_instance.migrate_legacy_files()
    return _paths_instance

# 편의 함수들
def get_path(key: str) -> Path:
    """경로 가져오기 편의 함수"""
    return get_paths().get(key)

def get_path_str(key: str) -> str:
    """경로 문자열 가져오기 편의 함수"""
    return get_paths().get_str(key)
