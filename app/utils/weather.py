import httpx
from ..core import settings 

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
            return resp.json()
        else: 
            return resp.status_code
        
    except Exception as e:
        return {"error": str(e)}
