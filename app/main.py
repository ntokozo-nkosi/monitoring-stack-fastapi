# app/main.py
import logging
import signal
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

# Get environment configuration
ENV = os.getenv("ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info").upper()

# Configure logging based on environment
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
if ENV == "production":
    # More structured logging for production
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=log_format
)
logger = logging.getLogger("fastapi-app")

# Global flag for graceful shutdown
shutdown_event = False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global shutdown_event
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    shutdown_event = True
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"FastAPI application starting up in {ENV} environment with log level {LOG_LEVEL}...")
    yield
    # Shutdown
    logger.info("FastAPI application shutting down gracefully...")

# Create FastAPI app with environment-based configuration
app_kwargs = {"lifespan": lifespan}
if ENV == "production":
    app_kwargs.update({
        "docs_url": None,  # Disable docs in production
        "redoc_url": None,  # Disable redoc in production
        "openapi_url": None,  # Disable OpenAPI schema in production
    })

app = FastAPI(**app_kwargs)

# This line creates an Instrumentator instance and instruments the app.
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World", "environment": ENV}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    logger.info(f"Item endpoint accessed: item_id={item_id}, q={q}")
    return {"item_id": item_id, "q": q, "environment": ENV}

@app.get("/health")
def health_check():
    """Health check endpoint for Docker and load balancers"""
    if shutdown_event:
        return {"status": "shutting down", "environment": ENV}
    return {"status": "healthy", "environment": ENV}
