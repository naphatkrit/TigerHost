#!/usr/bin/env bash

set -e

# ensures that deis and deisctl are installed
deisctl --version

ssh-add ~/.ssh/deis

(
    cd deis
    make discovery-url
    (
        cd contrib/aws
        ./provision-aws-cluster.sh
    )
)
