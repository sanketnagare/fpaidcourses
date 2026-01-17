"""
FuckPaidCourses - Backend API

Transform paid course URLs into free learning roadmaps.
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import time

from config import settings
from cache import course_cache, roadmap_cache
from logger import logger, RequestLogger, Colors
from models.schemas import (
    GenerateRoadmapRequest,
    RoadmapResponse,
    ErrorResponse,
    CourseInfo,
    Topic,
    Video,
    Documentation,
)
from services.scraper import scraper_service
from services.llm import llm_service
from services.youtube import youtube_service
from services.search import search_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    logger.info(f"{'='*60}")
    logger.info(f"🚀 {Colors.BOLD}FuckPaidCourses API Starting{Colors.RESET}")
    logger.info(f"{'='*60}")
    
    missing_keys = settings.validate()
    if missing_keys:
        logger.warning(f"Missing API keys: {missing_keys}")
    else:
        logger.info("✅ All API keys configured")
    
    logger.info(f"   📦 Firecrawl: {'Ready' if settings.FIRECRAWL_API_KEY else 'Not configured'}")
    logger.info(f"   🤖 Gemini:    {'Ready' if settings.GEMINI_API_KEY else 'Not configured'}")
    logger.info(f"   🔍 Serper:    {'Ready' if settings.SERPER_API_KEY else 'Not configured'}")
    logger.info(f"   📺 YouTube:   Ready (no key needed)")
    logger.info(f"{'='*60}")
    
    yield
    
    # Shutdown
    logger.info(f"{'='*60}")
    logger.info("👋 Shutting down FuckPaidCourses API")
    logger.info(f"   Clearing caches...")
    course_cache.clear()
    roadmap_cache.clear()
    logger.info("✅ Shutdown complete")
    logger.info(f"{'='*60}")


# Create FastAPI app
app = FastAPI(
    title="FuckPaidCourses API",
    description="Transform paid course URLs into free learning roadmaps",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API info."""
    return {
        "name": "FuckPaidCourses API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "generate": "POST /generate-roadmap",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Render."""
    missing = settings.validate()
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "firecrawl": "configured" if settings.FIRECRAWL_API_KEY else "missing",
            "gemini": "configured" if settings.GEMINI_API_KEY else "missing",
            "serper": "configured" if settings.SERPER_API_KEY else "missing",
            "youtube": "ready (no key needed)",
        }
    }


