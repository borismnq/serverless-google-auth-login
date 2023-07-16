from .use_case import UseCase
from bp.repositories import GoogleRepository


class PerformGoogleLogin(UseCase):
    def __init__(self, google_repository: GoogleRepository):
        self.google_repository = google_repository

    def run_use_case(self) -> str:
        request_uri = self.google_repository.perform_google_login()
        return request_uri
