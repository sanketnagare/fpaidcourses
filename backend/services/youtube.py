"""
YouTube search service using Official Google YouTube Data API v3.
Most reliable method, no scraping or bot detection issues.
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import settings
import re
from datetime import timedelta

class YouTubeService:
    """Service for searching YouTube videos using Official API."""
    
    def __init__(self):
        # Prefer specific YouTube key, fallback to Gemini key (often same project)
        self.api_key = settings.YOUTUBE_API_KEY or settings.GEMINI_API_KEY
    
    def search_videos(self, query: str, max_results: int = 3) -> list[dict]:
        """
        Hybrid Search:
        1. Use Serper to find video URLs (Fast, saves YouTube Search Quota).
        2. Use YouTube API to fetch details (views, duration) for those IDs (Cheap: 1 unit).
        Threads-safe and High Quality.
        """
        max_results = min(max(1, max_results), 5)
        
        # 1. Discovery Phase (Serper)
        # Fetch more candidates to ensure we find valid YouTube links
        from services.search import search_service
        try:
            # Append 'youtube' to query to ensure we get video platform results
            discovery_query = f"site:youtube.com {query}"
            raw_results = search_service.search_videos(discovery_query, num_results=10)
        except Exception as e:
            print(f"Serper discovery failed: {e}")
            raw_results = []
            
        if not raw_results:
            return []

        # Extract Video IDs
        video_ids = []
        video_map = {} # Map ID back to Serper result for fallback data
        
        for res in raw_results:
            url = res.get("link", "")
            video_id = self._extract_video_id(url)
            if video_id:
                video_ids.append(video_id)
                video_map[video_id] = res
        
        if not video_ids:
            return []
            
        # 2. Enrichment Phase (YouTube API)
        if not self.api_key:
            print("YouTube API not initialized (no key) - returning raw Serper results")
            return self._fallback_response(video_map.values(), max_results)
            
        try:
            with build("youtube", "v3", developerKey=self.api_key, cache_discovery=False) as youtube:
                videos_response = youtube.videos().list(
                    id=",".join(video_ids[:50]), # API limit per call
                    part="snippet,contentDetails,statistics"
                ).execute()
                
                candidates = []
                for item in videos_response.get("items", []):
                    vid_id = item["id"]
                    snippet = item.get("snippet", {})
                    statistics = item.get("statistics", {})
                    content_details = item.get("contentDetails", {})
                    
                    # Parse details
                    duration_iso = content_details.get("duration", "PT0S")
                    duration_formatted = self._parse_iso_duration(duration_iso)
                    view_count = int(statistics.get("viewCount", 0))
                    
                    # Merge with basic info (prefer API data over Serper)
                    candidates.append({
                        "title": snippet.get("title", video_map[vid_id].get("title")),
                        "url": f"https://www.youtube.com/watch?v={vid_id}",
                        "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", video_map[vid_id].get("imageUrl")),
                        "views": self._format_views(view_count),
                        "channel": snippet.get("channelTitle", video_map[vid_id].get("source")),
                        "duration": duration_formatted,
                        "_view_count": view_count
                    })
                
                # Sort by views and return top N
                candidates.sort(key=lambda x: x["_view_count"], reverse=True)
                
                for vid in candidates:
                    vid.pop("_view_count", None)
                    
                return candidates[:max_results]
                
        except Exception as e:
            print(f"YouTube Enrichement failed: {e}. Returning raw results.")
            return self._fallback_response(video_map.values(), max_results)

    def _extract_video_id(self, url: str) -> str:
        """Extract YouTube Video ID from URL."""
        # Regex for standard and short URLs
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
            r'(?:embed\/)([0-9A-Za-z_-]{11})'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return ""

    def _fallback_response(self, serper_results, max_results):
        """Return raw Serper results if enrichment fails."""
        videos = []
        for res in list(serper_results)[:max_results]:
            videos.append({
                "title": res.get("title", "Untitled"),
                "url": res.get("link", ""),
                "thumbnail": res.get("imageUrl", "https://i.ytimg.com/vi/placeholder/hqdefault.jpg"),
                "views": "N/A",
                "channel": res.get("source", "YouTube"),
                "duration": res.get("duration", "")
            })
        return videos


    def _parse_iso_duration(self, iso_duration: str) -> str:
        """Parse ISO 8601 duration string (PT1H2M3S) to HH:MM:SS."""
        try:
            # Simple regex parsing for PT#H#M#S format
            match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
            if not match:
                return ""
            
            h, m, s = match.groups()
            hours = int(h) if h else 0
            minutes = int(m) if m else 0
            seconds = int(s) if s else 0
            
            if hours > 0:
                return f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes}:{seconds:02d}"
        except:
            return ""

    def _format_views(self, count: int) -> str:
        """Format view count for display (e.g., 1.2M, 500K)."""
        if not count: return "N/A"
        if count >= 1_000_000_000:
            return f"{count / 1_000_000_000:.1f}B"
        elif count >= 1_000_000:
            return f"{count / 1_000_000:.1f}M"
        elif count >= 1_000:
            return f"{count / 1_000:.1f}K"
        else:
            return str(count)


# Singleton instance
youtube_service = YouTubeService()
