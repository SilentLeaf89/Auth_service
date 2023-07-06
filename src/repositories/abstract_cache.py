from abc import ABC, abstractmethod


class AbstractCache(ABC):
    def __init__(self, client):
        self._client = client

    @abstractmethod
    async def add_denied_token(self, jti: str, user_id: str, expire: int) -> None:
        pass

    @abstractmethod
    async def get(self, token: str) -> str:
        pass

    @abstractmethod
    async def close(self) -> str:
        pass
