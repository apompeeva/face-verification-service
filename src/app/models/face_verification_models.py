import datetime
from typing import Annotated

from sqlalchemy import DateTime, ForeignKey, Integer, MetaData, String, Table, text
from sqlalchemy.orm import Mapped, mapped_column, registry

from app.database import Base, sync_engine

metadata = MetaData()


class FaceDataModel(Base):
    """Модель для таблицы faces."""

    __tablename__ = 'faces'
    __table_args__ = {'schema': 'face_verification_schema'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('auth_schema.users.id'))
    vector: Mapped[str] = mapped_column(String(length=1024))
    path_to_image: Mapped[str] = mapped_column(String(length=1024))
    creation_time: Mapped[Annotated[datetime.datetime, mapped_column(
        DateTime(timezone=True), server_default=text("TIMEZONE('utc', now())"),
    )]]


mapper_registry = registry()

users_table = Table(
    'users',
    Base.metadata,
    autoload_with=sync_engine,
    schema='auth_schema',
)


class Users:
    """Класс для маппинга таблицы users."""

    pass


mapper_registry.map_imperatively(Users, users_table)
