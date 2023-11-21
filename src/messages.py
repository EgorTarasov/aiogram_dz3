from core import models
from aiogram import types
from core import models
import abc


class BaseMessages(abc.ABC):
    @abc.abstractmethod
    def start(self, user: models.User) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def help(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def daily_fact(self, fact: models.Fact) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def historical_fact(self, fact: models.Fact) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def scientific_fact(self, fact: models.Fact) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def settings_birth_date(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def settings_notifications(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def settings_notifications_time(self) -> str:
        raise NotImplementedError

    @abc.abstractclassmethod
    def fact_not_found() -> str:
        raise NotImplementedError


class RegularUser(BaseMessages):
    def start(self, user: models.User) -> str:
        return f"Привет, {user.first_name}!\nДоступный функционал 📚\n /daily - факт дня 🌞\n /historical - исторический факт 🏛️\n /scientific - научный факт 🔬 \n /help - отображение доступных комманд"

    def help(self) -> str:
        return f"Доступный функционал 📚\n /daily - факт дня 🌞\n /historical - исторический факт 🏛️\n /scientific - научный факт 🔬"

    def fact_not_found(self) -> str:
        return f"К сожалению, на сегодня фактов нет 😔"

    def daily_fact(self, fact: models.Fact | None) -> str:
        if not fact:
            return self.fact_not_found()

        message = f"Факт дня 🌞\n\n{fact.title}\n\n{fact.text}"
        if fact.img:
            message += f"\n\n![Image]({fact.img})"
        return message

    def historical_fact(self, fact: models.Fact | None) -> str:
        if not fact:
            return self.fact_not_found()

        message = f"Исторический факт 🏛️\n\n{fact.title}\n\n{fact.text}"
        if fact.img:
            message += f"\n\n![Image]({fact.img})"
        return message

    def scientific_fact(self, fact: models.Fact | None) -> str:
        if not fact:
            return self.fact_not_found()

        message = f"Научный факт 🔬\n\n{fact.title}\n\n{fact.text}"
        if fact.img:
            message += f"\n\n![Image]({fact.img})"
        return message

    def settings_birth_date(self) -> str:
        return f"📅 Введите вашу дату рождения в формате ДД.ММ.ГГГГ"

    def settings_notifications(self) -> str:
        return f"🔔 Хотите ли вы включить уведомления? Введите 'да' или 'нет'."

    def settings_notifications_time(self) -> str:
        return f"⏰ Введите время, в которое вы хотите получать уведомления, в формате ЧЧ:ММ"
