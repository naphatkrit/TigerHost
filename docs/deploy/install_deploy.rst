.. _deploy/install_deploy:

============================================
Installing TigerHost Deployment CLI
============================================

TigerHost deployment is done via the command-line tool :code:`tigerhost-deploy`, distributed on Pypi.


.. _deploy/install_deploy//prerequisites:

Prerequisites
==============

pip and virtualenv
--------------------
First, you need to have pip installed. Using virtualenv is not required but highly recommended. You can follow the tutorials :ref:`getting_started/install_client//pip` and :ref:`getting_started/install_client//virtualenv`.


AWS CLI
--------
The deployment script is meant to be used for deploying on AWS. To that end, you need to have the AWS CLI installed.

AWS CLI is distributed via Pypi. To install it, switch to your virtual environment (you should have one specifically for TigerHost deployment).

.. code-block:: console

    # if you don't already have a virtual environment for deployment
    $ mkvirtualenv tigerhost-deploy

    # if you already have a virtual environment for deployment
    $ workon tigerhost-deploy

Next, make sure you have your IAM user access key and credentials. If you don't know what that is, follow this `guide <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html#cli-signup>`_.

.. code-block:: console

    $ aws configure
    AWS Access Key ID [None]: ***************
    AWS Secret Access Key [None]: ************************
    Default region name [None]: us-east-1
    Default output format [None]:

.. warning::
    Make sure you put some value for default region. Since we are deploying for Princeton, the recommended value is :code:`us-east-1`.


Docker Toolbox
----------------
Docker is used to deploy the main server and the addons server. You need to have Docker Toolbox installed. The download links are `here <https://www.docker.com/products/docker-toolbox>`_.


.. _deploy/install_deploy//installations:

Installation
============

Using pip
---------
First, switch to your virtual environment (you should have one specifically for TigerHost deployment).

.. code-block:: console

    # if you don't already have a virtual environment for deployment
    $ mkvirtualenv tigerhost-deploy

    # if you already have a virtual environment for deployment
    $ workon tigerhost-deploy

Now you can install the TigerHost command-line client using pip (this is possible because TigerHost is distributed using Pypi).

.. code-block:: console

    $ pip install tigerhost-deploy

Installing From the Source
--------------------------

An alternative way to using Pypi is to get the source and use pip to
install from there. First, clone the repository:

.. code-block:: console

    $ git clone https://github.com/naphatkrit/TigerHost

Now, install:

.. code-block:: console

    $ cd TigerHost/deploy
    $ pip install .
