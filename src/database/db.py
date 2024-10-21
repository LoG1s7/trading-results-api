from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.settings.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
