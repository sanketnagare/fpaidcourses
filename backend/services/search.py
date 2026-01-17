"""
Serper.dev search service.
Searches for documentation and official resources.
"""

import httpx
from typing import Optional
from config import settings


class SearchService:
    """Service for searching documentation using Serper.dev."""
    
    SERPER_API_URL = "https://google.serper.dev/search"
    
    # Preferred domains for documentation (higher priority)
    PRIORITY_DOMAINS = [
        "docs.",
        "developer.",
        "learn.",
        "tutorial",
        "guide",
        "mozilla.org",
        "w3schools.com",
        "realpython.com",
        "freecodecamp.org",
        "geeksforgeeks.org",
        "tutorialspoint.com",
    ]
    
    # Domains to filter out (less useful for learning)
    BLOCKED_DOMAINS = [
        "youtube.com",  # We handle YouTube separately
        "udemy.com",
        "coursera.org",
        "skillshare.com",
        "linkedin.com/learning",
        "amazon.com",
        "ebay.com",
    ]
    
    def __init__(self):
        self.api_key = settings.SERPER_API_KEY
    
    def search_documentation(self, topic: str, max_results: int = 3) -> list[dict]:
        """
        Search for documentation and tutorials about a topic.
        
        Args:
            topic: The topic to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of documentation links with title, url, snippet
        """
        if not self.api_key:
            raise ValueError("Serper API key not configured")
        
        # Enhance query for documentation
        query = f"{topic} tutorial documentation guide"
        
        try:
            response = httpx.post(
                self.SERPER_API_URL,
                headers={
                    "X-API-KEY": self.api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "q": query,
                    "num": 10,  # Get more results to filter
                },
                timeout=15.0,
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Parse and filter results
            docs = []
            organic_results = data.get("organic", [])
            
            for result in organic_results:
                doc = self._parse_result(result)
                if doc:
                    docs.append(doc)
            
            # Sort by priority (official docs first)
            docs.sort(key=lambda d: d.get("_priority", 0), reverse=True)
            
            # Remove priority field and limit results
            for d in docs:
                d.pop("_priority", None)
            
            return docs[:max_results]
            
        except httpx.HTTPError as e:
            print(f"Serper API error: {e}")
            return []
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def _parse_result(self, result: dict) -> Optional[dict]:
        """Parse a Serper result into our format."""
        url = result.get("link", "")
        
        # Filter blocked domains
        for blocked in self.BLOCKED_DOMAINS:
            if blocked in url.lower():
                return None
        
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        
        if not url or not title:
            return None
        
        # Calculate priority based on domain
        priority = 0
        url_lower = url.lower()
        for domain in self.PRIORITY_DOMAINS:
            if domain in url_lower:
                priority += 1
        
        return {
            "title": title,
            "url": url,
            "snippet": snippet[:200] if snippet else None,
            "_priority": priority,
        }


# Singleton instance
search_service = SearchService()
