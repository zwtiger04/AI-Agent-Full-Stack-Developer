#!/bin/bash

# NAS 정보 설정
NAS_USER="KJ"  # NAS 사용자 이름으로 변경
NAS_IP="192.168.219.101"  # NAS의 IP 주소로 변경
NAS_PATH="/volume1/homes/KJ/News_Crawler"

# 배포할 파일 목록
FILES_TO_DEPLOY=(
    "main.py"
    "requirements.txt"
    "crawlers/"
    "notion/"
    "utils/"
    "config/"
    "ai_update_content.py"
    "ai_recommender.py"
    ".env.production"
    "run_crawler.sh"
    "Dockerfile"
    "docker-compose.yml"
)

# 배포 전 백업
echo "Creating backup on NAS..."
ssh $NAS_USER@$NAS_IP "cd $NAS_PATH && tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz *"

# Clear target directory on NAS
echo "Clearing target directory on NAS..."
# 이 명령은 사용자 KJ가 NAS에서 'sudo rm'을 비밀번호 없이 실행할 수 있도록 sudoers 파일에 설정되어 있어야 합니다.
ssh $NAS_USER@$NAS_IP "sudo rm -rf $NAS_PATH/*"

# 파일 복사 (scp 사용)
echo "Deploying files to NAS using scp..."
for file in "${FILES_TO_DEPLOY[@]}"; do
    # 디렉토리인지 파일인지 확인 (scp는 디렉토리 복사 시 재귀 옵션 필요)
    if [ -d "$file" ]; then
        scp -r "$file" "$NAS_USER@$NAS_IP:$NAS_PATH/"
    else
        scp "$file" "$NAS_USER@$NAS_IP:$NAS_PATH/"
    fi
done

# NAS에서 Docker 이미지 빌드 및 실행
echo "Building and running Docker container on NAS..."
# Docker Compose 명령은 이미 sudoers 파일에 설정되어 비밀번호 없이 실행 가능합니다.
# PATH 환경 변수를 Docker 실행 파일 경로와 기본 시스템 경로만 포함하도록 설정
ssh $NAS_USER@$NAS_IP "cd $NAS_PATH && export PATH=/usr/local/bin:/bin:/sbin:/usr/bin:/usr/sbin && sudo /usr/local/bin/docker-compose down && sudo /usr/local/bin/docker-compose build --no-cache && sudo /usr/local/bin/docker-compose up -d"

echo "Deployment completed!" 