# app/main.py
import logging
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

# Simple console logging that will be captured by Docker
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("fastapi-app")

app = FastAPI()

# This line creates an Instrumentator instance and instruments the app.
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    logger.info(f"Item endpoint accessed: item_id={item_id}, q={q}")
    return {"item_id": item_id, "q": q}
