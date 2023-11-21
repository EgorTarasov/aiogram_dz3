from . import models
import datetime as dt
from aiogram import types
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(session: AsyncSession, user: types.User) -> models.User:
    # stmt = select(models.User).where(models.User.id == user.id)
    db_user: models.User | None = await session.get(models.User, user.id)
    if db_user:
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.username = user.username
        db_user.language_code = user.language_code
        db_user.is_bot = user.is_bot
        db_user.is_premium = user.is_premium
        db_user.supports_inline_queries = (
            user.supports_inline_queries if user.supports_inline_queries else False
        )
    else:

        db_user = models.User(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            language_code=user.language_code,
            is_bot=user.is_bot,
            is_premium=user.is_premium,
            supports_inline_queries=user.supports_inline_queries,
        )
        session.add(db_user)
    await session.commit()
    return db_user


async def get_daily_fact(
    session: AsyncSession, user: models.User
) -> models.Fact | None:
    stmt = sa.select(models.Fact).where(models.Fact.type == "daily")
    # if await user.additional_info and await user.additional_info.birth_date:
    #     age = dt.datetime.now().year - user.additional_info.birth_date.year
    #     stmt = stmt.where(models.Fact.age <= age)
    fact: models.Fact | None = (await session.execute(stmt)).scalar_one_or_none()
    return fact


async def get_historical_fact(session: AsyncSession, user: models.User) -> models.Fact:
    stmt = sa.select(models.Fact).where(models.Fact.type == "historical")
    # if await user.additional_info and await user.additional_info.birth_date:
    #     age = dt.datetime.now().year - user.additional_info.birth_date.year
    #     stmt = stmt.where(models.Fact.age <= age)
    return (await session.execute(stmt)).scalar_one_or_none()


async def get_scientific_fact(session: AsyncSession, user: models.User) -> models.Fact:
    stmt = sa.select(models.Fact).where(models.Fact.type == "scientific")
    # if await user.additional_info and await user.additional_info.birth_date:
    #     age = dt.datetime.now().year - user.additional_info.birth_date.year
    #     stmt = stmt.where(models.Fact.age <= age)
    return (await session.execute(stmt)).scalar_one_or_none()
