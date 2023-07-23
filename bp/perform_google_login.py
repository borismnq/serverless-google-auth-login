from typing import Final

from oauthlib.oauth2 import WebApplicationClient

from .use_case import UseCase
from bp.repositories import GoogleRepository

AUTHORIZATION_ENDPOINT_KEY: Final = "authorization_endpoint"
LOGIN_CALLBACK_ENDPOINT: Final = "/login/callback"
USER_SCOPE: Final = ["openid", "email", "profile"]


class PerformGoogleLogin(UseCase):
    def __init__(
        self,
        google_repository: GoogleRepository,
        lambda_host: str,
        web_applicationt_client: WebApplicationClient,
    ):
        self.google_repository = google_repository
        self.lambda_host = lambda_host
        self.client = web_applicationt_client

    def run_use_case(self) -> str:
        google_provider_cfg = self.google_repository.get_google_provider_cfg()
        request_uri = self.client.prepare_request_uri(
            google_provider_cfg[AUTHORIZATION_ENDPOINT_KEY],
            redirect_uri=self.lambda_host + LOGIN_CALLBACK_ENDPOINT,
            scope=USER_SCOPE,
        )
        return request_uri
