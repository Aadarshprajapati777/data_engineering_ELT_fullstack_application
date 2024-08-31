from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import create_tables, SessionLocal
from app.api.endpoints import router as api_router
from app.api.dashboard import router as summary
from app.api.grouped_data import router as grouped_data
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import ALLOW_ORIGINS, ALLOW_CREDENTIALS, ALLOW_METHODS, ALLOW_HEADERS

from app.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating tables in the database if they do not exist...")
    create_tables()
    logger.info("Tables created successfully.")
    
    yield
    
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS, 
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(summary, prefix="/api/v1")
app.include_router(grouped_data, prefix="/api/v1")

if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
