"""
Firecrawl scraper service.
Scrapes course pages and extracts curriculum content.
"""

import re
from typing import Optional
from firecrawl import FirecrawlApp
from config import settings


class ScraperService:
    """Service for scraping course pages using Firecrawl."""
    
    # Platform detection patterns
    PLATFORM_PATTERNS = {
        "udemy": r"udemy\.com",
        "coursera": r"coursera\.org",
        "skillshare": r"skillshare\.com",
        "pluralsight": r"pluralsight\.com",
        "linkedin": r"linkedin\.com/learning",
        "edx": r"edx\.org",
        "udacity": r"udacity\.com",
    }
    
    def __init__(self):
        if settings.FIRECRAWL_API_KEY:
            self.client = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)
        else:
            self.client = None
    
    def detect_platform(self, url: str) -> str:
        """Detect which platform the course URL belongs to."""
        url_lower = url.lower()
        for platform, pattern in self.PLATFORM_PATTERNS.items():
            if re.search(pattern, url_lower):
                return platform.capitalize()
        return "Unknown"
    
    def scrape_course(self, url: str) -> dict:
        """
        Scrape a course page and extract content.
        
        Returns:
            dict with keys: title, platform, content (markdown), success
        """
        if not self.client:
            raise ValueError("Firecrawl API key not configured")
        
        platform = self.detect_platform(url)
        
        try:
            # Scrape the page using Firecrawl
            result = self.client.scrape_url(
                url,
                params={
                    "formats": ["markdown"],
                    "onlyMainContent": True,
                }
            )
            
            # Extract content from result
            content = result.get("markdown", "")
            
            # Try to extract title from the content or metadata
            title = self._extract_title(content, result.get("metadata", {}))
            
            return {
                "success": True,
                "title": title,
                "platform": platform,
                "content": content,
                "url": url,
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "platform": platform,
                "url": url,
            }
    
    def _extract_title(self, content: str, metadata: dict) -> str:
        """Extract course title from content or metadata."""
        # Try metadata first
        if metadata.get("title"):
            title = metadata["title"]
            # Clean up common suffixes
            for suffix in [" | Udemy", " - Coursera", " | Skillshare"]:
                title = title.replace(suffix, "")
            return title.strip()
        
        # Try to find first heading in markdown
        lines = content.split("\n")
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        
        return "Untitled Course"


# Singleton instance
scraper_service = ScraperService()
