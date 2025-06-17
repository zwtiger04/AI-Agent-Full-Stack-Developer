# 링크 경로 수정
import re

with open('update_summary.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 파일 경로를 상대 경로로 수정
content = re.sub(
    r"link=f'detailed/{os\.path\.basename\(filepath\)}'",
    r"link=f'detailed/{os.path.basename(filepath)}'",
    content
)

# 파일명 인코딩 문제 해결
content = content.replace(
    "os.path.basename(filepath)",
    "os.path.basename(filepath).replace(' ', '%20')"
)

with open('update_summary.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 링크 오류 수정 완료")
