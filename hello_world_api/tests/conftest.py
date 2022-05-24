from pathlib import Path

import pytest
import tftest
from google.auth.transport.requests import AuthorizedSession

from .cloud_run_client import (
    get_auth_session,
    get_service_account_file_path,
    get_token_credentials_from_service_account,
)

TF_VAR_CLOUD_RUN_URL = "cloud_run_api_url"


@pytest.fixture(name="auth_session", scope="session")
def deploy_api() -> AuthorizedSession:
    """ Deploy the API through terraform code and return the Cloud Run URL and auth session
    """
    file_path = Path(__file__).resolve()
    base_dir = file_path.parent.parent.parent.absolute()
    tf = tftest.TerraformTest(tfdir="terraform", basedir=base_dir)
    tf.setup()
    tf.apply(output=True, tf_non_interactive=True)

    cloud_run_api_url = tf.output().__getitem__(TF_VAR_CLOUD_RUN_URL)

    token_creds = get_token_credentials_from_service_account(
        target_audience=cloud_run_api_url,
        service_account_file=get_service_account_file_path(),
    )
    yield get_auth_session(token_creds)
    tf.destroy(auto_approve=True, tf_non_interactive=True)
