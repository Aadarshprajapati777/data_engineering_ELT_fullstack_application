from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import create_tables, SessionLocal
from app.api.endpoints import router as api_router
from app.api.dashboard import router as summary
from app.api.grouped_data import router as grouped_data

from app.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating tables in the database if they do not exist...")
    create_tables()
    logger.info("Tables created successfully.")
    
    yield
    
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")
app.include_router(summary, prefix="/api/v1")
app.include_router(grouped_data, prefix="/api/v1")


if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
