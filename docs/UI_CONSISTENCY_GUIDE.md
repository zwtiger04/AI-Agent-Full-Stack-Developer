# 🎨 UI 일관성 유지 가이드

## 📌 핵심 원칙

### 1. **스타일 정의 문서화**
```css
/* 필수 스타일 요소 */
- 배경색: #0f0f0f (다크 테마)
- 주 색상: #667eea (보라)
- 보조 색상: #764ba2 (진한 보라)
- 카드 배경: rgba(255, 255, 255, 0.05)
- 텍스트: #ffffff (메인), #cccccc (서브)
```

### 2. **컴포넌트 재사용**
```python
# styles/card_news_styles.py
DARK_THEME_CSS = """
/* 모든 UI에서 공통으로 사용할 CSS */
"""

def apply_dark_theme():
    st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
```

### 3. **UI 변경 시 체크리스트**
- [ ] 기존 스타일 가이드 확인
- [ ] 스크린샷 비교
- [ ] CSS 클래스명 일치
- [ ] 색상 코드 일치
- [ ] 레이아웃 구조 일치

## 🔒 구현 방식별 가이드

### HTML 직접 사용
```python
# 원본 HTML 그대로 유지
components.html(original_html, height=1200)
```

### Streamlit 재구현
```python
# 반드시 원본 CSS 참조
st.markdown(ORIGINAL_CSS, unsafe_allow_html=True)
```

### 하이브리드 방식
```python
# HTML 구조 + Streamlit 기능
render_with_original_style()
add_streamlit_interactivity()
```

## ⚠️ 금지 사항
1. 스타일 가이드 없이 UI 구현 ❌
2. 기본 Streamlit 테마 사용 ❌
3. CSS 없이 컴포넌트만 사용 ❌

## ✅ 필수 확인 사항
1. 다크 테마 적용 여부
2. 그라디언트 헤더
3. 카드 호버 효과
4. 카테고리별 색상
5. 애니메이션 효과
