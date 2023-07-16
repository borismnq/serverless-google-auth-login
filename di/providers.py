import os
from typing import Final

from dotenv import load_dotenv
from oauthlib.oauth2 import WebApplicationClient

from bp import HandleLoginCallback
from bp import PerformGoogleLogin
from bp.repositories import GoogleRepository
from data import GoogleRepositoryImp

load_dotenv()

GOOGLE_DISCOVERY_URL: Final = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
LAMBDA_URL_KEY: Final = "LAMBDA_URL"
GOOGLE_CLIENT_ID_KEY: Final = "OAUTH_CLIENT_ID"
GOOGLE_CLIENT_SECRET_KEY: Final = "OAUTH_CLIENT_SECRET"
STAGE_KEY: Final = "STAGE"
LOCAL_SSL_URL: Final = "https://127.0.0.1:5000"
LOCAL_STAGE: Final = "local"
APP_SECRET_KEY: Final = "SECRET_KEY"


def google_client_id_module() -> str:
    google_client_id = str(os.environ.get(GOOGLE_CLIENT_ID_KEY))
    return google_client_id


def get_app_stage_module() -> str:
    stage = str(os.environ.get(STAGE_KEY))
    return stage


def get_app_secret_key_module() -> str:
    secret_key = os.environ.get(APP_SECRET_KEY)
    return secret_key


def google_client_secret_module() -> str:
    google_client_secret = str(os.environ.get(GOOGLE_CLIENT_SECRET_KEY))
    return google_client_secret


def lambda_host_module(get_app_stage_module: str = get_app_stage_module()) -> str:

    lambda_host = (
        LOCAL_SSL_URL
        if get_app_stage_module == LOCAL_STAGE
        else str(os.environ.get(LAMBDA_URL_KEY))
    )
    return lambda_host


def google_discovery_url_module() -> str:
    return GOOGLE_DISCOVERY_URL


def web_applicationt_client_module(
    google_client_id: str = google_client_id_module(),
) -> str:
    web_applicationt_client = WebApplicationClient(google_client_id)
    return web_applicationt_client


def google_repository_module(
    lambda_host: str = lambda_host_module(),
    google_discovery_url: str = google_discovery_url_module(),
    web_applicationt_client: WebApplicationClient = web_applicationt_client_module(),
    oauth_client_id: str = google_client_id_module(),
    oauth_client_secret: str = google_client_secret_module(),
) -> GoogleRepository:
    return GoogleRepositoryImp(
        lambda_host,
        google_discovery_url,
        web_applicationt_client,
        oauth_client_id,
        oauth_client_secret,
    )


def get_perform_google_login_use_case_module(
    google_repository: GoogleRepository = google_repository_module(),
) -> PerformGoogleLogin:
    return PerformGoogleLogin(google_repository)


def get_handle_login_callback_use_case_module(
    google_repository: GoogleRepository = google_repository_module(),
) -> HandleLoginCallback:
    return HandleLoginCallback(google_repository)
