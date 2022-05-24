#!/usr/bin/env bash

set -e

IMAGE_URL=$1
DOCKER_TAG=$2
GCP_REGION=$3

docker buildx build --platform linux/amd64 -t $IMAGE_URL:$DOCKER_TAG \
            -t $IMAGE_URL:latest \
            -f Dockerfile .. --push
