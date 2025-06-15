# Memory-simple MCP WSL 경로 문제 해결 가이드

## 문제점
Memory-simple MCP가 Windows에서 실행되면서 WSL 경로(`\\wsl.localhost\\...`)에 접근하지 못하는 문제

## 해결 방법

### 1. Claude Desktop 설정 파일 수정
- 위치: `C:\Users\KJ\AppData\Roaming\Claude\claude_desktop_config.json`
- 변경 내용:
  ```json
  // 기존 (작동 안 함)
  "memory-simple": {
    "args": [
      "--memory-path",
      "\\wsl.localhost\\Ubuntu-22.04\\home\\zwtiger\\.mcp_memory\\memory.jsonl"
    ]
  }
  
  // 변경 후 (작동함)
  "memory-simple": {
    "args": [
      "--memory-path",
      "C:\\Users\\KJ\\.mcp_memory\\memory.jsonl"
    ]
  }
  ```

### 2. 파일 구조 설정
1. Windows에 디렉토리 생성: `C:\Users\KJ\.mcp_memory\`
2. WSL에서 심볼릭 링크 생성:
   ```bash
   ln -s /mnt/c/Users/KJ/.mcp_memory /home/zwtiger/.mcp_memory
   ```

### 3. 데이터 마이그레이션
```bash
# 기존 WSL 데이터를 Windows로 복사
cp /home/zwtiger/.mcp_memory_backup/memory.jsonl /mnt/c/Users/KJ/.mcp_memory/
```

### 4. Claude Desktop 재시작
1. 시스템 트레이에서 Claude 완전 종료
2. Claude Desktop 재시작
3. Memory-simple MCP 정상 작동 확인

## 장점
- Windows와 WSL 양쪽에서 동일한 메모리 파일 접근 가능
- 백업 및 관리 용이
- MCP가 정상적으로 작동

## 참고사항
- 설정 변경 후 반드시 Claude Desktop 재시작 필요
- 심볼릭 링크로 WSL에서도 동일한 경로 사용 가능

---
작성일: 2025-06-12
