"""
News API integration for Jarvis Bot
"""

import requests
from typing import Optional, List, Dict, Any
from datetime import datetime


class NewsAPI:
    """
    News service using NewsAPI.org
    """
    
    def __init__(self, config):
        """
        Initialize news API
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.api_key = config.get('news_api_key')
        self.base_url = "https://newsapi.org/v2"
        
        if not self.api_key:
            print("News API key not configured. News functionality disabled.")
    
    def get_headlines(self, country: str = 'us', category: Optional[str] = None, max_articles: int = 5) -> Optional[List[str]]:
        """
        Get top news headlines
        
        Args:
            country: Country code (e.g., 'us', 'gb', 'ca')
            category: News category (business, entertainment, general, health, science, sports, technology)
            max_articles: Maximum number of articles to return
        
        Returns:
            List of headline strings or None if failed
        """
        if not self.api_key:
            return ["News service is not configured. Please add your News API key."]
        
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'apiKey': self.api_key,
                'country': country,
                'pageSize': max_articles
            }
            
            if category:
                params['category'] = category
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok':
                headlines = []
                for article in data.get('articles', []):
                    title = article.get('title', '')
                    if title and title != '[Removed]':
                        headlines.append(title)
                
                return headlines[:max_articles] if headlines else None
            else:
                print(f"News API error: {data.get('message', 'Unknown error')}")
                return None
                
        except requests.RequestException as e:
            print(f"News API request failed: {e}")
            return None
        except Exception as e:
            print(f"Error getting news headlines: {e}")
            return None
    
    def search_news(self, query: str, max_articles: int = 5) -> Optional[List[Dict[str, str]]]:
        """
        Search for news articles by keyword
        
        Args:
            query: Search query
            max_articles: Maximum number of articles to return
        
        Returns:
            List of article dictionaries or None if failed
        """
        if not self.api_key:
            return None
        
        try:
            url = f"{self.base_url}/everything"
            params = {
                'apiKey': self.api_key,
                'q': query,
                'sortBy': 'relevancy',
                'pageSize': max_articles,
                'language': 'en'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok':
                articles = []
                for article in data.get('articles', []):
                    if article.get('title') and article.get('title') != '[Removed]':
                        article_info = {
                            'title': article.get('title', ''),
                            'description': article.get('description', ''),
                            'source': article.get('source', {}).get('name', ''),
                            'url': article.get('url', ''),
                            'published': article.get('publishedAt', '')
                        }
                        articles.append(article_info)
                
                return articles[:max_articles] if articles else None
            else:
                print(f"News search API error: {data.get('message', 'Unknown error')}")
                return None
                
        except requests.RequestException as e:
            print(f"News search API request failed: {e}")
            return None
        except Exception as e:
            print(f"Error searching news: {e}")
            return None
    
    def get_category_news(self, category: str, max_articles: int = 3) -> Optional[List[str]]:
        """
        Get news from a specific category
        
        Args:
            category: News category
            max_articles: Maximum number of articles
        
        Returns:
            List of headlines or None if failed
        """
        valid_categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
        
        if category.lower() not in valid_categories:
            return [f"Invalid category. Valid categories are: {', '.join(valid_categories)}"]
        
        return self.get_headlines(category=category.lower(), max_articles=max_articles)
    
    def get_tech_news(self) -> Optional[List[str]]:
        """Get technology news headlines"""
        return self.get_category_news('technology')
    
    def get_sports_news(self) -> Optional[List[str]]:
        """Get sports news headlines"""
        return self.get_category_news('sports')
    
    def get_business_news(self) -> Optional[List[str]]:
        """Get business news headlines"""
        return self.get_category_news('business')
    
    def format_headlines_for_speech(self, headlines: List[str]) -> str:
        """
        Format headlines for speech output
        
        Args:
            headlines: List of headline strings
        
        Returns:
            Formatted string for speech
        """
        if not headlines:
            return "No news headlines available at the moment."
        
        if len(headlines) == 1:
            return f"Here's the top headline: {headlines[0]}"
        
        speech = "Here are the top news headlines: "
        for i, headline in enumerate(headlines, 1):
            speech += f"Headline {i}: {headline}. "
        
        return speech
    
    def test_connection(self) -> bool:
        """
        Test news API connection
        
        Returns:
            True if connection is working, False otherwise
        """
        if not self.api_key:
            return False
        
        try:
            test_headlines = self.get_headlines(max_articles=1)
            return test_headlines is not None and len(test_headlines) > 0
        except Exception:
            return False