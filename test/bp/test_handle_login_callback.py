from typing import Final
from unittest.mock import Mock

from bp.handle_login_callback import HandleLoginCallback
from bp.handle_login_callback import HandleLoginCallbackParams


REQUEST_URI: Final = "https://examplerequesturi.com"
CODE: Final = "examplecode"
LOGIN_DATA_DICT: Final = {
    "user": {
        "email": "useremail",
        "email_verified": True,
        "family_name": "Family Name",
        "given_name": "Given Name",
        "locale": "locale",
        "name": "FULL NAME",
        "picture": "picturelink",
        "sub": "subid",
    },
    "tokens": {
        "access_token": "AT",
        "expires_in": 3599,
        "id_token": "idtoken.idtoken",
        "scope": "scope1 scope2",
        "token_type": "Bearer",
    },
}


class ShouldHandleLoginCallbackSuccessfully:
    def given(self):
        self.google_repository = Mock()
        self.google_repository.handle_login_callback = Mock(
            return_value=LOGIN_DATA_DICT
        )
        self.handle_login_callback_use_case = HandleLoginCallback(
            self.google_repository
        )

    def when(self):
        self.response = self.handle_login_callback_use_case.run_use_case(
            HandleLoginCallbackParams(request_url=REQUEST_URI, code=CODE)
        )

    def then(self):
        assert self.response
        self.google_repository.handle_login_callback.assert_called_with(
            REQUEST_URI, CODE
        )
        assert "user" and "tokens" in self.response.keys()


def test_handle_login_callback():
    test = ShouldHandleLoginCallbackSuccessfully()
    test.given()
    test.when()
    test.then()
