import logging
import typing as tp
from aiogram import types, BaseMiddleware
from core.repository import SqlFactsRepo

from messages import RegularUser
from core.sql import db
from core import crud


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: tp.Callable[
            [types.TelegramObject, tp.Dict[str, tp.Any]], tp.Awaitable[tp.Any]
        ],
        event: types.Update,
        data: tp.Dict[str, tp.Any],
    ) -> tp.Any:

        if event.message:
            logging.debug(
                f"user: {event.message.from_user.id}:{event.message.from_user.first_name} send: {event.message.text}"
            )

            data["messages"] = RegularUser()
            data["session"] = await anext(db.get_session())
            data["user"] = await crud.create_user(
                data["session"], event.message.from_user
            )
            data["facts"] = SqlFactsRepo(data["session"])
        return await handler(event, data)
