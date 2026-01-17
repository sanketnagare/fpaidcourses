"""
Simple in-memory cache for scraped courses.
Helps reduce Firecrawl API usage by caching results.
"""

import hashlib
import time
from typing import Optional, Any
from config import settings


class SimpleCache:
    """Thread-safe in-memory cache with TTL."""
    
    def __init__(self, ttl: int = None):
        self._cache: dict[str, tuple[Any, float]] = {}
        self._ttl = ttl or settings.CACHE_TTL
    
    def _hash_key(self, key: str) -> str:
        """Create a hash of the key for consistent storage."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache if it exists and hasn't expired."""
        hashed = self._hash_key(key)
        
        if hashed not in self._cache:
            return None
        
        value, timestamp = self._cache[hashed]
        
        # Check if expired
        if time.time() - timestamp > self._ttl:
            del self._cache[hashed]
            return None
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Store a value in cache with current timestamp."""
        hashed = self._hash_key(key)
        self._cache[hashed] = (value, time.time())
    
    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
    
    def cleanup_expired(self) -> int:
        """Remove expired entries and return count of removed items."""
        now = time.time()
        expired_keys = [
            k for k, (_, ts) in self._cache.items()
            if now - ts > self._ttl
        ]
        for k in expired_keys:
            del self._cache[k]
        return len(expired_keys)


# Global cache instances
course_cache = SimpleCache()  # Cache for scraped course content
roadmap_cache = SimpleCache()  # Cache for full generated roadmaps
