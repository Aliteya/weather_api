from pydantic import BaseModel,  ConfigDict
from datetime import datetime

class WeatherDetailSchema(BaseModel):
    weather_description: str
    temperature: float

class WeatherHistory(BaseModel):
    city_name: str
    detail: WeatherDetailSchema
    query_timestamp: datetime
