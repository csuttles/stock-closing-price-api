#!/bin/bash -x
if [[ $(basename $(pwd)) != "stock-closing-price-api" ]];then
    echo "this must be run from the repository root dir"
    exit 1
fi
# quick and dirty with my own username; in the real world this should be a service account, point to a registry your company manages, etc.
DOCKER_USERNAME="csuttles"
DOCKER_IMAGENAME="stock-closing-price-api"
DOCKER_VERSION="latest"
docker build --tag "${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:${DOCKER_VERSION}" .
