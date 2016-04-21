.. _deploy/secret:

Secret Management
====================

As part of the deployment of TigerHost, several secret values will be created. Some of these are:

- main server's symmetric secret key (used by Django)
- the database URL for TigerHost itself
- the :code:`docker-machine`-generated files pertaining to the docker hosts that run the main server and the addons server (this includes the Docker client certifiate files)
- master password for Deis

These must be stored somewhere, but they must not be in the TigerHost repo (as that repo is public). To solve this issue, the :code:`tigerhost-deploy` script puts all secret values into the directory :code:`~/.tigerhost-deploy/secret/`. You can manage this directory however you want, but the recommended method is to use git (and a private repo). If you do decide to use git, there is a shortcut command:

.. code-block:: console

    $ tigerhost-deploy secret [commands]

This gets translated roughly to:

.. code-block:: console

    $ (cd ~/.tigerhost-deploy/secret/ && git [commands])

That is, you can execute git commands to manage your secret from anywhere. Note that if you want to use git command-line options (anything that begins with a :code:`-`, like :code:`-b` in :code:`git checkout -b branch_name`), you will need to add :code:`--` before the options. This is simply an artifact of Click, the python library on which :code:`tigerhost-deploy` is built on.

That is, do this:

.. code-block:: console

    $ tigerhost-deploy secret -- checkout -b branch_name

Do NOT do this:

.. code-block:: console

    $ tigerhost-deploy secret checkout -b branch_name

.. note::
    :code:`--` is a POSIX convention that marks anything that follows it as arguments and not options.
