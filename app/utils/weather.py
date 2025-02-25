import httpx
from ..core import settings 
from fastapi import HTTPException, status

async def get_weather_from_api(city: str):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid":  settings.API_KEY,
        "units": "metric"
    }

    try: 
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            return {"weather_description": weather_description, "temperature": temperature}
        else: 
            error_message = resp.json().get("message", "Unknown error")
            raise HTTPException(status_code=resp.status_code, detail=error_message)
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
