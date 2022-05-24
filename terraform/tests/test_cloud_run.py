import pytest
import tftest
from pathlib import Path


@pytest.fixture
def plan():
    file_path = Path(__file__).resolve()
    base_dir = file_path.parent.parent.parent.absolute()
    tf = tftest.TerraformTest(tfdir="terraform", basedir=base_dir)
    tf.setup()
    return tf.plan(output=True)


def test_outputs(plan):
    """Simple test of the output vars after a terraform plan cmd
    """
    assert plan.outputs['cloud_run_api_image_name'] == f"{plan.variables['prefix']}-cloudrun-api"
