from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from ..models import City, WeatherDetail, WeatherQuery

class QueryRepo():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_query(self, city_name: str, weather: dict):
        try:
            async with self.session.begin():
                result = await self.session.execute(select(City).filter(City.name == city_name))
                city = result.scalars().first()

                if not city:
                    city = City(name=city_name)
                    self.session.add(city)
                    await self.session.flush()
            
                weather_detail = WeatherDetail(
                    temperature = weather["temperature"],
                    weather_description = weather["weather_description"] 
                )

                self.session.add(weather_detail)
                await self.session.flush()

                weather_query = WeatherQuery(city_id=city.id, detail_id=weather_detail.id)

                self.session.add(weather_query)
                await self.session.commit()
        except SQLAlchemyError as e: 
            raise HTTPException(status_code=500, detail="Internal server error")

