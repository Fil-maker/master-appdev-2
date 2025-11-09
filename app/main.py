# Настройка базы данных
import os
import logging
from litestar import Litestar
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from litestar.di import Provide

from app.controllers.user_controller import UserController
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@192.168.1.64/test_db")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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


app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_service": Provide(provide_user_service),
        "user_repository": Provide(provide_user_repository),
    },
    exception_handlers={
        Exception: global_exception_handler
    },
    middleware=[LoggingMiddleware]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level=5)
