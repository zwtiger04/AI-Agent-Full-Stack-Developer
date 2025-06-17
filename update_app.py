import re

# 파일 읽기
with open('card_news_app.py', 'r') as f:
    content = f.read()

# 1. 파일명 생성 부분 수정 (test_mode일 때 TEST_ 접두사 추가)
old_filename_line = 'filename = f"detail_{safe_title}_{timestamp}.html"'
new_filename_line = '''filename = f"{'TEST_' if test_mode else ''}detail_{safe_title}_{timestamp}.html"'''
content = content.replace(old_filename_line, new_filename_line)

# 2. 파일 경로 설정 수정 (test_mode일 때 output_test 사용)
old_filepath_line = 'filepath = generator.output_dir / filename'
new_filepath_line = '''filepath = (Path(get_path_str('output_test')) if test_mode else generator.output_dir) / filename'''
content = content.replace(old_filepath_line, new_filepath_line)

# 3. 자동 저장 디렉토리 설정 수정
old_detailed_dir = 'detailed_dir = generator.output_dir'
new_detailed_dir = '''detailed_dir = Path(get_path_str('output_test')) if test_mode else generator.output_dir'''
content = content.replace(old_detailed_dir, new_detailed_dir)

# 4. mark_as_processed 호출 차단
old_mark_processed = '''# 처리 완료 표시
                                            generator.mark_as_processed(article['page_id'])'''
new_mark_processed = '''# 처리 완료 표시
                                            if not test_mode:
                                                generator.mark_as_processed(article['page_id'])'''
content = content.replace(old_mark_processed, new_mark_processed)

# 5. 요약 페이지 추가 차단
old_summary_section = '''# 요약 페이지에 추가
                                    try:
                                        if add_to_summary(article, str(file_path), str(generator.output_dir)):
                                            st.success("📝 요약 페이지에 추가되었습니다!")
                                            update_summary_date()
                                    except Exception as e:
                                        st.warning(f"요약 페이지 업데이트 실패: {e}")'''

new_summary_section = '''# 요약 페이지에 추가
                                    if not test_mode:
                                        try:
                                            if add_to_summary(article, str(file_path), str(generator.output_dir)):
                                                st.success("📝 요약 페이지에 추가되었습니다!")
                                                update_summary_date()
                                        except Exception as e:
                                            st.warning(f"요약 페이지 업데이트 실패: {e}")
                                    else:
                                        st.info("🧪 테스트 모드: 요약 페이지에 추가되지 않습니다.")'''
content = content.replace(old_summary_section, new_summary_section)

# 파일 저장
with open('card_news_app.py', 'w') as f:
    f.write(content)

print("✅ card_news_app.py 수정 완료!")
