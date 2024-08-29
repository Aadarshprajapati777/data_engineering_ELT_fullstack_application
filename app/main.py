from fastapi import FastAPI
from app.api import endpoints

app = FastAPI()


app.include_router(endpoints.router,  prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
