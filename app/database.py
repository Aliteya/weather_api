from .core import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(settings.get_url(), echo=True)

AsyncSessionLocal=sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    pass