from typing import List, Dict, Any
from datetime import datetime
import re
from config.config import KEYWORDS

class NewsProcessor:
    def __init__(self):
        self.keywords = KEYWORDS

    def contains_keywords(self, text: str) -> bool:
        """Check if text contains any of the keywords"""
        return any(keyword in text for keyword in self.keywords)

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        return [keyword for keyword in self.keywords if keyword in text]

    def clean_text(self, text: str) -> str:
        """Clean text by removing extra whitespace and special characters"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[^\w\s가-힣]', '', text)
        return text.strip()

    def process_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single article"""
        # Clean title and content
        article['title'] = self.clean_text(article['title'])
        article['content'] = self.clean_text(article['content'])

        # Extract keywords
        article['keywords'] = self.extract_keywords(
            article['title'] + ' ' + article['content']
        )

        # Add processing timestamp
        article['processed_date'] = datetime.now()

        return article

    def process_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple articles"""
        processed_articles = []
        for article in articles:
            if self.contains_keywords(article['title'] + ' ' + article['content']):
                processed_article = self.process_article(article)
                processed_articles.append(processed_article)
        return processed_articles 