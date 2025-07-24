"""
Health Check API Route
"""
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    } 