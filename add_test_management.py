import re

# 파일 읽기
with open('card_news_app.py', 'r') as f:
    content = f.read()

# 테스트 파일 관리 섹션 추가
test_management_section = '''
        
        # 테스트 파일 관리
        st.subheader("🧪 테스트 파일 관리")
        
        test_dir = Path(get_path_str('output_test'))
        if test_dir.exists():
            test_files = list(test_dir.glob('TEST_*.html'))
            st.info(f"📁 테스트 파일 개수: {len(test_files)}개")
            
            if test_files:
                # 최근 테스트 파일 목록
                st.markdown("**최근 테스트 파일 (최대 5개):**")
                for file in sorted(test_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                    st.text(f"• {file.name}")
                
                # 일괄 삭제 버튼
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ 모든 테스트 파일 삭제", type="secondary"):
                        for file in test_files:
                            file.unlink()
                        st.success(f"✅ {len(test_files)}개의 테스트 파일을 삭제했습니다.")
                        st.rerun()
                
                with col2:
                    # 7일 이상 된 파일 삭제
                    if st.button("🧹 오래된 테스트 파일 정리 (7일 이상)"):
                        import time
                        current_time = time.time()
                        old_files = []
                        for file in test_files:
                            if current_time - file.stat().st_mtime > 7 * 24 * 3600:  # 7일
                                file.unlink()
                                old_files.append(file.name)
                        if old_files:
                            st.success(f"✅ {len(old_files)}개의 오래된 테스트 파일을 삭제했습니다.")
                            st.rerun()
                        else:
                            st.info("7일 이상 된 테스트 파일이 없습니다.")
            else:
                st.success("✨ 테스트 파일이 없습니다.")
        else:
            st.info("🔍 테스트 디렉토리가 아직 생성되지 않았습니다.")'''

# tab4의 마지막 부분 찾기 (tab5 시작 전)
pattern = r'(\s+"""\)\n\n)(\s+with tab5:)'
replacement = r'\1' + test_management_section + r'\n\n\2'
content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

# 파일 저장
with open('card_news_app.py', 'w') as f:
    f.write(content)

print("✅ 테스트 파일 관리 섹션 추가 완료!")
