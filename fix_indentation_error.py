# 파일 읽기
with open('card_news_app_integrated.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 문제가 있는 부분 찾기
for i, line in enumerate(lines):
    if "# 사이드바에 테스트 모드 토글 추가" in line:
        # 이 부분부터 with st.sidebar: 블록 끝까지 제거
        start_idx = i
        end_idx = i
        for j in range(i+1, len(lines)):
            if lines[j].strip() and not lines[j].startswith('    '):
                break
            end_idx = j
        
        # 해당 부분 제거
        del lines[start_idx:end_idx+1]
        break

# main() 함수 찾기
main_idx = -1
for i, line in enumerate(lines):
    if "def main():" in line:
        main_idx = i
        break

# main() 함수 내부에 테스트 모드 설정 추가
if main_idx != -1:
    # st.set_page_config 이후 위치 찾기
    for i in range(main_idx, len(lines)):
        if "st.set_page_config" in lines[i]:
            # 다음 빈 줄이나 다음 명령문 찾기
            for j in range(i+1, len(lines)):
                if lines[j].strip() == "" or (lines[j].strip() and not lines[j].strip().startswith('"')):
                    # 여기에 테스트 모드 설정 삽입
                    indent = "    "  # main() 함수 내부 들여쓰기
                    test_mode_code = f'''
{indent}# 테스트 모드 설정
{indent}with st.sidebar:
{indent}    st.markdown("### ⚙️ 설정")
{indent}    test_mode = st.checkbox(
{indent}        "🧪 테스트 모드",
{indent}        help="테스트 모드를 활성화하면 실제 API를 호출하지 않고 더미 카드뉴스를 생성합니다. 비용이 발생하지 않습니다."
{indent}    )
{indent}    if test_mode:
{indent}        st.info("🧪 테스트 모드 활성화됨\\n실제 API 호출 없이 테스트합니다.")
{indent}    st.markdown("---")
'''
                    lines.insert(j, test_mode_code)
                    break
            break

# 파일 쓰기
with open('card_news_app_integrated.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("인덴테이션 오류 수정 완료!")
