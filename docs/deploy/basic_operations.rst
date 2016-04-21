.. _deploy/basic_operations:

Basic Operations
==================

The :code:`tigerhost-deploy` supports three main operations: create, update, and destroy. As discussed in :ref:`under_the_hood/overview`, TigerHost is composed of three components: the main server, the Deis-based PaaS backend, and the addons server. :code:`tigerhost-deploy` commands are of the format:

.. code-block:: console

    $ tigerhost-deploy [component] [command]

For example, :code:`tigerhost-deploy addons create` creates the addons server. There is also the shortcut form:

.. code-block:: console

    $ tigerhost-deploy [command]

Commands of this form automatically calls the appropriate commands for each component. So, :code:`tigerhost-deploy create` will create the Deis cluster, the addons server, and the main server.
