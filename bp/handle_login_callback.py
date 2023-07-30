import json
from dataclasses import dataclass
from typing import Final
from typing import Optional

from oauthlib.oauth2 import WebApplicationClient

from .use_case import UseCase
from bp.repositories import GoogleRepository


TOKEN_ENDPOINT_KEY: Final = "token_endpoint"
LOGIN_CALLBACK_ENDPOINT: Final = "/login/callback"
USER_KEY: Final = "user"
TOKENS_KEY: Final = "tokens"
UNAVAILABLE_USER_MSG: Final = "User email not available or not verified by Google."
UNAVAILABLE_CODE: Final = 400
DEFAULT_AWS_URL_PREFIX: Final = "/$default"
USER_INFO_ENDPOINT_KEY: Final = "userinfo_endpoint"
EMAIL_VERIFIED_KEY: Final = "email_verified"
MESSAGE: Final = "code"
ERROR: Final = "error"
EMPTY_STR: Final = ""


@dataclass(frozen=True)
class HandleLoginCallbackParams:
    request_url: str
    code: str


@dataclass(frozen=True)
class Error:
    message: str
    code: str


@dataclass(frozen=True)
class LoginDataResponse:
    user_info: dict
    tokens: str
    error: Optional[Error] = None


class HandleLoginCallback(UseCase):
    def __init__(
        self,
        google_repository: GoogleRepository,
        lambda_host: str,
        web_applicationt_client: WebApplicationClient,
    ):
        self.google_repository = google_repository
        self.lambda_host = lambda_host
        self.client = web_applicationt_client

    async def run_use_case(
        self, params: HandleLoginCallbackParams
    ) -> LoginDataResponse:
        error = None
        google_provider_cfg = await self.google_repository.get_google_provider_cfg()
        token_url, headers, body = self.client.prepare_token_request(
            google_provider_cfg[TOKEN_ENDPOINT_KEY],
            authorization_response=(params.request_url).replace(
                DEFAULT_AWS_URL_PREFIX, EMPTY_STR
            ),
            redirect_url=self.lambda_host + LOGIN_CALLBACK_ENDPOINT,
            code=params.code,
        )
        tokens = await self.google_repository.get_tokens(token_url, headers, body)
        parsed_tokens = self.client.parse_request_body_response(json.dumps(tokens))
        uri, headers, body = self.client.add_token(
            google_provider_cfg[USER_INFO_ENDPOINT_KEY]
        )
        user_info = await self.google_repository.get_user_info(uri, headers, body)
        if not user_info.get(EMAIL_VERIFIED_KEY):
            error = Error(UNAVAILABLE_USER_MSG, UNAVAILABLE_CODE)

        return LoginDataResponse(user_info, parsed_tokens, error)
