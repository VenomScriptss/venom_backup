from enum import Enum as EnumGenerator
from time import time
from typing import List

from sqlalchemy import JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

from db.env import getenv

Base = declarative_base()


class Language(EnumGenerator):
    en = "EN"
    fa = "FA"


class BotSettings(Base):
    __tablename__ = 'bot_settings'
    id: Mapped[int] = mapped_column(
        primary_key=True,
        unique=True,
        default=1,
        index=True
    )
    backup_chat_id: Mapped[int] = mapped_column(
        default=None,
        nullable=True,
        unique=True
    )
    backup_interval: Mapped[int] = mapped_column(
        default=60,
        nullable=False,
        unique=True
    )
    language: Mapped[Language] = mapped_column(
        Enum(Language),
        default=Language.en,
        nullable=False,
        unique=True
    )
    _admins: Mapped[List[int]] = mapped_column(
        JSON,
        default=[],
        nullable=False,
        unique=True
    )

    @property
    def admins(self):
        return self._admins + [getenv("ADMIN_ID")]


class Backup(Base):
    __tablename__ = "backups"
    id: Mapped[str] = mapped_column(
        primary_key=True
    )
    timestamp: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
        unique=False,
        default=time
    )
