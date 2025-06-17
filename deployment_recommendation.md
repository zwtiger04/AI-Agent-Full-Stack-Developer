# 배포를 위한 구조 개선 방안

## 1. 요약 페이지를 Streamlit 탭으로 통합
- 별도 HTML 파일 대신 Streamlit 내장
- 동적 업데이트 가능
- 경로 문제 완전 해결

## 2. 정적 파일 서빙
```python
# Streamlit에서 정적 파일 서빙
import streamlit as st
import streamlit.components.v1 as components

# 요약 페이지 표시
def show_summary_page():
    summary_html = generate_summary_html()
    components.html(summary_html, height=800, scrolling=True)
```

## 3. 상대 경로 사용
- 모든 링크를 상대 경로로 변경
- 프로젝트 루트 기준 경로 설정

## 4. 환경 설정 파일
```yaml
# config.yaml
paths:
  output_dir: ./output/card_news
  summary_file: ./output/card_news/summary/index.html
  
# 사용자가 필요시 변경 가능
```
