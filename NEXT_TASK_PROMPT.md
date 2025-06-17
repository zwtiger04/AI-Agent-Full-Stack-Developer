# 🔧 전력산업 카드뉴스 생성기 - 남은 작업 가이드

## 📅 작성일: 2025년 6월 11일

## 🎯 해결해야 할 문제점

### 1. **전문가 의견 섹션 구분 문제**
**현재 상황**: 
- 4번 섹션(전문가 의견)과 5번 섹션(시사점 및 향후 전망)이 동일한 expert-quote 스타일 사용
- 시사점 섹션에 전문가 의견 스타일이 잘못 적용됨

**해결 방안**:
- 4번: 기사 내 인용문이나 관계자 발언 (expert-quote 스타일)
- 5번: AI가 분석한 시사점과 전망 (별도 스타일 필요)

**참조할 디폴트 양식**:
```html
<!-- 4번: 전문가 의견 -->
<div class="expert-quote">
    "실제 인용문이나 관계자 발언"
    <p style="text-align: right;">- 발언자 이름/직책</p>
</div>

<!-- 5번: 시사점 및 향후 전망 -->
<div class="section fade-in">
    <h2>🔮 향후 전망</h2>
    <div class="expert-quote">
        "AI가 분석한 전망 내용"
        <p style="text-align: right;">- 에너지 전문가 분석</p>
    </div>
    <div style="margin-top: 40px; padding: 30px; background: rgba(색상, 0.1);">
        <h3>🎯 핵심 시사점</h3>
        <ul>
            <li>✅ 시사점 1</li>
            <li>✅ 시사점 2</li>
        </ul>
    </div>
</div>
```

### 2. **백그라운드 도형 누락**
**누락된 위치**:
- stats-grid 섹션 배경
- timeline 섹션 배경  
- 각 섹션별 장식적 요소

**추가 필요한 스타일**:
```css
.section::before {
    content: '';
    position: absolute;
    /* 섹션별 배경 도형 */
}

.stats-grid::after {
    /* 통계 섹션 배경 효과 */
}

.timeline::before {
    /* 타임라인 장식 라인 */
}
```

### 3. **시사점 내용 생성 문제**
**현재**: 템플릿 문구 그대로 출력
**필요**: 기사 내용 기반 실제 시사점 생성

**프롬프트 개선안**:
```
"기사 내용을 바탕으로 다음을 포함한 시사점을 작성하세요:
1. 이 기사가 업계에 미칠 영향
2. 향후 예상되는 변화
3. 기업/정부가 주목해야 할 점
4. 기술적/정책적 함의"
```

### 4. **요약 페이지 업데이트 실패**
**가능한 원인**:
1. 파일 권한 문제
2. 경로 계산 오류
3. 파일 잠금 상태

**디버깅 방법**:
```python
# 1. 권한 확인
os.access(summary_path, os.W_OK)

# 2. 절대 경로 출력
print(f"절대 경로: {os.path.abspath(summary_path)}")

# 3. 파일 존재 여부
print(f"파일 존재: {os.path.exists(summary_path)}")
```

### 5. **예상 성과 중복 제거**
**현재**: "주요 성과"와 "예상 성과" 중복
**수정**: "예상 성과" → "핵심 시사점"으로 변경

## 🛠️ 수정 우선순위

1. **긴급**: 요약 페이지 업데이트 (파일 권한/경로 문제)
2. **중요**: 전문가 의견과 시사점 섹션 구분
3. **중요**: 시사점 내용 실제 생성
4. **보통**: 백그라운드 도형 추가
5. **보통**: 예상 성과 → 핵심 시사점 변경

## 💡 테스트 방법

1. **요약 페이지 테스트**:
   ```bash
   # 권한 확인
   ls -la /mnt/c/Users/KJ/Desktop/EnhancedCardNews/improved_summary.html
   
   # 수동 테스트
   python3 -c "from update_summary import add_to_summary; print(add_to_summary({'title':'테스트'}, 'test.html', '/mnt/c/Users/KJ/Desktop/EnhancedCardNews/detailed'))"
   ```

2. **스타일 확인**:
   - 생성된 HTML을 브라우저에서 열기
   - 개발자 도구로 CSS 검사
   - 디폴트 양식과 비교

## 🎯 목표

"디폴트 양식(detail_ACEF2025_민관협력_해외성공사례_20d2360b.html)과 
완전히 동일한 품질과 스타일의 카드뉴스 생성"

---
*이 문서를 참조하여 남은 작업을 진행하세요*
