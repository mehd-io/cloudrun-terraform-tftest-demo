"""Simple Cloud Run Client with Auth token"""
import json
import os
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from google.auth.transport import requests
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
from loguru import logger
from requests import Response

CLIENT_TIMEOUT = 60
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]


def get_service_account_file_path(
    gcp_service_account_env: str = "GOOGLE_APPLICATION_CREDENTIALS",
) -> str:
    if gcp_service_account_env in os.environ:
        return os.environ[gcp_service_account_env]
    else:
        raise KeyError(
            f"Please set {gcp_service_account_env} env for auth as service account"
        )


def get_token_credentials_from_service_account(
    target_audience: str, service_account_file: str
) -> service_account.IDTokenCredentials:
    credentials = service_account.IDTokenCredentials.from_service_account_file(
        service_account_file, target_audience=target_audience
    )
    request = requests.Request()
    credentials.refresh(request)
    return credentials


def get_credentials_from_service_account(
    service_account_file: str, scopes: List[str] = SCOPES
) -> service_account.Credentials:
    return service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes
    )


def get_auth_session(token_credentials: service_account.IDTokenCredentials) -> AuthorizedSession:
    return requests.AuthorizedSession(token_credentials)


def request_wrapper(
    method: str,
    route: str,
    auth_session: AuthorizedSession,
    body_json: Optional[Dict[str, Any]] = None,
    query_params: Optional[Dict[str, Any]] = None,
) -> Response:

    body_json = {} if body_json is None else body_json
    query_params = {} if query_params is None else query_params

    route_with_params = (
        f"{route}?{urlencode(query_params)}" if query_params != {} else route
    )

    request_args: Dict[str, Any] = {
        "method": method,
        "url": f"{auth_session.credentials._target_audience}/{route_with_params}",
        "timeout": CLIENT_TIMEOUT,
    }
    request_args["json"] = None if body_json == {} else body_json

    logger.info(f"Performing request {method} on {request_args['url']}")
    response: Response = auth_session.request(**request_args)

    if not response.ok:
        logger.error(
            f"API call failed, got code {response.status_code} and message: {response.text}"
        )
    else:
        logger.info(f"API call succeed {response.text}")

    return response
