# Terraform tftest showcase
This repo is part of a blog post to showcase tftest with an example of two different tests on a simple python API: 
* 1 simple test using a terraform `plan` command
* 1 e2e test that will deploy the api, perform a request, assert the results and destroy the stack

Tech stack : 
* Terraform
* Python 3.10
* Cloud Run (for API runtime)


# How to run the tests
## With VSCode  
Requirements : 
* Docker
* VSCode & [remote-development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

Pick in the palette `>remote-containers:reopen in container`. This will load the dev container image definition located in `./devcontainer/Dockerfile`

Assuming that you have already the rights credentials under `~/.config/gcloud` to a gcp project, authenticate to the Google Container Registry : 
```
make gcloud-docker-auth-cli
```

Then run a simple test using terraform `plan` (`terraform/tests/test_cloud_run.py`) : 
```
make test-infra
```

Run the e2e test (`hello_world_api/tests/test_hello.py`): 
```
make test-api
```

Tested on MacOS M1


