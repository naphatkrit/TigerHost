.. _addons:

============
Addons
============

TigerHost addons provide you resources like database as a service. You can add an addon to your app, and the resource will be available as a config var.


Add an Addon
==============

To add an addon, use the command:

.. code-block:: console

    $ tigerhost addons:create <addon_type>

The generated addon will be given a unique, random name. When the resource become available, the relevant config var will be set in your app.

For example, to add the postgres database addon to your app:

.. code-block:: console

    $ tigerhost addons:create postgres

Once the database is available for use, the config var ``DATABASE_URL`` will be set in your app.


Listing Addons
===============

To list addons added to an app, use the command:

.. code-block:: console

    $ tigerhost addons

This will list the addons with their unique names, their types (e.g. postgres), and their current statuses (waiting for provision, ready, etc.).


Waiting for an Addon
=====================

Some addons take a while before they are ready for use (particularly database addons). The TigerHost CLI client can wait for an addon to become available, blocking the terminal window. To do this:

.. code-block:: console

    $ tigerhost addons:wait <addon_name>

``addon_name`` is the unique name assigned to the addon when you added it (you can retrieve it by running ``tigerhost addons``).
This will poll the server every 30 seconds and report the status back to you, stopping once the addon becomes available. To stop waiting, simply use ``ctrl-c``.


Removing an Addon
===================

To remove an addon from your app:

.. code-block:: console

    $ tigerhost addons:destroy <addon_name>

``addon_name`` is the unique name assigned to the addon when you added it (you can retrieve it by running ``tigerhost addons``). Note that this does **not** unset the relevant config var from your app - it may not be safe for us to do that automatically! You should do that yourself. See :ref:`config_vars__unset`.
