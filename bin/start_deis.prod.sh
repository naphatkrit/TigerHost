#!/usr/bin/env bash

set -e

# ensures that deis and deisctl are installed
deisctl --version

ssh-add ~/.ssh/deis

(
    cd deis

    # test if everything works
    deisctl list # should not give an error

    # install deis
    deisctl config platform set sshPrivateKey=~/.ssh/deis
    deisctl config platform set domain=tigerhostapp.com
    deisctl refresh-units
    deisctl install platform

    # start deis, takes a while
    deisctl start platform
)
