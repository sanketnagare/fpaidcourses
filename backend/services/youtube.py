"""
YouTube search service using pytubefix.
Searches for videos and returns metadata.
"""

from typing import Optional
from pytubefix import Search


class YouTubeService:
    """Service for searching YouTube videos using pytubefix."""
    
    def __init__(self):
        pass
    
    def search_videos(self, query: str, max_results: int = 3) -> list[dict]:
        """
        Search YouTube for videos matching the query using pytubefix.
        
        Args:
            query: Search terms
            max_results: Maximum number of videos to return (1-5)
            
        Returns:
            List of video dictionaries with title, url, thumbnail, views, channel, duration
        """
        max_results = min(max(1, max_results), 5)  # Clamp to 1-5
        
        try:
            # Pytubefix search
            s = Search(query)
            results = s.videos
            
            if not results:
                return []

            # Map results to our video format
            videos = []
            for video in results[:max_results]:
                try:
                    # Parse duration in seconds to HH:MM:SS
                    duration_sec = video.length
                    duration_display = self._format_duration(duration_sec)
                    
                    videos.append({
                        "title": video.title,
                        "url": video.watch_url,
                        "thumbnail": video.thumbnail_url,
                        "views": self._format_views(video.views), 
                        "channel": video.author,
                        "duration": duration_display
                    })
                except Exception as parse_err:
                    print(f"Error parsing video object: {parse_err}")
                    continue
                    
            return videos
            
        except Exception as e:
            print(f"YouTube search error (pytubefix): {e}")
            return []

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
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration in HH:MM:SS or MM:SS format."""
        if not seconds or seconds <= 0:
            return ""
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"


# Singleton instance
youtube_service = YouTubeService()
