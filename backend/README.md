# FuckPaidCourses Backend

Transform paid course URLs into free learning roadmaps.

## Quick Start

1. **Install dependencies:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Run the server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Test the API:**
   ```bash
   curl http://localhost:8000/health
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/generate-roadmap` | Generate roadmap from course URL |

## Getting API Keys

### Firecrawl (500 credits/month free)
1. Go to [firecrawl.dev](https://firecrawl.dev)
2. Sign up with email or GitHub
3. Copy API key from Dashboard

### Google Gemini (Free tier)
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with Google
3. Click "Get API Key" → "Create API Key"

### Serper.dev (2,500 searches free)
1. Go to [serper.dev](https://serper.dev)
2. Sign up for free
3. Copy API key from Dashboard

## Project Structure

```
backend/
├── main.py           # FastAPI app entry point
├── config.py         # Environment configuration
├── cache.py          # In-memory caching
├── models/
│   └── schemas.py    # Pydantic models
└── services/
    ├── scraper.py    # Firecrawl integration
    ├── llm.py        # Google Gemini
    ├── youtube.py    # yt-dlp video search
    └── search.py     # Serper.dev docs search
```
