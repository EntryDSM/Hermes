from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

import aiomysql
import aioredis
import json


class DBConnection(ABC):
    @classmethod
    @abstractmethod
    async def initialize(cls, connection_info): ...

    @classmethod
    @abstractmethod
    async def destroy(cls): ...

    @classmethod
    @abstractmethod
    async def execute(cls, query: str, *args) -> int: ...

    @classmethod
    @abstractmethod
    async def executemany(cls, query: str, *args) -> int: ...

    @classmethod
    @abstractmethod
    async def fetch(cls, query: str, *args) -> List[Dict[str, Any]]: ...

    @classmethod
    @abstractmethod
    async def fetchone(cls, query: str, *args) -> Dict[str, Any]: ...


class CacheConnection(ABC):
    @classmethod
    @abstractmethod
    async def initialize(cls, connection_info): ...

    @classmethod
    @abstractmethod
    async def destroy(cls): ...

    @classmethod
    @abstractmethod
    async def set(cls, key: str, value: Dict[str, Any]) -> None: ...

    @classmethod
    @abstractmethod
    async def get(cls, key: str) -> Dict[str, Any]: ...

    @classmethod
    @abstractmethod
    async def delete(cls, key: str) -> None: ...

