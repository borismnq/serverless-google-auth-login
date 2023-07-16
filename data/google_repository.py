import json
import logging
from typing import Final

import requests
from oauthlib.oauth2 import WebApplicationClient

from bp.repositories import GoogleRepository


ERROR_REQUESTING_ENDPOINT_MSG: Final = (
    "An error occurred while requesting endpoint {endpoint}: {error}"
)
AUTHORIZATION_ENDPOINT_KEY: Final = "authorization_endpoint"
LOGIN_CALLBACK_ENDPOINT: Final = "/login/callback"
USER_SCOPE: Final = ["openid", "email", "profile"]
DEFAULT_AWS_URL_PREFIX: Final = "/$default"
TOKEN_ENDPOINT_KEY: Final = "token_endpoint"
USER_INFO_ENDPOINT_KEY: Final = "userinfo_endpoint"
EMAIL_VERIFIED_KEY: Final = "email_verified"
USER_KEY: Final = "user"
TOKENS_KEY: Final = "tokens"
UNAVAILABLE_USER_MSG: Final = "User email not available or not verified by Google."
UNAVAILABLE_CODE: Final = 400
CODE: Final = "code"
ERROR: Final = "error"


class UnableGoogleProvider(Exception):
    pass


class TokenRequestException(Exception):
    pass


class GoogleRepositoryImp(GoogleRepository):
    def __init__(
        self,
        lambda_host: str,
        google_discovery_url: str,
        web_applicationt_client: WebApplicationClient,
        oauth_client_id: str,
        oauth_client_secret: str,
    ):
        self.lambda_host = lambda_host
        self.google_discovery_url = google_discovery_url
        self.client = web_applicationt_client
        self.oauth_client_id = oauth_client_id
        self.oauth_client_secret = oauth_client_secret

    def perform_google_login(self) -> str:
        google_provider_cfg = self.get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg[AUTHORIZATION_ENDPOINT_KEY]
        redirect_url = self.lambda_host + LOGIN_CALLBACK_ENDPOINT
        request_uri = self.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=redirect_url,
            scope=USER_SCOPE,
        )
        return request_uri

    def get_google_provider_cfg(self):
        json_response = {}
        try:
            response = requests.get(self.google_discovery_url)
            json_response = response.json()
        except Exception as exc:
            logging.exception(exc)
            try:
                error = response.json()  # type: ignore
            except Exception:
                error = str(exc)
            raise UnableGoogleProvider(
                ERROR_REQUESTING_ENDPOINT_MSG.format(
                    endpoint=self.google_discovery_url,
                    error=error,
                )
            )
        return json_response

    def get_tokens(self, token_url: str, headers: dict, body: str) -> dict:
        tokens = {}
        try:
            token_response = requests.post(
                token_url,
                headers=headers,
                data=body,
                auth=(self.oauth_client_id, self.oauth_client_secret),
            )
            self.client.parse_request_body_response(json.dumps(token_response.json()))
            tokens = token_response.json()
        except Exception as exception:
            logging.exception(exception)
            try:
                error = response.json()  # type: ignore
            except Exception:
                error = str(exception)
            raise TokenRequestException(
                ERROR_REQUESTING_ENDPOINT_MSG.format(
                    endpoint=self.google_discovery_url,
                    error=error,
                )
            )
        return tokens

    def handle_login_callback(self, request_url: str, code: str) -> dict:
        google_provider_cfg = self.get_google_provider_cfg()
        token_endpoint = google_provider_cfg[TOKEN_ENDPOINT_KEY]
        redirect_url = self.lambda_host + LOGIN_CALLBACK_ENDPOINT
        token_url, headers, body = self.client.prepare_token_request(
            token_endpoint,
            authorization_response=(request_url).replace(DEFAULT_AWS_URL_PREFIX, ""),
            redirect_url=redirect_url,
            code=code,
        )
        tokens = self.get_tokens(token_url, headers, body)
        userinfo_endpoint = google_provider_cfg[USER_INFO_ENDPOINT_KEY]
        uri, headers, body = self.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if not userinfo_response.json().get(EMAIL_VERIFIED_KEY):
            return {ERROR: UNAVAILABLE_USER_MSG, CODE: UNAVAILABLE_CODE}
        user_info = userinfo_response.json()
        return {USER_KEY: user_info, TOKENS_KEY: tokens}
