#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Phase 2: 리소스 관리 Context Manager 클래스들
- WebDriver 안전 관리
- Session 재사용 관리  
- 메모리 모니터링
- 배치 처리 시스템
"""

import os
import gc
import time
import random
import requests
from typing import Optional, Iterator, List, Dict, Any
from contextlib import contextmanager
from datetime import datetime

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ psutil 없음 - 메모리 모니터링 제한적")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️ Selenium 없음 - WebDriver 관리 불가")


class ResourceMonitor:
    """
    🔧 시스템 리소스 모니터링 Context Manager
    
    **특징**:
    - 메모리 사용량 추적
    - 누수 감지 및 경고
    - 가비지 컬렉션 최적화
    """
    
    def __init__(self, warning_threshold_mb: float = 100):
        self.warning_threshold_mb = warning_threshold_mb
        self.start_memory = 0
        self.start_time = 0
    
    def __enter__(self):
        print("📊 리소스 모니터링 시작...")
        
        self.start_time = time.time()
        
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            self.start_memory = process.memory_info().rss
            print(f"🔍 시작 메모리: {self.start_memory / 1024 / 1024:.1f} MB")
        else:
            print("⚠️ psutil 없음 - 메모리 모니터링 제한적")
            
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """리소스 사용량 분석 및 정리"""
        
        # 강제 가비지 컬렉션
        collected = gc.collect()
        print(f"🔄 가비지 컬렉션: {collected}개 객체 정리")
        
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            end_memory = process.memory_info().rss
            diff_mb = (end_memory - self.start_memory) / 1024 / 1024
            
            elapsed_time = time.time() - self.start_time
            
            print(f"📊 종료 메모리: {end_memory / 1024 / 1024:.1f} MB")
            print(f"📈 메모리 변화: {diff_mb:+.1f} MB")
            print(f"⏱️ 실행 시간: {elapsed_time:.1f}초")
            
            # 메모리 누수 경고
            if diff_mb > self.warning_threshold_mb:
                print(f"⚠️ 메모리 누수 의심! 증가량: {diff_mb:.1f} MB")
            elif diff_mb > 0:
                print(f"✅ 정상 메모리 증가: {diff_mb:.1f} MB")
            else:
                print(f"✅ 메모리 효율적 사용: {diff_mb:.1f} MB")


class SessionManager:
    """
    🔧 HTTP Session 재사용 관리 Context Manager
    """
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session: Optional[requests.Session] = None
    
    def __enter__(self):
        print("🌐 HTTP Session 초기화 중...")
        
        self.session = requests.Session()
        
        # 기본 헤더 설정
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        })
        
        print("✅ HTTP Session 초기화 완료")
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """세션 정리"""
        if self.session:
            try:
                self.session.close()
                print("✅ HTTP Session 정상 종료")
            except Exception as e:
                print(f"⚠️ HTTP Session 종료 중 오류: {e}")
            finally:
                self.session = None
