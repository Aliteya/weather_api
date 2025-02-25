from fastapi import FastAPI
from .database import init_db, close_db_connections
from .controllers import weather_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"start")
    await init_db()
    yield
    await close_db_connections()
    print(f"finish")

version = "v1"    

app = FastAPI(lifespan=life_span)

app.include_router(weather_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}