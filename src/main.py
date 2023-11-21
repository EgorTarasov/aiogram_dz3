"""
7. Бот-фактов:

· Кнопки: "Факт дня", "Исторический факт", "Научный факт".


· Функции: Предоставляет интересные факты.

"Научный факты: -https://spaceflightnewsapi.net"
"""

# Вариант 7
import typing as tp
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart, StateFilter

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis
from sqlalchemy.ext.asyncio import AsyncSession
from core import crud, models
from core.sql import db
from messages import BaseMessages
from middlewares import UserMiddleware
from core import config
from core.repository import FactsRepo
import asyncio

redis = Redis(host=config.redis_host, port=config.redis_port)
STORAGE = RedisStorage(redis=redis)
BOT = Bot(token=config.bot_token)
dp = Dispatcher(storage=STORAGE)
dp.update.middleware(UserMiddleware())
avaliable_facts = ["daily", "historical", "scientific"]


def fact_reply_markup():

    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=f"/{fact}")] for fact in avaliable_facts]
    )


class SettingsForm(StatesGroup):
    birth_date = State()
    notifications = State()
    notifications_time = State()


class FeedbackForm(StatesGroup):
    feedback = State()


@dp.message(CommandStart())
async def start(
    message: types.Message,
    messages: BaseMessages,
    user: models.User,
    session: AsyncSession,
):
    await message.answer(messages.start(user), reply_markup=fact_reply_markup())


@dp.message(Command(prefix="/", commands=["help"]))
async def command_help_handler(message: types.Message, messages: BaseMessages) -> None:
    await message.answer(messages.help(), reply_markup=fact_reply_markup())


@dp.message(Command(prefix="/", commands=avaliable_facts))
async def fact_handler(
    message: types.Message, facts: FactsRepo, user: models.User, messages: BaseMessages
) -> None:

    reply: str = ""
    match message.text:
        case "/daily":
            reply = messages.daily_fact(await facts.get_daily(user))
        case "/historical":
            reply = messages.historical_fact(await facts.get_historical(user))
        case "/scientific":
            reply = messages.scientific_fact(await facts.get_scientific(user))
    await message.answer(reply)


async def main():
    await db.init(crud.models.Base)
    await dp.start_polling(BOT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
