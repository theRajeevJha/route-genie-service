import time
import uuid
import traceback
from fastapi import Request
from fastapi.exceptions import RequestValidationError as ReqValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from loguru import logger
from app.core.config import CORRELATION_ID_CTX_VAR

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        # store correlation id in context var
        CORRELATION_ID_CTX_VAR.set(correlation_id)

        response: Response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        
        return response
    

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        logger.info(f"Received request: {request.method} {request.url.path} - from {request.client.host}")
        try:
            response: Response = await call_next(request)
        except Exception as e:
            logger.error(f"Error processing request:{request.url.path}, error: {e}")
            raise e
        process_time = (time.time() - start_time) * 1000  # in milliseconds
        formatted_time = f"{process_time:.2f}ms"
        logger.info(
            f"{request.method} {request.url.path}"
            f" completed with status code: {response.status_code} in {formatted_time}")
        return response