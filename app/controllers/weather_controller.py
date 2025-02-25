from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_session
from ..utils import get_weather_from_api
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import WeatherOut
 
weather_router = APIRouter(prefix="/weather")

@weather_router.get("/", response_model=WeatherOut)
async def get_weather(city: str="Minsk", session: AsyncSession=Depends(get_session)):
    try:
        res = await get_weather_from_api(city)
        return WeatherOut(**res)
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    