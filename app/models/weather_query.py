from .base import Base
from .weather_details import WeatherDetail
from .city import City
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy import ForeignKey

class WeatherQuery(Base):
    __tablename__ = "weather_history"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    query_timestamp: Mapped[datetime] = mapped_column(nullable=False, server_default=text("TIMEZONE('UTC', NOW())"))

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)
    city: Mapped["City"] = relationship(back_populates="queries")

    detail_id: Mapped[int] = mapped_column(ForeignKey("weather_details.id"), nullable=False)
    detail: Mapped["WeatherDetail"] = relationship(back_populates="query")