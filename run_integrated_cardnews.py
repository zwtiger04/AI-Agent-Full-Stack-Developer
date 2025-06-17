#!/usr/bin/env python3
"""
통합 카드뉴스 시스템 실행 스크립트
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_environment():
    """환경 확인"""
    print("🔍 환경 확인 중...")
    
    # 가상환경 확인
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  가상환경이 활성화되지 않았습니다.")
        print("💡 다음 명령어로 활성화하세요: source venv/bin/activate")
        return False
    
    # 필요 패키지 확인
    required_packages = ['streamlit', 'pandas', 'plotly', 'anthropic']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ 누락된 패키지: {', '.join(missing)}")
        print(f"💡 설치 명령어: pip install {' '.join(missing)}")
        return False
    
    # API 키 확인
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다!")
        return False
    
    if not os.getenv('NOTION_API_KEY'):
        print("⚠️  NOTION_API_KEY가 설정되지 않았습니다. (카드뉴스 생성은 가능)")
    
    print("✅ 환경 확인 완료!")
    return True

def run_integrated_app():
    """통합 앱 실행"""
    print("\n🚀 통합 카드뉴스 시스템 시작...")
    
    # 백그라운드 프로세스 시작
    processes = []
    
    # 1. 관심 기사 모니터링 (선택사항)
    if os.path.exists('watch_interested_articles.py'):
        print("📡 관심 기사 모니터링 시작...")
        monitor_process = subprocess.Popen(
            [sys.executable, 'watch_interested_articles.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(('모니터링', monitor_process))
    
    # 2. Streamlit 앱 실행
    print("🎨 카드뉴스 생성기 UI 시작...")
    
    # 통합 버전이 있으면 사용, 없으면 기본 버전
    app_file = 'card_news_app_integrated.py' if os.path.exists('card_news_app_integrated.py') else 'card_news_app.py'
    
    streamlit_cmd = [
        sys.executable, '-m', 'streamlit', 'run', 
        app_file,
        '--server.port', '8501',
        '--server.address', '0.0.0.0'
    ]
    
    try:
        streamlit_process = subprocess.Popen(streamlit_cmd)
        
        print("\n✨ 시스템이 실행 중입니다!")
        print("🌐 브라우저에서 접속: http://localhost:8501")
        print("⏹️  종료하려면 Ctrl+C를 누르세요.\n")
        
        # 프로세스 대기
        streamlit_process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 시스템 종료 중...")
        
        # 모든 프로세스 종료
        for name, process in processes:
            if process.poll() is None:
                process.terminate()
                print(f"  - {name} 프로세스 종료")
        
        streamlit_process.terminate()
        print("  - Streamlit 종료")
        
        print("✅ 시스템이 안전하게 종료되었습니다.")
    
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)

def main():
    """메인 함수"""
    print("=" * 50)
    print("⚡ 전력산업 카드뉴스 통합 시스템")
    print("📊 분석 대시보드 & 자동 최적화 포함")
    print("=" * 50)
    
    if not check_environment():
        print("\n❌ 환경 설정을 완료한 후 다시 실행하세요.")
        sys.exit(1)
    
    run_integrated_app()

if __name__ == "__main__":
    main()
