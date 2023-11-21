import abc
import datetime as dt

from . import models
from core import crud
from sqlalchemy.ext.asyncio import AsyncSession


class FactsRepo(abc.ABC):
    @abc.abstractmethod
    async def get_daily(self, user: models.User) -> models.Fact | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_historical(self, user: models.User) -> models.Fact | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_scientific(self, user: models.User) -> models.Fact | None:
        raise NotImplementedError


class SqlFactsRepo(FactsRepo):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_daily(self, user: models.User) -> models.Fact | None:
        await crud.get_daily_fact(self.session, user)

    async def get_historical(self, user: models.User) -> models.Fact | None:
        await crud.get_historical_fact(self.session, user)

    async def get_scientific(self, user: models.User) -> models.Fact | None:
        await crud.get_scientific_fact(self.session, user)
