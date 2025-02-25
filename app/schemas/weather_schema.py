from pydantic import BaseModel,  ConfigDict

class WeatherOut(BaseModel):
    weather_description: str
    temperature: float

    model_config = ConfigDict(from_attributes=True)
