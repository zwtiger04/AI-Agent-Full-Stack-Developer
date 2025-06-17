"""
카드뉴스 시스템 데코레이터 모듈
작성일: 2025-06-15
목적: 함수 입력값 자동 검증 및 타입 보장
"""

from functools import wraps
from typing import Any, Callable, Dict, List
import logging
import inspect
from .validators import DataValidator, TypeGuard
from .types import Section, Article, ThemeData

logger = logging.getLogger(__name__)

def validate_inputs(func: Callable) -> Callable:
    """입력값 자동 검증 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 함수 시그니처 분석
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        # 각 파라미터 검증
        for param_name, param_value in bound_args.arguments.items():
            # self는 건너뛰기
            if param_name == 'self':
                continue
            
            # 파라미터 타입 힌트 가져오기
            param_annotation = sig.parameters[param_name].annotation
            
            # theme 관련 파라미터 검증
            if param_name in ['theme', 'theme_name', 'color_theme']:
                validated_value = DataValidator.normalize_theme(param_value)
                bound_args.arguments[param_name] = validated_value
                logger.debug(f"Validated {param_name}: {type(param_value).__name__} -> {type(validated_value).__name__}")
            
            # sections 관련 파라미터 검증
            elif param_name in ['sections', 'emphasis', 'selected_sections']:
                if param_value is not None:
                    validated_value = DataValidator.normalize_sections(param_value)
                    bound_args.arguments[param_name] = validated_value
                    logger.debug(f"Normalized {param_name}: {len(validated_value)} sections")
            
            # article 관련 파라미터 검증
            elif param_name == 'article' and isinstance(param_value, dict):
                try:
                    validated_value = DataValidator.validate_article(param_value)
                    bound_args.arguments[param_name] = validated_value
                    logger.debug(f"Validated article: {validated_value.title[:30]}...")
                except ValueError as e:
                    logger.error(f"Article validation failed: {e}")
                    # 원본 유지
            
            # 딕셔너리 키로 사용되는 파라미터
            elif param_name in ['key', 'dict_key', 'section_id']:
                validated_value = DataValidator.sanitize_dict_key(param_value)
                bound_args.arguments[param_name] = validated_value
        
        # 검증된 인자로 함수 호출
        return func(**bound_args.arguments)
    
    return wrapper

def ensure_string_params(*param_names: str) -> Callable:
    """특정 파라미터를 문자열로 보장하는 데코레이터"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            for param_name in param_names:
                if param_name in bound_args.arguments:
                    original_value = bound_args.arguments[param_name]
                    if original_value is not None:
                        bound_args.arguments[param_name] = DataValidator.ensure_string(original_value)
            
            return func(**bound_args.arguments)
        return wrapper
    return decorator

def safe_dict_access(func: Callable) -> Callable:
    """딕셔너리 접근을 안전하게 만드는 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            if "unhashable type" in str(e):
                logger.error(f"Unhashable type error in {func.__name__}: {e}")
                # 기본값 반환 또는 안전한 처리
                sig = inspect.signature(func)
                return_annotation = sig.return_annotation
                
                if return_annotation == str:
                    return ''
                elif return_annotation == dict:
                    return {}
                elif return_annotation == list:
                    return []
                else:
                    return None
            else:
                raise
    return wrapper

def log_type_errors(func: Callable) -> Callable:
    """타입 에러 로깅 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            logger.error(f"TypeError in {func.__name__}: {e}")
            logger.error(f"Args: {args}")
            logger.error(f"Kwargs: {kwargs}")
            raise
    return wrapper

def normalize_section_output(func: Callable) -> Callable:
    """섹션 출력을 정규화하는 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        
        # 결과가 섹션 리스트인 경우 정규화
        if isinstance(result, (list, tuple)):
            try:
                sections = DataValidator.normalize_sections(result)
                # 문자열 리스트로 반환
                return [section.id for section in sections]
            except:
                return result
        
        return result
    return wrapper

# 조합 데코레이터
def fully_validated(func: Callable) -> Callable:
    """모든 검증을 적용하는 통합 데코레이터"""
    @log_type_errors
    @safe_dict_access
    @validate_inputs
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
