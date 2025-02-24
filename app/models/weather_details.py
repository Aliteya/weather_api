from .base import Base
from .weather_history import WeatherHistory
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import text

class WeatherDetail(Base):
    __tablename__ = "weather_details"

    detail_id: Mapped[int] = mapped_column(primary_key=True)
    temperature: Mapped[int] = mapped_column()
    weather_description: Mapped[text] = mapped_column()

    query: Mapped[WeatherHistory] = relationship(back_populates="weather_history")