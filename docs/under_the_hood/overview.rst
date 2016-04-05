.. _under_the_hood/overview:

Overview
=========

.. image:: /images/tigerhost_components.png

TigerHost is comprised of three main components: the main TigerHost server, at least one PaaS backend, and an addons server. The developer uses the TigerHost CLI tool to communicate with the main server.

.. note::
    This illustration is a simplification. Not all addons live on the addons server. Simple addons, like the :code:`secret` addon, live directly on the TigerHost main server. In the future, we may choose to house some addons separately on their own servers.

In a typical workflow, the CLI tool sends a request for a new app with the main server. Upon receiving this request, the main server decides which PaaS backend to house this app on, and sends back the corresponding git remote URL. The CLI tool then creates a new git remote in the project repository pointing to this URL, allowing the developer to use git to interface directly with the PaaS backend. Optionally, the developer may want to attach a database addon to the new app. The CLI tool sends this request, and the main server routes the request to the addons server. The addons server provisions a new database instance, returns the URL to this instance back to the main server, and the main server in turn communicates this URL to the right PaaS backend to be saved in the app config.
