import datetime as dt
import sqlalchemy as sa
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    declared_attr,
    relationship,
)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime, default=dt.datetime.utcnow
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow
    )


class User(Base):
    """Модель пользователя телеграма (https://core.telegram.org/bots/api#user)"""

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(32), nullable=True)
    first_name: Mapped[str] = mapped_column(sa.String(32))
    last_name: Mapped[str] = mapped_column(sa.String(32), nullable=True)
    is_bot: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    is_premium: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    supports_inline_queries: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    language_code: Mapped[str] = mapped_column(sa.String(8), nullable=True)

    additional_info: Mapped["AdditionalInfo"] = relationship(
        "AdditionalInfo", back_populates="user"
    )

    def __repr__(self) -> str:
        return f"<User {self.id}>"


class Fact(Base):
    """Модель факта для бота

    type:
        - daily
        - historical
        - scientific
    img:
        - путь к картинке (в статике) или ссылка на картинку
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(256))
    text: Mapped[str] = mapped_column(sa.Text)
    type: Mapped[str] = mapped_column(sa.String(32))
    img: Mapped[str] = mapped_column(sa.String(256), nullable=True)
    age: Mapped[int] = mapped_column(sa.Integer, nullable=True)


class AdditionalInfo(Base):
    """Дополнительная информация о пользователе

    birth_date: Дата рождения пользователя (для цензуры)
    notification: Подписан ли пользователь на уведомления (о новых дневных фактах)
    notifications_time: Время, в которое пользователь хочет получать уведомления
    """

    id: Mapped[int] = mapped_column(sa.ForeignKey(User.id), primary_key=True)
    birth_date: Mapped[dt.date] = mapped_column(sa.DATE)
    notifications: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    notifications_time: Mapped[dt.time] = mapped_column(
        sa.TIME, default=dt.time(hour=12)
    )

    user: Mapped[User] = relationship("User", back_populates="additional_info")


class Feedback(Base):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey(User.id), on_delete="CASCADE")

    text: Mapped[str] = mapped_column(sa.Text)
