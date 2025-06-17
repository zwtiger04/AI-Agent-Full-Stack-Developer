# WSL에서 Memory-simple MCP 사용하는 방법들

## 방법 1: 기존 Filesystem MCP가 이미 WSL 지원! ⭐

실제로 기본 Filesystem MCP 서버도 WSL 경로를 지원합니다:

```json
{
  "mcpServers": {
    "memory-simple": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-knowledge-graph",
        "--memory-path",
        "\\\\wsl.localhost\\Ubuntu-22.04\\home\\zwtiger\\.mcp_memory\\memory.jsonl"
      ]
    }
  }
}
```

## 방법 2: WSL 전용 MCP 서버 사용 (더 빠른 성능)

`mcp-server-wsl-filesystem`은 네이티브 Linux 명령어를 사용해 더 빠른 성능 제공:

```json
{
  "mcpServers": {
    "wsl-filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-server-wsl-filesystem",
        "--distro=Ubuntu-22.04",
        "/home/zwtiger/.mcp_memory"
      ]
    }
  }
}
```

## 방법 3: 권한 문제 해결

Windows가 WSL 파일에 접근할 때 default user의 권한을 사용합니다.

### 옵션 A: /mnt/wsl 공유 영역 사용
```bash
# WSL에서 실행
sudo mkdir -p /mnt/wsl/mcp_memory
sudo chmod 777 /mnt/wsl/mcp_memory
ln -s /mnt/wsl/mcp_memory /home/zwtiger/.mcp_memory
```

### 옵션 B: 파일 권한 완화
```bash
# WSL에서 실행
chmod 755 /home/zwtiger/.mcp_memory
chmod 644 /home/zwtiger/.mcp_memory/memory.jsonl
```

## 성능 비교

| 방법 | 속도 | 설정 난이도 | 안정성 |
|------|------|------------|--------|
| Windows 로컬 | 느림 (3.3초) | 쉬움 | 높음 |
| WSL (기본 MCP) | 중간 | 중간 | 중간 |
| WSL 전용 MCP | 빠름 (0.8초) | 쉬움 | 높음 |

## 권장 사항

1. **먼저 시도**: 기존 설정을 WSL 경로로 변경
2. **성능 필요시**: WSL 전용 MCP 서버 사용
3. **안정성 우선**: 현재 Windows 경로 유지

