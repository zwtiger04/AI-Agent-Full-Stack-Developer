#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Level 2 자동화 시스템 통합 실행기
- 관심 기사 모니터링 + 카드뉴스 생성 UI
"""

import subprocess
import time
import os
import sys
import signal
from pathlib import Path

class Level2Runner:
    """Level 2 시스템 실행 관리자"""
    
    def __init__(self):
        self.processes = []
        self.setup_signal_handlers()
        
    def setup_signal_handlers(self):
        """종료 시그널 처리"""
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
    
    def cleanup(self, signum, frame):
        """프로세스 정리"""
        print("\n\n👋 시스템 종료 중...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        print("✅ 종료 완료")
        sys.exit(0)
    
    def check_requirements(self):
        """시스템 요구사항 확인"""
        print("🔍 시스템 요구사항 확인 중...")
        
        # 1. Python 패키지 확인
        required_packages = ['anthropic', 'streamlit', 'notion_client']
        missing = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✅ {package} 설치됨")
            except ImportError:
                missing.append(package)
                print(f"  ❌ {package} 미설치")
        
        if missing:
            print(f"\n⚠️  필요한 패키지 설치: pip install {' '.join(missing)}")
            return False
        
        # 2. 환경변수 확인
        if not os.getenv('ANTHROPIC_API_KEY'):
            print("\n⚠️  ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
            print("   .env 파일에 추가하거나 export ANTHROPIC_API_KEY=... 실행")
        
        # 3. 디렉토리 확인
        Path("logs").mkdir(exist_ok=True)
        Path("detailed").mkdir(exist_ok=True)
        
        return True
    
    def run_monitoring(self):
        """백그라운드 모니터링 시작"""
        print("\n📊 관심 기사 모니터링 시작...")
        
        # 기존 프로세스 종료
        subprocess.run(['pkill', '-f', 'watch_interested_articles.py'], 
                      capture_output=True)
        
        # 새 프로세스 시작
        process = subprocess.Popen([
            sys.executable, 'watch_interested_articles.py', 
            '--interval', '300'
        ])
        self.processes.append(process)
        
        print("  ✅ 모니터링 프로세스 시작 (PID: {})".format(process.pid))
        return process
    
    def run_streamlit(self):
        """Streamlit UI 실행"""
        print("\n🎨 카드뉴스 생성 UI 시작...")
        
        # Streamlit 프로세스 시작
        process = subprocess.Popen([
            'streamlit', 'run', 'card_news_app.py',
            '--server.port', '8501',
            '--server.address', 'localhost'
        ])
        self.processes.append(process)
        
        print("  ✅ Streamlit 서버 시작 (PID: {})".format(process.pid))
        return process
    
    def display_status(self):
        """시스템 상태 표시"""
        print("\n" + "="*60)
        print("⚡ Level 2 전력산업 카드뉴스 자동화 시스템")
        print("="*60)
        print("\n📊 실행 중인 프로세스:")
        print("  - 관심 기사 모니터링 (5분 간격)")
        print("  - 카드뉴스 생성 UI (http://localhost:8501)")
        print("\n📁 주요 파일:")
        print("  - pending_cardnews.json: 대기 중인 기사")
        print("  - processed_articles.json: 처리 완료 기사")
        print("  - detailed/: 생성된 카드뉴스 저장")
        print("\n🛑 종료하려면 Ctrl+C를 누르세요")
        print("="*60)
    
    def run(self):
        """메인 실행"""
        print("🚀 Level 2 자동화 시스템 시작\n")
        
        # 요구사항 확인
        if not self.check_requirements():
            print("\n❌ 요구사항을 먼저 해결해주세요.")
            return
        
        try:
            # 1. 모니터링 시작
            monitor_process = self.run_monitoring()
            time.sleep(2)
            
            # 2. UI 시작
            ui_process = self.run_streamlit()
            time.sleep(3)
            
            # 3. 상태 표시
            self.display_status()
            
            # 4. 대기
            print("\n🌐 브라우저에서 http://localhost:8501 접속하세요!")
            
            # 프로세스 모니터링
            while True:
                # 프로세스 상태 확인
                if monitor_process.poll() is not None:
                    print("\n⚠️  모니터링 프로세스가 종료되었습니다. 재시작...")
                    monitor_process = self.run_monitoring()
                
                if ui_process.poll() is not None:
                    print("\n⚠️  UI 프로세스가 종료되었습니다. 재시작...")
                    ui_process = self.run_streamlit()
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            self.cleanup(None, None)


def main():
    """메인 함수"""
    # 옵션 파싱
    import argparse
    parser = argparse.ArgumentParser(description='Level 2 자동화 시스템')
    parser.add_argument('--monitor-only', action='store_true', 
                       help='모니터링만 실행')
    parser.add_argument('--ui-only', action='store_true',
                       help='UI만 실행')
    
    args = parser.parse_args()
    
    runner = Level2Runner()
    
    if args.monitor_only:
        print("📊 모니터링만 실행합니다...")
        runner.run_monitoring()
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            runner.cleanup(None, None)
    
    elif args.ui_only:
        print("🎨 UI만 실행합니다...")
        runner.run_streamlit()
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            runner.cleanup(None, None)
    
    else:
        # 전체 실행
        runner.run()


if __name__ == "__main__":
    main()
