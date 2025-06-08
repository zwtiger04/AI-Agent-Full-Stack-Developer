import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os
from notion.notion_client import NotionClient

MODEL_PATH = 'feedback/ai_recommend_model.joblib'
VECTORIZER_PATH = 'feedback/ai_recommend_vectorizer.joblib'

def fit_and_save_model(notion_client: NotionClient = None):
    """관심/비관심 기사로 AI 추천 모델 학습 및 저장
    
    Args:
        notion_client: NotionClient 인스턴스. None이면 새로 생성
    """
    try:
        if notion_client is None:
            notion_client = NotionClient()
        
        # 1. 모든 주차의 관심 기사 가져오기
        interested_articles = notion_client.get_interested_articles()
        if not interested_articles:
            print("관심 기사가 없어 모델 학습을 건너뜁니다.")
            return
        
        # 2. 데이터프레임 생성
        df = pd.DataFrame(interested_articles)
        
        # 3. 텍스트 feature 생성
        for col in ['title', 'summary', 'content']:
            if col not in df.columns:
                df[col] = ''
        df['text'] = df['title'].fillna('') + ' ' + df['summary'].fillna('') + ' ' + df['content'].fillna('')
        
        # 4. 학습 데이터 준비
        X = df['text']
        y = df['interest'].astype(int)
        
        # 5. 모델 학습
        vectorizer = TfidfVectorizer(max_features=1000)
        X_vec = vectorizer.fit_transform(X)
        model = LogisticRegression(max_iter=200, class_weight='balanced')
        model.fit(X_vec, y)
        
        # 6. 모델 저장
        os.makedirs('feedback', exist_ok=True)
        joblib.dump(model, MODEL_PATH)
        joblib.dump(vectorizer, VECTORIZER_PATH)
        print(f"모델 및 벡터라이저 저장 완료: {MODEL_PATH}, {VECTORIZER_PATH}")
        print(f"학습된 데이터 수: {len(df)}개")
        
    except Exception as e:
        print(f"모델 학습 중 오류 발생: {str(e)}")
        import traceback
        print(traceback.format_exc())

def predict_ai_recommend(articles):
    """새 기사 리스트에 대해 AI추천 예측 결과를 반환"""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise RuntimeError('모델이 학습되어 있지 않습니다. fit_and_save_model을 먼저 실행하세요.')
    
    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        
        # 텍스트 feature 생성
        texts = []
        for article in articles:
            text = ' '.join([
                article.get('title', ''),
                article.get('summary', ''),
                article.get('content', '')
            ])
            texts.append(text)
        
        # 예측
        X_vec = vectorizer.transform(texts)
        preds = model.predict(X_vec)
        
        # 결과 반환
        results = []
        for i, article in enumerate(articles):
            results.append({
                'title': article.get('title', ''),
                'page_id': article.get('page_id', ''),
                'ai_recommend': bool(preds[i])
            })
        return results
        
    except Exception as e:
        print(f"예측 중 오류 발생: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return []

def update_notion_ai_recommend_all():
    """Notion DB의 모든 기사에 대해 AI추천 예측 및 컬럼 업데이트"""
    try:
        notion = NotionClient()
        dbid = notion.get_weekly_database_id()
        
        # 1. 모든 기사 추출
        results = []
        query = notion.client.databases.query(database_id=dbid, page_size=100)
        results.extend(query.get('results', []))
        while query.get('has_more'):
            query = notion.client.databases.query(
                database_id=dbid,
                start_cursor=query['next_cursor'],
                page_size=100
            )
            results.extend(query.get('results', []))
        
        # 2. 기사 정보 추출
        articles = []
        for page in results:
            props = page['properties']
            def safe_get_text(prop, key):
                arr = prop.get(key, {}).get('title' if key == '제목' else 'rich_text', [])
                return arr[0].get('plain_text', '') if arr and 'plain_text' in arr[0] else ''
            
            articles.append({
                'page_id': page['id'],
                'title': safe_get_text(props, '제목'),
                'summary': safe_get_text(props, '한줄요약'),
                'content': safe_get_text(props, '핵심 내용')
            })
        
        # 3. AI 추천 예측
        results = predict_ai_recommend(articles)
        
        # 4. Notion에 업데이트
        for r in results:
            print(f"[AI추천 업데이트] page_id={r['page_id']} title={r['title']} ai_recommend={r['ai_recommend']}")
            try:
                notion.update_ai_recommendation(r['page_id'], r['ai_recommend'])
            except Exception as e:
                print(f"[ERROR] page_id={r['page_id']} title={r['title']} 예외: {e}")
        
        print(f"총 {len(results)}건의 AI추천 결과를 Notion에 반영 완료.")
        
    except Exception as e:
        print(f"AI 추천 업데이트 중 오류 발생: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == '__main__':
    try:
        notion = NotionClient()
        fit_and_save_model(notion)
        update_notion_ai_recommend_all()
    except Exception as e:
        import traceback
        print(f"[FATAL ERROR] {e}")
        print(traceback.format_exc()) 