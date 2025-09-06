"""
FastAPI Backend for Financial RAG System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
from datetime import datetime
import sys
import os

# Add paths
sys.path.append('.')
sys.path.append('src')

from financial_agent import FinancialRAGAgent, create_full_agent
from config import settings

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    use_rag: bool = True
    use_tools: bool = True

class QueryResponse(BaseModel):
    query: str
    response: str
    context_used: bool
    timestamp: str
    processing_time_ms: int

class SystemStatus(BaseModel):
    openai_available: bool
    ollama_available: bool
    rag_enabled: bool
    tools_enabled: bool

# Initialize FastAPI app
app = FastAPI(
    title="Financial RAG System API",
    description="Advanced Financial Analysis using RAG, LLM, and AI Agents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
financial_agent: Optional[FinancialRAGAgent] = None

@app.on_event("startup")
async def startup_event():
    """Initialize the financial agent on startup"""
    global financial_agent
    print("🚀 Starting Financial RAG System API...")
    try:
        financial_agent = create_full_agent()
        print("✅ Financial agent initialized")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        financial_agent = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Financial RAG System API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agent_available": financial_agent is not None
    }

@app.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get system status"""
    if not financial_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    status = financial_agent.get_system_status()
    return SystemStatus(**status)

@app.post("/analyze", response_model=QueryResponse)
async def analyze_query(request: QueryRequest):
    """Analyze financial query"""
    if not financial_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    start_time = datetime.now()

    try:
        result = financial_agent.analyze_query(request.query)
        end_time = datetime.now()
        processing_time = int((end_time - start_time).total_seconds() * 1000)

        return QueryResponse(
            query=result["query"],
            response=result["response"],
            context_used=bool(result["context"]),
            timestamp=end_time.isoformat(),
            processing_time_ms=processing_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/companies")
async def get_companies():
    """Get list of companies"""
    return {"companies": ["TechCorp", "FinanceInc", "HealthPlus", "EnergyGiant", "RetailMax"]}

@app.get("/sectors")
async def get_sectors():
    """Get list of sectors"""
    return {"sectors": ["Technology", "Finance", "Healthcare", "Energy", "Retail"]}

if __name__ == "__main__":
    print(f"🚀 Starting Financial RAG API server...")
    print(f"Host: {settings.API_HOST}:{settings.API_PORT}")

    uvicorn.run(
        "fastapi_app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
