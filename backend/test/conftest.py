import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import ASGITransport, AsyncClient
from backend.core.config import config as cfg
from sqlmodel import SQLModel
from backend.external.database import get_session
import sys
import asyncio
from backend.main import app


@pytest_asyncio.fixture()
async def async_engine() -> AsyncEngine:
    engine = create_async_engine(url=cfg.TEST_DB_URL, echo=False, pool_pre_ping=True)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture()
async def session(async_engine) -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with Session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="session", autouse=True)
def setup_windows_event_loop():
    """Force Windows to use SelectorEventLoop for psycopg async, safely ignored on AWS Linux."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest_asyncio.fixture(autouse=True)
async def test_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    try:
        yield
    finally:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture()
async def client(session) -> AsyncClient:
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://localhost") as ac:
        yield ac

    app.dependency_overrides.clear()
