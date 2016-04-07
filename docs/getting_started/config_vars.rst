.. _config_vars:

==================
Configuration Variables
==================

Configuration variables are used to store app-specific information that you do not necessarily want to check into the repository, such as server secrets and database URL. Configuration variables are exposed to apps as environmental variables.

Setting Config Vars
====================

To set config vars, use the command:

.. code-block:: console

    $ tigerhost config:set VAR1=value1 VAR2=value2 ...

You can specify as many config vars bindings as you want.


Getting Config Vars
====================

To get the list of config vars for the app, use the command:

.. code-block:: console

    $ tigerhost config


.. _config_vars__unset:

Unsetting Config Vars
======================

To unset config vars, either use ``config:unset``, or set the value of the config var to empty.

These two are equivalent:

.. code-block:: console

    $ tigerhost config:unset VAR1

.. code-block:: console

    $ tigerhost config:set VAR1=
