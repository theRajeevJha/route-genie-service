from loguru import logger
import sys
import logging
from app.core.config import CORRELATION_ID_CTX_VAR, LOG_LEVEL


class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # log message with Loguru
            logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())

def correlation_id_filter(record):
    record["extra"]["correlation_id"] = CORRELATION_ID_CTX_VAR.get()
    return True

def setup_logging():
    logger.remove()  # Remove default handler
    logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "correlation_id={extra[correlation_id]} | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>",
            filter=correlation_id_filter,
            level=LOG_LEVEL,  # Change to "DEBUG" if needed
            enqueue=True,  # Thread-safe
            backtrace=True,
            diagnose=True,  # Show full traceback on error
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

     # Override uvicorn loggers so only Loguru handles them
    for log_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "httpcore", "httpx"):
        logging.getLogger(log_name).setLevel(logging.CRITICAL)
        uvicorn_logger = logging.getLogger(log_name)
        uvicorn_logger.handlers = [InterceptHandler()]
        
    return logger