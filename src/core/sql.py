from asyncio import current_task
from enum import auto
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from .config import config, Config
from .models import Base


class Database:
    def __init__(self, conf: Config, echo: bool = False) -> None:
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{conf.postgres_user}:{conf.postgres_password}@{conf.postgres_host}"
            f":{conf.postgres_port}/{conf.postgres_db}",
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def init(self, base: DeclarativeBase):
        async with self.engine.begin() as conn:
            base.metadata.bind = self.engine
            await conn.run_sync(base.metadata.create_all)

    def get_scoped_session(self):
        return async_scoped_session(self.session_factory, scopefunc=current_task)

    async def get_session(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


db = Database(config)
