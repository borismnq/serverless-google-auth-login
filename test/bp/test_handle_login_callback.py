import json
from typing import Final
from unittest.mock import Mock

from bp.handle_login_callback import HandleLoginCallback
from bp.handle_login_callback import HandleLoginCallbackParams


REQUEST_URI: Final = "https://examplerequesturi.com"
LOCAL_SSL_URL: Final = "https://127.0.0.1:5000"
CODE: Final = "examplecode"
USER_INFO: Final = {
    "email": "useremail",
    "email_verified": True,
    "family_name": "Family Name",
    "given_name": "Given Name",
    "locale": "locale",
    "name": "FULL NAME",
    "picture": "picturelink",
    "sub": "subid",
}
TOKENS: Final = {
    "access_token": "AT",
    "expires_in": 3599,
    "id_token": "idtoken.idtoken",
    "scope": "scope1 scope2",
    "token_type": "Bearer",
}
LOGIN_DATA_DICT: Final = {"user": USER_INFO, "tokens": TOKENS}
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
PREPARE_TOKEN_REQUEST_RESPONSE: Final = "token_url", "headers", "body"
ADD_TOKEN_RESPONSE: Final = "uri", "headers", "body"
TOKEN_ENDPOINT_KEY: Final = "token_endpoint"
DEFAULT_AWS_URL_PREFIX: Final = "/$default"
LOGIN_CALLBACK_ENDPOINT: Final = "/login/callback"
USER_INFO_ENDPOINT_KEY: Final = "userinfo_endpoint"


class ShouldHandleLoginCallbackSuccessfully:
    def given(self):
        self.google_repository = Mock()
        self.web_applicationt_client = Mock()
        self.lambda_host = LOCAL_SSL_URL
        self.google_repository.get_google_provider_cfg = Mock(
            return_value=PROVIDER_CONFIG
        )
        self.google_repository.get_tokens = Mock(return_value=TOKENS)
        self.google_repository.get_user_info = Mock(return_value=USER_INFO)
        self.web_applicationt_client.prepare_token_request = Mock(
            return_value=PREPARE_TOKEN_REQUEST_RESPONSE
        )
        self.web_applicationt_client.parse_request_body_response = Mock(
            return_value=TOKENS
        )
        self.web_applicationt_client.add_token = Mock(return_value=ADD_TOKEN_RESPONSE)
        self.handle_login_callback_use_case = HandleLoginCallback(
            self.google_repository, self.lambda_host, self.web_applicationt_client
        )

    def when(self):
        self.response = self.handle_login_callback_use_case.run_use_case(
            HandleLoginCallbackParams(request_url=REQUEST_URI, code=CODE)
        )

    def then(self):
        assert self.response
        self.google_repository.get_google_provider_cfg.assert_called()
        self.web_applicationt_client.prepare_token_request.assert_called_with(
            PROVIDER_CONFIG[TOKEN_ENDPOINT_KEY],
            authorization_response=REQUEST_URI.replace(DEFAULT_AWS_URL_PREFIX, ""),
            redirect_url=self.lambda_host + LOGIN_CALLBACK_ENDPOINT,
            code=CODE,
        )
        self.google_repository.get_tokens.assert_called_with(
            PREPARE_TOKEN_REQUEST_RESPONSE[0],
            PREPARE_TOKEN_REQUEST_RESPONSE[1],
            PREPARE_TOKEN_REQUEST_RESPONSE[2],
        )
        self.web_applicationt_client.parse_request_body_response.assert_called_with(
            json.dumps(TOKENS)
        )
        self.web_applicationt_client.add_token.assert_called_with(
            PROVIDER_CONFIG[USER_INFO_ENDPOINT_KEY]
        )
        self.google_repository.get_user_info.assert_called_with(
            ADD_TOKEN_RESPONSE[0], ADD_TOKEN_RESPONSE[1], ADD_TOKEN_RESPONSE[2]
        )

        assert "user" and "tokens" in self.response.__dict__


def test_handle_login_callback():
    test = ShouldHandleLoginCallbackSuccessfully()
    test.given()
    test.when()
    test.then()
