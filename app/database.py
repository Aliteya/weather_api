from .core import settings
from .models import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(settings.get_url(), echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db_connections():
    try:
        await engine.dispose()
        print("Соединения с базой данных успешно закрыты!")
    except Exception as e:
        print(f"Ошибка при закрытии соединений: {e}")

AsyncSessionLocal=sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session