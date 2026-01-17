"""
Pydantic models for request/response schemas.
"""

from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime


# Request Models
class GenerateRoadmapRequest(BaseModel):
    """Request body for generating a roadmap from a course URL."""
    url: str = Field(..., description="URL of the paid course to convert")


# Response Models
class Video(BaseModel):
    """YouTube video information."""
    title: str
    url: str
    thumbnail: str
    views: str
    channel: str
    duration: Optional[str] = None


class Documentation(BaseModel):
    """Documentation/resource link."""
    title: str
    url: str
    snippet: Optional[str] = None


class Topic(BaseModel):
    """A single topic/milestone in the roadmap."""
    id: int
    order: int
    topic: str
    description: str
    estimatedHours: Optional[float] = None
    videos: list[Video]
    documentation: list[Documentation]


class CourseInfo(BaseModel):
    """Basic information about the original course."""
    title: str
    platform: str
    originalUrl: str
    totalTopics: int


class RoadmapResponse(BaseModel):
    """Successful response with generated roadmap."""
    success: bool = True
    course: CourseInfo
    roadmap: list[Topic]
    generatedAt: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Error response."""
    success: bool = False
    error: str
    message: str
