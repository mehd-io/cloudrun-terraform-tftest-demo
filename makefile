
gcloud-docker-auth-cli:
	gcloud auth configure-docker

test-infra:
	pytest terraform/tests/test_cloud_run.py

test-api:
	pytest hello_world_api/tests/test_hello.py 
