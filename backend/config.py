"""
Configuration module for FuckPaidCourses backend.
Loads environment variables and provides app-wide settings.
"""

import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # API Keys
    FIRECRAWL_API_KEY: str = os.getenv("FIRECRAWL_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")
    
    # App settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # CORS - Allow frontend origins
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
        "https://*.vercel.app",   # Vercel deployments
    ]
    
    # Rate limiting (simple in-memory)
    MAX_REQUESTS_PER_MINUTE: int = 5
    
    # Cache TTL in seconds (24 hours)
    CACHE_TTL: int = 86400
    
    def validate(self) -> list[str]:
        """Check if required API keys are set. Returns list of missing keys."""
        missing = []
        if not self.FIRECRAWL_API_KEY:
            missing.append("FIRECRAWL_API_KEY")
        if not self.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if not self.SERPER_API_KEY:
            missing.append("SERPER_API_KEY")
        return missing


settings = Settings()
