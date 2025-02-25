from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_session
from ..utils import get_weather_from_api
from sqlalchemy.ext.asyncio import AsyncSession
 
weather_router = APIRouter(prefix="/weather")

@weather_router.get("/")
async def get_weather(city: str="Minsk", session: AsyncSession=Depends(get_session)):
    try:
        res = await get_weather_from_api(city)
        return res
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    