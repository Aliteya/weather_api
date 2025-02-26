from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from .database import init_db, close_db_connections
from .controllers import weather_router
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def life_span(app: FastAPI):
    await init_db()
    yield
    await close_db_connections()

version = "v1"    

app = FastAPI(lifespan=life_span)

app.include_router(weather_router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})