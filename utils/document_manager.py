import os
import re
from typing import List, Dict, Any, Set
from datetime import datetime

class DocumentManager:
    def __init__(self):
        self.documents = {
            'README.md': {
                'required_sections': [
                    '## 최근 작업 내역',
                    '## 주요 기능',
                    '## 설치 방법',
                    '## 사용 방법'
                ],
                'keywords_section': '## 주요 키워드'
            },
            'DEVELOPMENT_CONTEXT.md': {
                'required_sections': [
                    '## 최근 작업 내역',
                    '## 프로젝트 개발 컨텍스트 및 규칙',
                    '## 향후 작업 방향'
                ]
            },
            'CODE_DESCRIPTION.md': {
                'required_sections': [
                    '## 최근 업데이트',
                    '## 코드 구조',
                    '## 주요 기능 설명'
                ]
            }
        }
    
    def validate_all(self) -> List[str]:
        """모든 문서의 일관성을 검증"""
        errors = []
        
        # 1. 필수 섹션 존재 여부 확인
        section_errors = self._validate_required_sections()
        errors.extend(section_errors)
        
        # 2. 날짜 일관성 확인
        date_errors = self._validate_dates()
        errors.extend(date_errors)
        
        # 3. 키워드 일관성 확인
        keyword_errors = self._validate_keywords()
        errors.extend(keyword_errors)
        
        # 4. TODO 항목 일관성 확인
        todo_errors = self._validate_todos()
        errors.extend(todo_errors)
        
        return errors
    
    def _validate_required_sections(self) -> List[str]:
        """필수 섹션 존재 여부 확인"""
        errors = []
        for doc_name, doc_info in self.documents.items():
            if not os.path.exists(doc_name):
                errors.append(f"문서가 존재하지 않음: {doc_name}")
                continue
                
            with open(doc_name, 'r', encoding='utf-8') as f:
                content = f.read()
                for section in doc_info['required_sections']:
                    if section not in content:
                        errors.append(f"{doc_name}에 필수 섹션이 없음: {section}")
        return errors
    
    def _validate_dates(self) -> List[str]:
        """문서 간 날짜 일관성 확인"""
        errors = []
        dates = {}
        
        for doc_name in self.documents.keys():
            if not os.path.exists(doc_name):
                continue
                
            with open(doc_name, 'r', encoding='utf-8') as f:
                content = f.read()
                date_match = re.search(r'## 최근 (작업 내역|업데이트) \((\d{4}-\d{2}-\d{2})\)', content)
                if date_match:
                    dates[doc_name] = date_match.group(2)
        
        if len(set(dates.values())) > 1:
            errors.append(f"문서 간 날짜 불일치: {dates}")
        
        return errors
    
    def _validate_keywords(self) -> List[str]:
        """키워드 일관성 확인"""
        errors = []
        keywords = set()
        
        # README.md에서 키워드 추출
        if os.path.exists('README.md'):
            with open('README.md', 'r', encoding='utf-8') as f:
                content = f.read()
                keyword_section = re.search(
                    f"{self.documents['README.md']['keywords_section']}\n\n(.*?)(?=\n\n|$)",
                    content,
                    re.DOTALL
                )
                if keyword_section:
                    keywords = set(line.strip('- ') for line in keyword_section.group(1).split('\n') if line.strip())
        
        # CODE_DESCRIPTION.md의 키워드와 비교
        if os.path.exists('CODE_DESCRIPTION.md'):
            with open('CODE_DESCRIPTION.md', 'r', encoding='utf-8') as f:
                content = f.read()
                code_keywords = set()
                keyword_matches = re.finditer(r'키워드.*?[:：]\s*(.*?)(?=\n|$)', content)
                for match in keyword_matches:
                    code_keywords.update(k.strip() for k in match.group(1).split(','))
                
                if keywords and code_keywords and keywords != code_keywords:
                    errors.append(f"키워드 불일치:\nREADME.md: {keywords}\nCODE_DESCRIPTION.md: {code_keywords}")
        
        return errors
    
    def _validate_todos(self) -> List[str]:
        """TODO 항목 일관성 확인"""
        errors = []
        todos = {}
        
        for doc_name in self.documents.keys():
            if not os.path.exists(doc_name):
                continue
                
            with open(doc_name, 'r', encoding='utf-8') as f:
                content = f.read()
                todo_matches = re.finditer(r'\[TODO\](.*?)(?=\n|$)', content)
                todos[doc_name] = set(match.group(1).strip() for match in todo_matches)
        
        # TODO 항목이 다른 문서에 중복되는지 확인
        for doc1, todos1 in todos.items():
            for doc2, todos2 in todos.items():
                if doc1 != doc2:
                    common_todos = todos1.intersection(todos2)
                    if common_todos:
                        errors.append(f"중복된 TODO 항목 발견:\n{doc1}와 {doc2} 사이:\n{common_todos}")
        
        return errors
    
    def update_document_dates(self, new_date: str = None) -> None:
        """모든 문서의 날짜를 업데이트"""
        if new_date is None:
            new_date = datetime.now().strftime('%Y-%m-%d')
            
        for doc_name in self.documents.keys():
            if not os.path.exists(doc_name):
                continue
                
            with open(doc_name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 날짜 업데이트
            updated_content = re.sub(
                r'(## 최근 (작업 내역|업데이트) \()\d{4}-\d{2}-\d{2}(\))',
                f'\\1{new_date}\\3',
                content
            )
            
            with open(doc_name, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"문서 날짜 업데이트 완료: {doc_name}")

if __name__ == "__main__":
    manager = DocumentManager()
    errors = manager.validate_all()
    if errors:
        print("문서 검증 중 오류 발견:")
        for error in errors:
            print(f"- {error}")
    else:
        print("모든 문서가 일관성 있게 유지되고 있습니다.") 