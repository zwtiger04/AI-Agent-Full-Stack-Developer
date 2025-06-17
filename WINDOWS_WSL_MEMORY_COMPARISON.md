# Windows vs WSL Memory.jsonl 비교 분석

## 🧪 테스트 결과

### 1. 기능 테스트
- **read_graph**: ✅ 정상 작동
- **search_nodes**: ✅ 정상 작동
- **데이터 추가**: ✅ 양방향 동기화 확인

### 2. 성능 비교 (1000회 읽기)
- **Windows 경로**: 3.329초 (NTFS 파일시스템)
- **WSL 경로**: 0.794초 (ext4 파일시스템)
- **성능 차이**: WSL이 약 4.2배 빠름

## 📊 상세 비교

### Windows 경로 (`C:\Users\KJ\.mcp_memory\`)
**장점:**
- ✅ Memory-simple MCP가 직접 접근 가능
- ✅ Windows 앱들과 호환성 좋음
- ✅ 파일 탐색기에서 쉽게 접근
- ✅ Windows 백업 도구 활용 가능
- ✅ 권한 문제 없음 (777)

**단점:**
- ❌ WSL에서 접근 시 성능 저하 (4배 느림)
- ❌ 파일 권한이 모두 열려있음 (보안 취약)
- ❌ 대소문자 구분 없음
- ❌ 심볼릭 링크 제한적

### WSL 경로 (`/home/zwtiger/.mcp_memory/`)
**장점:**
- ✅ 빠른 파일 I/O 성능
- ✅ 적절한 파일 권한 관리 (644)
- ✅ Linux 도구 활용 가능
- ✅ 대소문자 구분
- ✅ 심볼릭 링크 자유로움

**단점:**
- ❌ Windows MCP에서 직접 접근 불가
- ❌ Windows 앱과 호환성 문제
- ❌ Windows 파일 탐색기에서 접근 번거로움
- ❌ WSL 재설치 시 데이터 손실 위험

## 🎯 권장 설정

### 현재 구성 (최적)
```
Windows: C:\Users\KJ\.mcp_memory\memory.jsonl (실제 파일)
    ↕️
WSL: /home/zwtiger/.mcp_memory -> /mnt/c/Users/KJ/.mcp_memory (심볼릭 링크)
```

### 이유
1. **MCP 호환성**: Windows MCP가 정상 작동
2. **접근성**: 양쪽에서 모두 접근 가능
3. **백업**: Windows 백업 도구 활용 가능
4. **관리**: 한 곳에서 중앙 관리

## 💡 사용 팁

### 성능이 중요한 작업
```bash
# WSL 로컬에 임시 복사 후 작업
cp /mnt/c/Users/KJ/.mcp_memory/memory.jsonl /tmp/memory_temp.jsonl
# 작업 수행
# 작업 완료 후 다시 복사
cp /tmp/memory_temp.jsonl /mnt/c/Users/KJ/.mcp_memory/memory.jsonl
```

### 정기 백업
```bash
# cron으로 자동 백업 설정
0 * * * * cp /mnt/c/Users/KJ/.mcp_memory/memory.jsonl /home/zwtiger/.mcp_memory_backup/memory_$(date +\%Y\%m\%d_\%H).jsonl
```

### 파일 무결성 확인
```bash
# 주기적으로 체크섬 확인
md5sum /mnt/c/Users/KJ/.mcp_memory/memory.jsonl > memory.md5
md5sum -c memory.md5
```

## 📝 결론

현재 설정(Windows 저장 + WSL 심볼릭 링크)이 가장 실용적입니다:
- MCP 정상 작동 ✅
- 양쪽 접근 가능 ✅
- 백업 용이 ✅
- 성능은 약간 느리지만 실용적 수준 ✅

---
작성일: 2025-06-12
