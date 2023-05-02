import asyncio
import pickle
from datetime import timedelta
from typing import Any, Awaitable, Type, Union

from aioredis.client import KeyT, Redis
from aioredis.connection import EncodableT
from pydantic import BaseModel


class RedisClient(Redis):
    def __init__(self, host, port, password):
        if password:
            super().__init__(host=host, port=port, encoding="utf-8", password=password)
        else:
            super().__init__(host=host, port=port, encoding="utf-8")

    async def get(self, name: KeyT, model: Type[BaseModel] = None) -> Any:
        response = await super().get(name=name)
        if response:
            return pickle.loads(response)

    async def set(
        self,
        name: KeyT,
        value: Union[EncodableT, Type[BaseModel]],
        expiration: timedelta = None,
    ) -> Awaitable:
        dumped = pickle.dumps(value)
        return await super().set(name=name, value=dumped, ex=expiration)
