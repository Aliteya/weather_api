from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .weather_details import WeatherDetail


class WeatherHistory(Base):
    __tablename__ = "weather_history"

    query_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    city_name: Mapped[str] = mapped_column(nullable=False)
    query_timestamp: Mapped[datetime] = mapped_column(nullable=False, server_default='NOW()')

    detail: Mapped[WeatherDetail] = relationship(back_populates="weather_details") 

