from abc import ABC
from abc import abstractmethod


class GoogleRepository(ABC):
    @abstractmethod
    def perform_google_login(self) -> str:
        pass

    @abstractmethod
    def handle_login_callback(self, request_url: str, code: str) -> dict:
        pass
