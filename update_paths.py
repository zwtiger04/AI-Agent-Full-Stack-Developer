import re

# 파일 읽기
with open('card_news_paths.py', 'r') as f:
    content = f.read()

# 첫 번째 수정: 테스트 디렉토리 생성 추가
pattern1 = r"(\(output_dir / 'html'\)\.mkdir\(parents=True, exist_ok=True\))"
replacement1 = r"\1\n        (output_dir / 'test').mkdir(parents=True, exist_ok=True)  # 테스트 디렉토리 추가"
content = re.sub(pattern1, replacement1, content)

# 두 번째 수정: 테스트 경로 추가
pattern2 = r"('output_images': str\(output_dir / 'images'\),)"
replacement2 = r"\1\n            'output_test': str(output_dir / 'test'),  # 테스트 출력 디렉토리 추가"
content = re.sub(pattern2, replacement2, content)

# 파일 저장
with open('card_news_paths.py', 'w') as f:
    f.write(content)

print("✅ card_news_paths.py 수정 완료!")
