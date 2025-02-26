from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..database import get_session
from ..utils import get_weather_from_api
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import WeatherOut, WeatherHistory, WeatherDetailSchema
from ..repository import QueryRepo
 
templates = Jinja2Templates(directory="templates")

weather_router = APIRouter(prefix="/weather")

@weather_router.get("/form", response_class=HTMLResponse)
async def get_weather_form(request: Request):
    return templates.TemplateResponse("weather_form.html", {"request": request})

@weather_router.post("/get", response_class=HTMLResponse)
async def get_weather(request: Request, city: str = Form(...), session: AsyncSession=Depends(get_session)):
    try:
        repo = QueryRepo(session)
        res = await get_weather_from_api(city)
        await repo.save_query(city, res.model_dump())
        return templates.TemplateResponse("weather.html", {"request": request, "city": city, "temperature": res.temperature, "description": res.weather_description})
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error_code": 404, "error_message": "Не удалось получить данные о погоде."},
            status_code=status.HTTP_404_NOT_FOUND
        )

    
@weather_router.get("/history", response_class=HTMLResponse)
async def get_query_history(request: Request, session: AsyncSession=Depends(get_session)):
    try:
        repo = QueryRepo(session)
        res = await repo.get_history()
        return templates.TemplateResponse("history.html",  {"request": request, "history": res})
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error_code": 404, "error_message": "Не удалось получить историю запросов."},
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    