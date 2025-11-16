# app/app_main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging

from app.data_fetcher import DataFetcher
from app.qa_engine import QAEngine

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Member QA System",
    description="Answer natural language questions about member data",
    version="1.0.0"
)

# initialize components
data_fetcher = DataFetcher()
qa_engine = QAEngine(api_key=os.getenv("OPENAI_API_KEY"))

# pydantic models
class QuestionRequest(BaseModel):
    question: str
    
class AnswerResponse(BaseModel):
    answer: str

class StatsResponse(BaseModel):
    total_messages: int
    unique_users: int
    cache_status: str

# cached data
_cached_messages = None
_cached_context = None

def get_context(force_refresh: bool = False):
    """
    fetch or return cached context
    """
    global _cached_messages, _cached_context
    
    if _cached_context is None or force_refresh:
        _cached_messages = data_fetcher.fetch_all_messages()
        
        if not _cached_messages:
            logger.error("No messages returned")
            _cached_context = None
        else:
            _cached_context = data_fetcher.format_messages_for_context(_cached_messages)
            logger.info(f"Cached {len(_cached_messages)} messages")
    
    return _cached_context

@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "Member QA System API",
        "endpoints": {
            "ask": "/ask (POST)",
            "stats": "/stats (GET)",
            "refresh": "/refresh (POST)"
        }
    }

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    global _cached_messages
    if _cached_messages is None:
        get_context()
    
    stats = data_fetcher.get_message_stats(_cached_messages or [])
    
    return StatsResponse(
        total_messages=stats.get("total_messages", 0),
        unique_users=stats.get("unique_users", 0),
        cache_status="loaded" if _cached_messages else "empty"
    )

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    context = get_context()
    
    if not context:
        raise HTTPException(status_code=503, detail="Unable to fetch messages")
    
    try:
        answer = qa_engine.answer_question(request.question, context)
        return AnswerResponse(answer=answer)
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate answer")

@app.post("/refresh")
async def refresh_cache():
    global _cached_messages, _cached_context
    
    _cached_messages = None
    _cached_context = None
    
    context = get_context(force_refresh=True)
    
    if not context:
        raise HTTPException(status_code=503, detail="Failed to refresh cache")
    
    return {
        "status": "cache refreshed",
        "messages_count": len(_cached_messages) if _cached_messages else 0
    }

@app.on_event("startup")
async def startup_event():
    get_context()
