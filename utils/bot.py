from pickle import dumps as pickle_dumps, loads as pickle_loads
from typing import Optional, Type, Union, Literal, Dict, Any
from uuid import uuid4

from aiogram import MagicFilter, F
from aiogram.filters import Filter
from aiogram.types import CallbackQuery
from redis.asyncio import Redis

redis = Redis(
    db=1
)


class CallbackData:
    def __init__(
            self,
            session: str,
            packed_data: str = None,
            **kwargs
    ):
        self.session = session
        self.data = kwargs
        self.packed = packed_data

    @property
    def attr(self):
        attr_class = type(
            "callback_atte",
            (object,),
            self.data
        )
        return attr_class

    async def pack(self):
        data_len = len(self.session) + 1 + sum(len(key) + len(str(value)) + 1 for key, value in self.data.items())
        if data_len > 64:
            id = str(uuid4())
            id = "ipvenom" + id[7:]
            self.packed = id
            data = pickle_dumps(self)
            await redis.set(id, data)
            return id
        data = (f"{self.session}:" + ":".join(f"{key}:{value}" for key, value in self.data.items())).rstrip(":")
        return data

    @classmethod
    async def unpack(cls, data_from_tg: str):
        if len(data_from_tg) > 64:
            raise TypeError(
                "data_from_tg is too long"
            )
        if data_from_tg.startswith("ipvenom"):
            data = await redis.get(data_from_tg)
            data = pickle_loads(data)
            return data
        session, *data = data_from_tg.split(":")
        data = {data[num]: data[num + 1] for num in range(0, len(data), 2)}
        return cls(session, data_from_tg, **data)

    async def delete(self):
        if self.packed and self.packed.startswith("ipvenom"):
            await redis.delete(self.packed)
            self.packed = None

    @property
    def attrs(self):
        attr_class = type(
            "callback_atte",
            (object,),
            self.data
        )()
        return attr_class

    @classmethod
    def filter(cls, rule: Optional[MagicFilter] = None) -> "CallbackQueryFilter":
        return CallbackQueryFilter(
            callback_data=cls,
            rule=rule
        )

    def auto_filter(self, rule: Optional[MagicFilter] = None) -> "CallbackQueryFilter":

        main_rule = (F.session == self.session)
        if self.data:
            main_rule = main_rule & (F.data == self.data)
        if rule is not None:
            main_rule = rule & main_rule
        return CallbackQueryFilter(
            callback_data=type(self),
            rule=main_rule
        )


class CallbackQueryFilter(Filter):
    __slots__ = (
        "callback_data",
        "rule",
    )

    def __init__(
            self,
            *,
            callback_data: Type[CallbackData],
            rule: Optional[MagicFilter] = None,
    ):
        self.callback_data = callback_data
        self.rule = rule

    def __str__(self) -> str:
        return self._signature_to_string(
            callback_data=self.callback_data.attrs,
            rule=self.rule,
        )

    async def __call__(
            self,
            query: CallbackQuery,
    ) -> Union[Literal[False], Dict[str, Any]]:
        if not isinstance(query, CallbackQuery) or not query.data:
            return False
        try:
            data = await self.callback_data.unpack(query.data)
        except (TypeError, ValueError):
            return False
        if self.rule is None or self.rule.resolve(data):
            print(data.session)
            return {"callback_data": data}
        return False
