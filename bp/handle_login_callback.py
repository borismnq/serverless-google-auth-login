from dataclasses import dataclass

from .use_case import UseCase
from bp.repositories import GoogleRepository


@dataclass(frozen=True)
class HandleLoginCallbackParams:
    request_url: str
    code: str


class HandleLoginCallback(UseCase):
    def __init__(self, google_repository: GoogleRepository):
        self.google_repository = google_repository

    def run_use_case(self, params: HandleLoginCallbackParams) -> dict:
        login_data_dict = self.google_repository.handle_login_callback(
            params.request_url, params.code
        )
        return login_data_dict
