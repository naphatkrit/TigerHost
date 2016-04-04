.. _core_concepts/addons:

Addons
=======

As stated in :ref:`core_concepts/stateless_apps`, apps deployed on TigerHost must be stateless, and the best way to do that is to push states out into environmental variables. Take the case of a database. You can store the database URL in, say, the variable :code:`DATABASE_URL`. But where will this database be running? While you can choose to run the database on your own server, if you have your own server, you probably don't need to use TigerHost to begin with. This is why TigerHost offers common resources like database as a service, in the form of addons.

Addons can be provisioned and added to an app via the TigerHost CLI tool, and the relevant environmental variables will be set in your app's config automatically. For example, if you app uses :code:`PostgresSQL`, you can simply create a new :code:`postgres` addon via one simple command, and TigerHost will take care of creating a new database, exposing a URL, and storing that URL in your app's config.
