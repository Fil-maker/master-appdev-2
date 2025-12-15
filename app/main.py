# Настройка базы данных
import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from litestar import Litestar
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.controllers.product_controller import ProductController
from app.controllers.user_controller import UserController
from app.rabbit import broker
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.services.order_service import OrderService
from app.services.product_service import ProductService
from app.services.user_service import UserService

load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@192.168.1.64/test_db"
)

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def provide_db_session() -> AsyncSession:
    """Провайдер сессии базы данных"""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    """Провайдер репозитория пользователей"""
    return UserRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    """Провайдер сервиса пользователей"""
    return UserService(user_repository)


async def provide_product_service(product_repository: ProductRepository) -> ProductService:
    """Провайдер сервиса пользователей"""
    return ProductService(product_repository)


async def provide_product_repository(db_session: AsyncSession) -> ProductRepository:
    """Провайдер репозитория пользователей"""
    return ProductRepository(db_session)


async def provide_order_service(order_repository: OrderRepository) -> OrderService:
    """Провайдер сервиса пользователей"""
    return OrderService(order_repository)


async def provide_order_repository(db_session: AsyncSession) -> OrderRepository:
    """Провайдер репозитория пользователей"""
    return OrderRepository(db_session)


def global_exception_handler(request, exc: Exception) -> None:
    """Глобальный обработчик для логирования необработанных исключений"""
    logger.error(f"Unhandled exception in {request.method} {request.url}: {str(exc)}")
    # Позволяем исключению пробрасываться дальше для стандартной обработки Litestar
    raise exc


# Дополнительно: middleware для логирования запросов
from litestar.middleware import MiddlewareProtocol
from litestar.types import ASGIApp, Receive, Scope, Send


class LoggingMiddleware(MiddlewareProtocol):
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            method = scope["method"]
            path = scope["path"]
            logger.info(f"Request: {method} {path}")

        await self.app(scope, receive, send)


# В lifespan Litestar мы запускаем брокера
@asynccontextmanager
async def lifespan(app: Litestar):
    # Запускаем брокера
    await broker.start()
    yield
    # Останавливаем брокера
    await broker.close()


app = Litestar(
    route_handlers=[UserController, ProductController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_service": Provide(provide_user_service, use_cache=True),
        "user_repository": Provide(provide_user_repository),
        "product_service": Provide(provide_product_service, use_cache=True),
        "product_repository": Provide(provide_product_repository),
    },
    exception_handlers={Exception: global_exception_handler},
    middleware=[LoggingMiddleware],
    lifespan=[lifespan]
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level=5)
