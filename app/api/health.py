from fastapi import APIRouter
from loguru import logger

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    logger.debug("Health check endpoint called.")
    return {"status": "ok", "message": "routeGenie service is healthy"}
