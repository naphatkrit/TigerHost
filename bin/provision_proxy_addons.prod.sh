#!/usr/bin/env bash

set -e

MACHINE_NAME=tigerhost-addons-aws

docker-machine create --driver amazonec2 --amazonec2-instance-type t2.large $MACHINE_NAME
eval $(docker-machine env $MACHINE_NAME)

docker-compose -f proxy/docker-compose.prod.yml up -d
mkdir -p web/credentials
cp $DOCKER_CERT_PATH/ca.pem web/credentials/
cp $DOCKER_CERT_PATH/cert.pem web/credentials/
cp $DOCKER_CERT_PATH/key.pem web/credentials/
