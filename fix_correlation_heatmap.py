# card_news/analytics_integration.py 파일 수정
with open('card_news/analytics_integration.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 293번째 줄 근처 수정
for i in range(len(lines)):
    if i >= 290 and i <= 295:
        if 'sections = list(set(s for kw_data in correlation_matrix.values() for s in kw_data.keys()))' in lines[i]:
            lines[i] = '        sections = list(set(s[0] for kw_data in correlation_matrix.values() for s in kw_data))\n'
            print(f"수정됨: {i+1}번째 줄")
    # 298-300번째 줄 근처도 수정
    elif i >= 295 and i <= 305:
        if 'row.append(correlation_matrix.get(keyword, {}).get(section, 0))' in lines[i]:
            lines[i] = '                # 해당 키워드의 섹션 찾기\n'
            lines.insert(i+1, '                value = 0\n')
            lines.insert(i+2, '                kw_sections = correlation_matrix.get(keyword, [])\n')
            lines.insert(i+3, '                for s, score in kw_sections:\n')
            lines.insert(i+4, '                    if s == section:\n')
            lines.insert(i+5, '                        value = score\n')
            lines.insert(i+6, '                        break\n')
            lines.insert(i+7, '                row.append(value)\n')
            print(f"수정됨: {i+1}번째 줄")
            break

# 파일 저장
with open('card_news/analytics_integration.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("수정 완료!")
