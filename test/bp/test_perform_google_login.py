from typing import Final
from unittest.mock import Mock

from bp.perform_google_login import PerformGoogleLogin


USER_ID: Final = "anyuserid"
SUCCESS_RESPONSE: Final = True
REQUEST_URI: Final = "https://examplerequesturi.com"


class ShouldPerformGoogleLoginSuccessfully:
    def given(self):
        self.google_repository = Mock()
        self.google_repository.perform_google_login = Mock(return_value=REQUEST_URI)
        self.perform_google_login_use_case = PerformGoogleLogin(self.google_repository)

    def when(self):
        self.response = self.perform_google_login_use_case.run_use_case()

    def then(self):
        assert self.response
        self.google_repository.perform_google_login.assert_called()


def test_perform_google_login():
    test = ShouldPerformGoogleLoginSuccessfully()
    test.given()
    test.when()
    test.then()
