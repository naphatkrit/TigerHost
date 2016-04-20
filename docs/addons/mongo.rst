.. _addons/mongo:

The :code:`mongo` Addon
==========================


================  =============
Config Variable   Value
================  =============
DATABASE_URL      URL of format :code:`mongodb://{user}:{password}@{host}:5432/{db_name}`
================  =============

The :code:`mongo` addon provisions a new mongodb database for the application to use.

.. warning::
    Keep your database URL secret. Anyone with the URL can access your database.

.. note::
    While it is possible to create new mongodb users and/or databases, please do not do so. In particular, the only way to connect to your database instance is via the supplied URL. Even if you create a new user and grant the user access to your database, you cannot connect using the URL :code:`mongodb://{new_user}:{new_password}@{host}:5432/{db_name}`. Doing so will fail.
