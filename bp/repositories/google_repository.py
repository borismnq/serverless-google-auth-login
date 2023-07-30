from abc import ABC
from abc import abstractmethod


class GoogleRepository(ABC):
    @abstractmethod
    async def get_google_provider_cfg(self) -> dict:
        pass

    @abstractmethod
    async def get_tokens(self, url: str, headers: dict, body: str) -> dict:
        pass

    @abstractmethod
    async def get_user_info(self, uri: str, headers: dict, body: str) -> dict:
        pass
