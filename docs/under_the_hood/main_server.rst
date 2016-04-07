.. _under_the_hood/main_server:

The Main TigerHost Server
===========================

.. _under_the_hood/main_server//responsibility:

Responsibility
----------------
The main TigerHost server acts as the interface between developers and TigerHost. Most of the computations do not happen on the main server itself; relevant requests are routed to PaaS backends and the addons server.

There are a couple of reasons why we chose to write the separate server (as opposed to using a PaaS backend as is):

1. Set a standardized interface that PaaS backends to satisfy. Because these backends are most likely going to be based on 3rd party, open-sourced projects, they may not all have the same capabilities. Having a standard interface allows us to very clearly specify what capabilities we want from a 3rd party project.

2. Support many backends. This gives us more flexibility. For example, we may choose to have a "dev" backend with a 3-machine cluster for all students to use for testing, and a "prod" backend with a 5-machine cluster for apps in production to run on. There is also a security aspect. Some 3rd party backends may run really fast and cheap, but does not provide the level of security and isolation that a slower solution may provide. In this case, supporting multiple backends allow us to designate some users as trusted and allow them to run on the faster and cheaper backends.

3. Most 3rd party backends do not have built-in support for addons. By abstracting away the actual backend used to deploy apps, we can add extra features like addons without worrying about compatibility with 3rd party code.


Technology Stack
-----------------
The source code for the TigerHost server is available at `/web/ <https://github.com/naphatkrit/TigerHost/tree/master/web>`_.

The TigerHost server is a Django server. The Django app :code:`api_server` is where most of the TigerHost logic lives. It is the one that receives incoming requests from the TigerHost CLI client and routes them accordingly. :code:`api_server` should be developed purely as an API server. A good heuristic is that it probably shouldn't be rendering HTML pages. If we were to write a web dashboard, for example, the dashboard should be written as a separate Django app.

The TigerHost server is deployed using Docker, as a :code:`docker-compose` project. The project sets up a nginx proxy and serves the Django server from :code:`/`. It also serves this documentation from :code:`/docs/`.

.. TODO link to deployment docs


Authentication
----------------
The canonical authentication method that Princeton uses is `CAS <https://sp.princeton.edu/oit/SDP/CAS/Wiki%20Pages/Home.aspx>`_.

.. image:: /images/cas.png

Unfortunately, CAS is inconvenient to use with a command-line client, which is the primary client of the TigerHost server. A more natural authentication method for command-line clients is one based on an API key. That is, each user is associated with an API key, and as long as the command-line client can prove that it has the key, the server will consider the client authenticated. The actual API key protocol used is `WSSE <https://en.wikipedia.org/wiki/WS-Security>`_, which offers additional security benefits over simply transmitting the key from the client to the server.

How does the client get the API key to begin with? This is where CAS comes in. The API key is exposed at a specific endpoint (:code:`/api/api_key/` at the time of this writing), and that endpoint is protected by CAS.
