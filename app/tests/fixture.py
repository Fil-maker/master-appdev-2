import os

import pytest
from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Import your actual application components
from app.orm_db import Base  # Replace with your actual Base import
from app.repositories.address_repository import AddressRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.main import app  # Replace with your actual app import

# Test database URL
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@192.168.1.64/test_db")


@pytest.fixture(scope="session")
def engine():
    return create_async_engine(TEST_DATABASE_URL, echo=True)


@pytest.fixture(scope="session")
async def tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session(engine, tables):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
def user_repository(session):
    return UserRepository(session)


@pytest.fixture
def product_repository(session):
    return ProductRepository(session)


@pytest.fixture
def order_repository(session):
    return OrderRepository(session)


@pytest.fixture
def address_repository(session):
    return AddressRepository(session)


@pytest.fixture
def client():
    return TestClient(app=app)
