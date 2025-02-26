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

def get_query_repo(session: AsyncSession = Depends(get_session)) -> QueryRepo:
    return QueryRepo(session)

@weather_router.get("/form", response_class=HTMLResponse)
async def get_weather_form(request: Request):
    return templates.TemplateResponse(request=request, name="weather_form.html")

@weather_router.post("/get", response_class=HTMLResponse)
async def get_weather(request: Request, city: str = Form(...), repo: QueryRepo=Depends(get_query_repo)):
    try:
        res = await get_weather_from_api(city)
        await repo.save_query(city, res.model_dump())
        return templates.TemplateResponse(request, "weather.html", context={"city": city, "temperature": res.temperature, "description": res.weather_description})
    except Exception as e:
        return templates.TemplateResponse( 
            request=request,
            name="error.html",
            context={"error_code": 404, "error_message": "Не удалось получить данные о погоде."},
            status_code=status.HTTP_404_NOT_FOUND
        )

    
@weather_router.get("/history", response_class=HTMLResponse)
async def get_query_history(request: Request, repo: QueryRepo=Depends(get_query_repo)):
    try:
        res = await repo.get_history()
        return templates.TemplateResponse(request, "history.html",  {"history": res})
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error_code": 404, "error_message": "Не удалось получить историю запросов."},
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    