import os
import glob
from datetime import datetime, timedelta

def cleanup_debug_files(max_age_days: int = 7) -> None:
    """
    디버그 파일들을 정리합니다.
    
    Args:
        max_age_days (int): 보관할 최대 일수. 기본값은 7일입니다.
    """
    # 디버그 파일 패턴
    debug_patterns = [
        'debug_article_*.html',
        'debug_*.log',
        'debug_*.txt'
    ]
    
    # 현재 시간
    now = datetime.now()
    
    # 각 패턴에 대해 파일 정리
    for pattern in debug_patterns:
        debug_files = glob.glob(pattern)
        for file_path in debug_files:
            try:
                # 파일 생성 시간 확인
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                age = now - file_time
                
                # max_age_days보다 오래된 파일 삭제
                if age > timedelta(days=max_age_days):
                    os.remove(file_path)
                    print(f"삭제된 디버그 파일: {file_path} (생성일: {file_time.strftime('%Y-%m-%d')})")
            except Exception as e:
                print(f"파일 정리 중 오류 발생 ({file_path}): {str(e)}")

if __name__ == "__main__":
    cleanup_debug_files() 