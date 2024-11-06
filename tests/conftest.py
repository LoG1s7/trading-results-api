import logging
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Result, sql
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from models import SpimexTradingResults
from src.app import app
from src.models.base import Base
from src.routers.trading_results import get_db
from src.settings.config import settings
from tests.fixtures import TRADING_RESULTS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/"
)
TEST_DATABASE_URL = f"{DATABASE_URL}{settings.DB_NAME}"


@pytest.fixture(scope="function", autouse=True)
def initialize_cache():
    FastAPICache.init(InMemoryBackend(), prefix="test-cache")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_test_db():
    """Создает тестовую базу данных на время тестов."""
    assert settings.MODE == "TEST"
    sqlalchemy_database_url = (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/"
    )
    nodb_engine = create_async_engine(
        sqlalchemy_database_url,
        echo=False,
        future=True,
    )
    db = AsyncSession(bind=nodb_engine)

    db_exists_query = sql.text(
        f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.DB_NAME}'"
    )
    db_exists: Result = await db.execute(db_exists_query)
    db_exists = db_exists.fetchone() is not None
    autocommit_engine = nodb_engine.execution_options(isolation_level="AUTOCOMMIT")
    connection = await autocommit_engine.connect()
    if not db_exists:
        db_create_query = sql.text(f"CREATE DATABASE {settings.DB_NAME}")
        await connection.execute(db_create_query)

    yield

    db_drop_query = sql.text(f"DROP DATABASE IF EXISTS {settings.DB_NAME} WITH (FORCE)")
    await db.close()
    await connection.execute(db_drop_query)
    await connection.close()
    await nodb_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Создаёт тестовый движок."""
    logger.info("Создание тестового движка базы данных")
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)

    try:
        yield test_engine
    finally:
        await test_engine.dispose()
        logger.info("Тестовый движок базы данных закрыт")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db(test_engine: AsyncEngine):
    """Пересоздаёт таблицы перед каждым тестом."""
    async with test_engine.begin() as conn:
        logger.info("Пересоздание таблиц в тестовой базе данных")
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Таблицы пересозданы")


@pytest_asyncio.fixture
async def async_session_maker(test_engine: AsyncEngine) -> async_sessionmaker:
    """Создаёт async_sessionmaker."""
    logger.info("Создание async_sessionmaker")
    async_session_maker = async_sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )

    yield async_session_maker


@pytest_asyncio.fixture
async def session(
    async_session_maker: async_sessionmaker,
) -> AsyncGenerator[AsyncSession, None]:
    """Предоставляет новую сессию для каждого теста."""
    logger.info("Создание новой сессии")
    async with async_session_maker() as session:
        yield session
    logger.info("Сессия закрыта")


@pytest_asyncio.fixture
async def client(
    async_session_maker: async_sessionmaker,
) -> AsyncGenerator[AsyncClient, None]:
    """Возвращает клиент для тестирования эндпоинтов FastAPI с переопределённой зависимостью get_db."""

    async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    transport = ASGITransport(app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.pop(get_db, None)


@pytest_asyncio.fixture
async def setup_trading_results(async_session_maker: async_sessionmaker):
    """Фикстура для добавления тестовых данных в базу данных."""
    logger.info("Добавление тестовых данных в базу данных")
    async with async_session_maker() as session:
        async with session.begin():
            for data in TRADING_RESULTS:
                trading_result = SpimexTradingResults(**data)
                session.add(trading_result)
    logger.info("Тестовые данные успешно добавлены")
