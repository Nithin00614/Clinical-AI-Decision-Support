import logging
import time
from fastapi import FastAPI
from fastapi import Request
from api.routes import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clinical-ai-api")

app = FastAPI(
    title="Clinical AI Decision Support API",
    version="1.0"
)

# versioned API
app.include_router(router, prefix="/api/v1")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)

    logger.info(f"{request.method} {request.url.path} completed in {duration}s")
    return response
