import pkgutil
import importlib
from fastapi import FastAPI
from app.core.middleware import LoggingMiddleware, CorrelationIdMiddleware
from app.core.logging import setup_logging
import uvicorn

logger = setup_logging()

app = FastAPI(
    title="RouteGenie Service",
    version="1.0.0",
    description="RouteGenie Service is an API designed to generate, manage, and optimize routes for various applications. It provides endpoints for route calculation, management of route data, and integration with mapping services, enabling efficient and scalable route planning for logistics, delivery, and transportation solutions."
)

#add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)

# Include API routers
for _, module_name, _ in pkgutil.iter_modules(['app/api']):
    module = importlib.import_module(f'app.api.{module_name}')
    if hasattr(module, 'router'):
        app.include_router(module.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
