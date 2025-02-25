from .base import Base
# from .weather_query import WeatherQuery
from sqlalchemy.orm import Mapped, mapped_column, relationship

class WeatherDetail(Base):
    __tablename__ = "weather_details"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    temperature: Mapped[float] = mapped_column(nullable=False)
    weather_description: Mapped[str] = mapped_column(nullable=False)

    query: Mapped["WeatherQuery"] = relationship(back_populates="detail")