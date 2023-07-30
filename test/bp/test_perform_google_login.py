from typing import Final
from unittest.mock import AsyncMock
from unittest.mock import Mock

import pytest

from bp.perform_google_login import PerformGoogleLogin


USER_ID: Final = "anyuserid"
LOGIN_CALLBACK_ENDPOINT: Final = "/login/callback"
SUCCESS_RESPONSE: Final = True
REQUEST_URI: Final = "https://examplerequesturi.com"
LOCAL_SSL_URL: Final = "https://127.0.0.1:5000"
PROVIDER_CONFIG: Final = {
    "issuer": "https://accounts.google.com",
    "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
    "device_authorization_endpoint": "https://oauth2.googleapis.com/device/code",
    "token_endpoint": "https://oauth2.googleapis.com/token",
    "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
    "revocation_endpoint": "https://oauth2.googleapis.com/revoke",
    "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
    "response_types_supported": [
        "code",
        "token",
        "id_token",
        "code token",
        "code id_token",
        "token id_token",
        "code token id_token",
        "none",
    ],
    "subject_types_supported": ["public"],
    "id_token_signing_alg_values_supported": ["RS256"],
    "scopes_supported": ["openid", "email", "profile"],
    "token_endpoint_auth_methods_supported": [
        "client_secret_post",
        "client_secret_basic",
    ],
    "claims_supported": [
        "aud",
        "email",
        "email_verified",
        "exp",
        "family_name",
        "given_name",
        "iat",
        "iss",
        "locale",
        "name",
        "picture",
        "sub",
    ],
    "code_challenge_methods_supported": ["plain", "S256"],
    "grant_types_supported": [
        "authorization_code",
        "refresh_token",
        "urn:ietf:params:oauth:grant-type:device_code",
        "urn:ietf:params:oauth:grant-type:jwt-bearer",
    ],
}
AUTHORIZATION_ENDPOINT_KEY: Final = "authorization_endpoint"
USER_SCOPE: Final = ["openid", "email", "profile"]


class ShouldPerformGoogleLoginSuccessfully:
    def given(self):
        self.google_repository = AsyncMock()
        self.web_applicationt_client = Mock()
        self.lambda_host = LOCAL_SSL_URL
        self.google_repository.get_google_provider_cfg = AsyncMock(
            return_value=PROVIDER_CONFIG
        )
        self.web_applicationt_client.prepare_request_uri = Mock(
            return_value=REQUEST_URI
        )
        self.perform_google_login_use_case = PerformGoogleLogin(
            self.google_repository, self.lambda_host, self.web_applicationt_client
        )

    async def when(self):
        self.response = await self.perform_google_login_use_case.run_use_case()

    def then(self):
        assert self.response
        self.google_repository.get_google_provider_cfg.assert_called()
        self.web_applicationt_client.prepare_request_uri.assert_called_with(
            PROVIDER_CONFIG[AUTHORIZATION_ENDPOINT_KEY],
            redirect_uri=self.lambda_host + LOGIN_CALLBACK_ENDPOINT,
            scope=USER_SCOPE,
        )


@pytest.mark.asyncio
async def test_perform_google_login():
    test = ShouldPerformGoogleLoginSuccessfully()
    test.given()
    await test.when()
    test.then()
