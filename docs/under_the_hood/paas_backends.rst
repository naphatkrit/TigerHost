.. _under_the_hood/paas_backends:

Platform-as-a-Service (PaaS) Backends
======================================

.. _under_the_hood/paas_backends//responsibility:

Responsibility
---------------
PaaS backends are responsible for actually hosting apps with high availability. This is a complex layer. When we started TigerHost, we decided that it was infeasible to develop this layer at the same time as more user-experience-oriented features, such as developing a good command-line client and an addons system. Fortunately, there are multiple open-sourced projects dedicated to solving just the problem of hosting apps. As long as a project satisfies a specified API, it can serve as a PaaS backend.

.. _under_the_hood/paas_backends//backend_api:

The Backend API
----------------
A PaaS project is compatible with TigerHost if a backend client can be created for it. This means that a subclass of both :py:class:`BaseClient <api_server.clients.base_client.BaseClient>` and :py:class:`BaseAuthenticatedClient <api_server.clients.base_authenticated_client.BaseAuthenticatedClient>` must be created for the new backend, with **all** the functions implemented.

.. autoclass:: api_server.clients.base_client.BaseClient
    :members:
    :noindex:


.. autoclass:: api_server.clients.base_authenticated_client.BaseAuthenticatedClient
    :members:
    :noindex:
