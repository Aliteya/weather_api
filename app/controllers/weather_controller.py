from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..database import get_session
from ..utils import get_weather_from_api
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import WeatherOut, WeatherHistory, WeatherDetailSchema
from ..repository import QueryRepo
 
weather_router = APIRouter(prefix="/weather")

@weather_router.get("/", response_model=WeatherOut)
async def get_weather(city: str="Minsk", session: AsyncSession=Depends(get_session)):
    try:
        repo = QueryRepo(session)
        res = await get_weather_from_api(city)
        await repo.save_query(city, res)
        return WeatherOut(**res)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
@weather_router.get("/history", response_model=List[WeatherHistory])
async def get_query_history(session: AsyncSession=Depends(get_session)):
    try:
        repo = QueryRepo(session)
        res = await repo.get_history()
        return res
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    