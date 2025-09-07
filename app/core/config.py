from contextvars import ContextVar
import os
from loguru import logger
from dotenv import load_dotenv

# context var for the correlation id
CORRELATION_ID_CTX_VAR: ContextVar[str] = ContextVar("correlation_id", default="-")

def get_env_var(name:str) -> str:
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Environment variable '{name}' is not set.")
    return value

logger.info("loading env variables...")
load_dotenv()
ORS_API_KEY = get_env_var("ORS_API_KEY")
LOG_LEVEL = get_env_var("LOG_LEVEL")
logger.info(f"Log level set to: {LOG_LEVEL} ")
logger.info("env variables loaded....")