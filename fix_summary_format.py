# 요약 페이지 형식 수정
import fileinput

with open('update_summary.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 카드 형식을 기존과 동일하게 수정
old_card_template = '''<div class="news-card">
                    <span class="category-label {category_class}">{category}</span>
                    <h3>{title}</h3>
                    <p>{summary}</p>
                    <a href="{link}" class="detail-link">자세히 보기 →</a>
                </div>'''

new_card_template = '''<div class="news-card">
                    <span class="category-label {category_class}">{category}</span>
                    <h3>{title}</h3>
                    <p class="description">{summary}</p>
                    <div class="meta-info">
                        <span class="source">전기신문</span>
                        <a href="{link}" class="detail-link">자세히 보기 →</a>
                    </div>
                </div>'''

content = content.replace(old_card_template, new_card_template)

# CSS 스타일도 기존과 맞춤
additional_css = '''
        .meta-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
        }
        
        .source {
            color: #888;
            font-size: 0.9em;
        }
        
        .description {
            margin: 15px 0;
            line-height: 1.6;
        }'''

# CSS 섹션에 추가
content = content.replace('.detail-link:hover {', additional_css + '\n        .detail-link:hover {')

with open('update_summary.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 요약 페이지 형식 수정 완료")
