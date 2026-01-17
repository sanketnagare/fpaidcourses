"""
Google Gemini LLM service using the new google-genai SDK.
Extracts structured topics from course content with Pydantic schemas.
"""

import json
from google import genai
from pydantic import BaseModel, Field
from config import settings


class TopicItem(BaseModel):
    """A single topic extracted from course content."""
    topic: str = Field(description="Clear topic name, 3-8 words")
    description: str = Field(description="Brief description of what will be learned, 1-2 sentences")
    estimatedHours: float = Field(description="Estimated hours to learn this topic")


class TopicList(BaseModel):
    """List of topics extracted from course curriculum."""
    topics: list[TopicItem] = Field(description="List of course topics in learning order")


class LLMService:
    """Service for processing content using Google Gemini with structured output."""
    
    # System prompt for topic extraction
    EXTRACTION_PROMPT = """You are an expert at analyzing online course curricula. 
Given the markdown content of a course page, extract the main topics/modules that the course covers.

Rules:
- Extract 5-15 topics maximum (combine very small topics, split very large ones)
- Order topics logically (prerequisites before advanced topics)
- Keep topic names beginner-friendly and concise (3-8 words)
- If the content seems incomplete or unclear, make reasonable inferences based on the course title
- Provide brief but informative descriptions (1-2 sentences each)
- Estimate realistic learning hours for each topic

Course content to analyze:
"""

    def __init__(self):
        if settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        else:
            self.client = None
    
    def extract_topics(self, content: str, course_title: str = "") -> list[dict]:
        """
        Extract structured topics from course content.
        
        Args:
            content: Markdown content of the course page
            course_title: Optional course title for context
            
        Returns:
            List of topic dictionaries with 'topic', 'description', 'estimatedHours'
        """
        if not self.client:
            raise ValueError("Gemini API key not configured")
        
        # Prepare the prompt
        prompt = self.EXTRACTION_PROMPT
        if course_title:
            prompt += f"\nCourse Title: {course_title}\n\n"
        prompt += content[:15000]  # Limit content length to avoid token limits
        
        try:
            # Generate response with structured output using new SDK
            # Using gemini-2.5-flash-lite for better quota availability
            response = self.client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': TopicList,
                    'temperature': 0.3,
                },
            )
            
            # Parse the structured response
            if response.parsed:
                # response.parsed is a TopicList instance
                topics = []
                for item in response.parsed.topics:
                    topics.append({
                        "topic": item.topic,
                        "description": item.description,
                        "estimatedHours": item.estimatedHours,
                    })
                return topics if topics else self._fallback_topics()
            else:
                # Fallback to parsing JSON text
                result = json.loads(response.text)
                if isinstance(result, dict) and "topics" in result:
                    topics_list = result["topics"]
                elif isinstance(result, list):
                    topics_list = result
                else:
                    return self._fallback_topics()
                
                topics = []
                for i, item in enumerate(topics_list):
                    if isinstance(item, dict) and "topic" in item:
                        topics.append({
                            "topic": str(item.get("topic", f"Topic {i+1}")),
                            "description": str(item.get("description", "")),
                            "estimatedHours": float(item.get("estimatedHours", 2.0)),
                        })
                return topics if topics else self._fallback_topics()
            
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            return self._fallback_topics()
        except Exception as e:
            print(f"Gemini API error: {e}")
            raise
    
    def _fallback_topics(self) -> list[dict]:
        """Return fallback topics if extraction fails."""
        return [
            {
                "topic": "Introduction & Setup",
                "description": "Getting started with the fundamentals",
                "estimatedHours": 1.0,
            },
            {
                "topic": "Core Concepts",
                "description": "Understanding the main principles",
                "estimatedHours": 3.0,
            },
            {
                "topic": "Practical Application",
                "description": "Hands-on practice and projects",
                "estimatedHours": 4.0,
            },
        ]


# Singleton instance
llm_service = LLMService()
