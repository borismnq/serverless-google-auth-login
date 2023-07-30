import logging
import os
from dataclasses import asdict
from typing import Final
from typing import Optional

from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin
from pydantic import BaseModel
from pydantic import Field

from bp import HandleLoginCallback
from bp import HandleLoginCallbackParams
from bp import PerformGoogleLogin
from di import providers

load_dotenv()

# APP ENVS
STAGE: Final = providers.get_app_stage_module()
SUCCESS_STATUS_CODE: Final = 200
FAIL_STATUS_CODE: Final = 500
STATUS_CODE_ALIAS: Final = "statusCode"
BODY_ALIAS: Final = "body"
CODE_ARG: Final = "code"
CODE: Final = "code"
MESSAGE: Final = "message"
EMPTY_BODY: Final = {}
ERROR_ALIAS: Final = "error"
EMPTY_ERROR: Final = ""
# Init Flask
app = Flask(__name__)
app.secret_key = providers.get_app_secret_key_module() or os.urandom(24)

# CORS
# app.config["CORS_HEADERS"] = "Content-Type"
# cors = CORS(app)


class ResponseBody(BaseModel):
    status_code: int = Field(alias=STATUS_CODE_ALIAS)
    body: dict = Field(alias=BODY_ALIAS)
    error: Optional[str] = Field(alias=ERROR_ALIAS, default=None)


@app.route("/login")
# @cross_origin()  # CORS
async def login(
    perform_google_login: PerformGoogleLogin = providers.get_perform_google_login_use_case_module(),
):
    try:
        request_uri = await perform_google_login.run_use_case()
        return redirect(request_uri)
    except Exception as exception:
        logging.error("Fatal error in login", exc_info=True)
        response = ResponseBody.model_construct(
            status_code=FAIL_STATUS_CODE, body=EMPTY_BODY, error=str(exception)
        ).model_dump(by_alias=True)
        return response


@app.route("/login/callback")
# @cross_origin()  # CORS
async def callback(
    handle_login_callback: HandleLoginCallback = providers.get_handle_login_callback_use_case_module(),
):
    status_code = FAIL_STATUS_CODE
    body = EMPTY_BODY
    error = None
    try:
        code = request.args.get(CODE_ARG)
        request_url = request.url
        login_data = await handle_login_callback.run_use_case(
            HandleLoginCallbackParams(request_url, code)
        )
        status_code = SUCCESS_STATUS_CODE
        body = asdict(login_data)
        login_error = login_data.error
        if login_error:
            error = login_error.message
            status_code = login_error.code
    except Exception as exception:
        logging.error("Fatal error in login callback", exc_info=True)
        error = str(exception)
    response = ResponseBody.model_construct(
        status_code=status_code, body=body, error=error
    ).model_dump(by_alias=True)
    return jsonify(response)


if __name__ == "__main__":

    app.run() if STAGE != "local" else app.run(debug=True, ssl_context="adhoc")
