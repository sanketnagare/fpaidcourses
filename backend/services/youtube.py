"""
YouTube search service using yt-dlp.
Searches for videos and returns metadata - NO downloading!
"""

import yt_dlp
from typing import Optional


class YouTubeService:
    """Service for searching YouTube videos using yt-dlp (no API key needed)."""
    
    def __init__(self):
        # yt-dlp options - extract info only, NO download
        self.ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,  # Get full metadata
            "ignoreerrors": True,
        }
    
    def search_videos(self, query: str, max_results: int = 3) -> list[dict]:
        """
        Search YouTube for videos matching the query.
        
        Args:
            query: Search terms
            max_results: Maximum number of videos to return (1-5)
            
        Returns:
            List of video dictionaries with title, url, thumbnail, views, channel, duration
        """
        max_results = min(max(1, max_results), 5)  # Clamp to 1-5
        search_query = f"ytsearch{max_results}:{query}"
        
        videos = []
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Extract info without downloading
                result = ydl.extract_info(search_query, download=False)
                
                if not result or "entries" not in result:
                    return []
                
                for entry in result["entries"]:
                    if entry is None:
                        continue
                    
                    video = self._parse_video_entry(entry)
                    if video:
                        videos.append(video)
        
        except Exception as e:
            print(f"YouTube search error: {e}")
            return []
        
        # Sort by view count (descending) to prioritize popular/quality content
        videos.sort(key=lambda v: v.get("view_count_raw", 0), reverse=True)
        
        # Remove raw view count from response
        for v in videos:
            v.pop("view_count_raw", None)
        
        return videos
    
    def _parse_video_entry(self, entry: dict) -> Optional[dict]:
        """Parse a yt-dlp entry into our video format."""
        try:
            video_id = entry.get("id", "")
            if not video_id:
                return None
            
            # Get view count
            view_count = entry.get("view_count", 0) or 0
            
            # Format view count for display
            views_display = self._format_views(view_count)
            
            # Format duration
            duration_seconds = entry.get("duration", 0) or 0
            duration_display = self._format_duration(duration_seconds)
            
            # Get best thumbnail
            thumbnails = entry.get("thumbnails", [])
            thumbnail_url = ""
            if thumbnails:
                # Prefer medium quality thumbnail
                for thumb in thumbnails:
                    if thumb.get("url"):
                        thumbnail_url = thumb["url"]
                        if "hqdefault" in thumbnail_url or "mqdefault" in thumbnail_url:
                            break
            
            # Fallback to standard YouTube thumbnail URL
            if not thumbnail_url:
                thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
            
            return {
                "title": entry.get("title", "Untitled"),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": thumbnail_url,
                "views": views_display,
                "channel": entry.get("channel", entry.get("uploader", "Unknown")),
                "duration": duration_display,
                "view_count_raw": view_count,  # For sorting, removed later
            }
            
        except Exception as e:
            print(f"Error parsing video entry: {e}")
            return None
    
    def _format_views(self, count: int) -> str:
        """Format view count for display (e.g., 1.2M, 500K)."""
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
        if seconds <= 0:
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
