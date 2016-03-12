#!/usr/bin/env bash

set -e

# ensures that deis and deisctl are installed
deisctl --version
deis --version

ssh-add ~/.vagrant.d/insecure_private_key
export DEISCTL_TUNNEL=172.17.8.100

(
    cd deis

    # bring up an instance
    make discovery-url # !!IMPORTANT, don't forget to do this everytime
    vagrant up

    # test if everything works
    deisctl list # should not give an error

    # install deis
    deisctl config platform set sshPrivateKey=${HOME}/.vagrant.d/insecure_private_key
    deisctl config platform set domain=local3.deisapp.com
    deisctl refresh-units
    deisctl install platform

    # start deis, takes a while
    deisctl start platform
)
