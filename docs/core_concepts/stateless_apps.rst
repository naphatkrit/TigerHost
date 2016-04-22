.. _core_concepts/stateless_apps:

Stateless Apps
=================

In order to deploy on TigerHost, your app needs to be stateless, i.e. it cannot rely on a persistent file system. All states should be pushed out to the environmental variables, also known as config variables. For example, instead of relying that you will have a database running on the same machine as your app, you should store the database URL as an environmental variable, and connect to that URL instead. (TigerHost makes this process easy, see :ref:`core_concepts/addons`)

While this requirement for apps to be stateless may seem limiting, it actually encourages the best practice of not hardcoding the path to resources. It also allows TigerHost to ensure that an instance of your app is always running - if one goes down, a new one can just be started up.

Note that if your project absolutely needs to access the disk directly, not just via a database (most projects don't), it is possible to provide stateless disk access by mounting an NFS partition of remote disk living somewhere else. A possible scenario is if you are writing a WordPress app that handles file uploads by saving them to a specific location on disk.
