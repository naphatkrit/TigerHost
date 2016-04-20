.. _addons/postgres:

The :code:`postgres` Addon
==========================


================  =============
Config Variable   Value
================  =============
DATABASE_URL      URL of format :code:`postgres://{user}@{host}:5432/{db_name}`
================  =============

The :code:`postgres` addon provisions a new database for the application to use.

.. warning::
    Keep your database URL secret. Anyone with the URL can access your database.

.. note::
    While it is possible to create new postgres users and/or databases, please do not do so. In particular, the only way to connect to your database instance is via the supplied URL. Even if you create a new user and grant the user access to your database, you cannot connect using the URL :code:`postgres://{new_user}@{host}:5432/{db_name}`. Doing so will fail.
