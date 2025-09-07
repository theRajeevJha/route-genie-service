from fastapi import APIRouter
from app.models.route_request import RouteRequest
from app.models.route_response import RouteResponse
from app.services.route_optimizer import RouteOptimizer
from loguru import logger

router = APIRouter()

@router.post("/routes/optimize", response_model=RouteResponse, tags=["Routes"])
async def optimize_route(request: RouteRequest):

    logger.info(f"request body: {request.model_dump_json(indent=2)}")
    route_optimizer = RouteOptimizer()
    resp = await route_optimizer.optimize_route(request)
    logger.info(f"route optimized response: {resp.model_dump_json(indent=2)}")
    return resp
