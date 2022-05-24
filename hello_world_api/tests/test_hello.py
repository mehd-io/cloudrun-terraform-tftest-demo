import json

import pytest
from google.auth.transport.requests import AuthorizedSession

from .cloud_run_client import request_wrapper


@pytest.mark.integration
def test_health_check(auth_session: AuthorizedSession):
    params = {"auth_session": auth_session, "method": "GET", "route": "/"}
    response = request_wrapper(**params)
    assert response.ok
    assert json.loads(response.text)["message"] == "Hello World"
