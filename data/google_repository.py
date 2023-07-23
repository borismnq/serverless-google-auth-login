import logging
from typing import Final
from typing import Optional

import requests

from bp.repositories import GoogleRepository


ERROR_REQUESTING_ENDPOINT_MSG: Final = (
    "An error occurred while requesting endpoint {endpoint}: {error}"
)


class UnableGoogleProvider(Exception):
    pass


class TokenRequestException(Exception):
    pass


class UserInfoException(Exception):
    pass


class GoogleRepositoryImp(GoogleRepository):
    def __init__(
        self,
        google_discovery_url: str,
        oauth_client_id: str,
        oauth_client_secret: str,
    ):
        self.google_discovery_url = google_discovery_url
        self.oauth_client_id = oauth_client_id
        self.oauth_client_secret = oauth_client_secret

    def get_google_provider_cfg(self) -> dict:
        response: Optional[requests.Response] = None
        provider_config = {}
        try:
            response = requests.get(self.google_discovery_url)
            provider_config = response.json()
        except Exception as exc:
            logging.exception(exc)
            try:
                error = response.json()
            except Exception:
                error = str(exc)
            raise UnableGoogleProvider(
                ERROR_REQUESTING_ENDPOINT_MSG.format(
                    endpoint=self.google_discovery_url,
                    error=error,
                )
            )
        return provider_config

    def get_tokens(self, url: str, headers: dict, body: str) -> dict:
        response: Optional[requests.Response] = None
        tokens = {}
        try:
            response = requests.post(
                url,
                headers=headers,
                data=body,
                auth=(self.oauth_client_id, self.oauth_client_secret),
            )
            tokens = response.json()
        except Exception as exception:
            logging.exception(exception)
            try:
                error = response.json()
            except Exception:
                error = str(exception)
            raise TokenRequestException(
                ERROR_REQUESTING_ENDPOINT_MSG.format(
                    endpoint=url,
                    error=error,
                )
            )
        return tokens

    def get_user_info(self, uri: str, headers: dict, body: str) -> dict:
        response: Optional[requests.Response] = None
        user_info = {}
        try:
            response = requests.get(uri, headers=headers, data=body)
            user_info = response.json()
        except Exception as exception:
            logging.exception(exception)
            try:
                error = response.json()
            except Exception:
                error = str(exception)
            raise UserInfoException(
                ERROR_REQUESTING_ENDPOINT_MSG.format(
                    endpoint=uri,
                    error=error,
                )
            )
        return user_info
