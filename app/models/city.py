from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
# from .weather_query import WeatherQuery

class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    queries: Mapped[List["WeatherQuery"]] = relationship(back_populates="city")
