import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import WeatherOut, WeatherHistory, WeatherDetailSchema
from app.controllers import weather_router

sys.path.append(str(Path(__file__).parent.parent))

client = TestClient(app)

@pytest.fixture
def mock_get_weather_from_api():
    with patch("app.controllers.weather_controller.get_weather_from_api") as mock:
        mock.return_value = WeatherOut(
            weather_description="Sunny",
            temperature=20.5
        )
        yield mock


def test_get_weather(mock_get_weather_from_api):
    mock_get_weather_from_api.return_value = WeatherOut(
        weather_description="Sunny",
        temperature=20.5
    )

    response = client.post(
        "/weather/get",
        data={"city": "London"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    # Validate the response
    assert response.status_code == 200
    assert "London" in response.text
    assert "20.5" in response.text
    assert "Sunny" in response.text

def test_get_weather_not_found(mock_get_weather_from_api):
    mock_get_weather_from_api.side_effect = Exception("API Error")

    response = client.post(
        "/weather/get",
        data={"city": "InvalidCityName"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 404
    assert "Не удалось получить данные о погоде" in response.text