@app.post("/generate-roadmap", response_model=RoadmapResponse)
async def generate_roadmap(request: GenerateRoadmapRequest):
    """
    Generate a free learning roadmap from a paid course URL.
    """
    url = request.url.strip()
    
    # Validate URL format
    if not url.startswith(("http://", "https://")):
        logger.warning(f"Invalid URL format: {url}")
        raise HTTPException(
            status_code=400,
            detail={"error": "INVALID_URL", "message": "URL must start with http:// or https://"}
        )
    
    # Check cache first
    cached_roadmap = roadmap_cache.get(url)
    if cached_roadmap:
        logger.info(f"📦 {Colors.GREEN}CACHE HIT{Colors.RESET} - Returning cached roadmap")
        logger.info(f"   URL: {url[:60]}...")
        return cached_roadmap
    
    # Validate API keys
    missing = settings.validate()
    if missing:
        logger.error(f"Missing configuration: {missing}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "MISSING_CONFIG",
                "message": f"Server is not fully configured. Missing: {', '.join(missing)}"
            }
        )
    
    # Use RequestLogger for detailed tracking
    with RequestLogger("Generate Roadmap", url) as req_log:
        try:
            # Step 1: Scrape the course page
            req_log.step("Scraping course page", "Using Firecrawl API")
            start_scrape = time.time()
            scraped = scraper_service.scrape_course(url)
            scrape_time = time.time() - start_scrape
            
            if not scraped.get("success"):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "SCRAPE_FAILED",
                        "message": f"Could not scrape course page: {scraped.get('error', 'Unknown error')}"
                    }
                )
            
            course_title = scraped["title"]
            platform = scraped["platform"]
            content = scraped["content"]
            
            req_log.detail(f"Title: {course_title}")
            req_log.detail(f"Platform: {platform}")
            req_log.detail(f"Content length: {len(content)} chars")
            req_log.detail(f"Scrape time: {scrape_time:.2f}s")
            
            # Step 2: Extract topics using LLM
            req_log.step("Extracting topics with AI", "Using Gemini 2.5 Flash Lite")
            start_llm = time.time()
            raw_topics = llm_service.extract_topics(content, course_title)
            llm_time = time.time() - start_llm
            
            req_log.detail(f"Extracted {len(raw_topics)} topics")
            req_log.detail(f"LLM time: {llm_time:.2f}s")
            
            for i, topic in enumerate(raw_topics):
                req_log.detail(f"  Topic {i+1}: {topic['topic']}")
            
            # Step 3 & 4: Find resources for each topic (in parallel)
            req_log.step("Finding resources", f"YouTube + Serper for {len(raw_topics)} topics")
            start_resources = time.time()
            roadmap_topics = await _enrich_topics(raw_topics, req_log)
            resources_time = time.time() - start_resources
            
            req_log.detail(f"Resource search time: {resources_time:.2f}s")
            
            # Count total resources
            total_videos = sum(len(t.videos) for t in roadmap_topics)
            total_docs = sum(len(t.documentation) for t in roadmap_topics)
            req_log.detail(f"Total videos found: {total_videos}")
            req_log.detail(f"Total docs found: {total_docs}")
            
            # Build response
            req_log.step("Building response")
            response = RoadmapResponse(
                success=True,
                course=CourseInfo(
                    title=course_title,
                    platform=platform,
                    originalUrl=url,
                    totalTopics=len(roadmap_topics),
                ),
                roadmap=roadmap_topics,
                generatedAt=datetime.utcnow(),
            )
            
            # Cache the result
            roadmap_cache.set(url, response)
            req_log.detail("Response cached for future requests")
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to generate roadmap: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "GENERATION_FAILED",
                    "message": f"Failed to generate roadmap: {str(e)}"
                }
            )


async def _enrich_topics(raw_topics: list[dict], req_log: RequestLogger) -> list[Topic]:
    """Add YouTube videos and documentation to each topic."""
    
    async def enrich_single_topic(index: int, topic_data: dict) -> Topic:
        """Enrich a single topic with resources."""
        topic_name = topic_data["topic"]
        
        # Run YouTube and Serper searches concurrently
        loop = asyncio.get_event_loop()
        
        # These are sync functions, run them in thread pool
        videos_task = loop.run_in_executor(
            None, 
            youtube_service.search_videos, 
            f"{topic_name} tutorial",
            3
        )
        docs_task = loop.run_in_executor(
            None,
            search_service.search_documentation,
            topic_name,
            2
        )
        
        videos_raw, docs_raw = await asyncio.gather(videos_task, docs_task)
        
        # Log results for this topic
        logger.debug(f"       Topic {index+1}: {len(videos_raw)} videos, {len(docs_raw)} docs")
        
        # Convert to Pydantic models
        videos = [Video(**v) for v in videos_raw]
        docs = [Documentation(**d) for d in docs_raw]
        
        return Topic(
            id=index + 1,
            order=index + 1,
            topic=topic_data["topic"],
            description=topic_data.get("description", ""),
            estimatedHours=topic_data.get("estimatedHours"),
            videos=videos,
            documentation=docs,
        )
    
    # Process all topics concurrently
    logger.info(f"       Processing {len(raw_topics)} topics in parallel...")
    tasks = [
        enrich_single_topic(i, topic) 
        for i, topic in enumerate(raw_topics)
    ]
    
    results = await asyncio.gather(*tasks)
    logger.info(f"       ✅ All topics enriched")
    
    return results


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unexpected errors gracefully."""
    logger.error(f"Unhandled exception: {type(exc).__name__}: {exc}")
    return {
        "success": False,
        "error": "INTERNAL_ERROR",
        "message": "An unexpected error occurred. Please try again.",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
