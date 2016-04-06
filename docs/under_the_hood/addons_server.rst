.. _under_the_hood/addons_server:
The Addons Server
=================

.. _under_the_hood/addons_server//motivation:
Motivation
-----------
In :ref:`under_the_hood/overview`, we talked about a dedicated addons server. Although there is no restriction on where an addon provider live, as long as one can write a subclass of :code:`BaseAddonProvider`, the dedicated addons server is motivated by cost and scale.

Consider the case of a PostgreSQL addon. A very reasonable implementation is to provision a number of machines from `Amazon Relational Database Service (AWS RDS) <https://aws.amazon.com/rds/>`_. RDS creates machines dedicated to running a specific database engine. Each new addon can just be a different database on one of these machines, and as the number of addons increase, we can provision more machines.

.. image:: /images/addon_rds.png

This approach works well enough, if the only kind of addon we ever want in our system is a PostgreSQL addon. Otherwise, this breaks down quickly. Suppose that we also want a MySQL addon provider. Suppose further that there is exactly one developer who insists on using a MySQL database. In that scenario, we will end up provisioning a whole machine for just a single database, which is extremely inefficient. Furthermore, this model only works for databases supported by RDS. What if we want a queueing service addon, like RabbitMQ, or a key-value store addon, like Redis? We don't want to have to reengineer a separate solution for those kinds of addons. Clearly, we need a better solution that scale better across the different types of addons.

.. _under_the_hood/addons_server//docker:
A Docker-Based Solution
--------------------------
To engineer a standardized way to run addon providers, we turn to Docker. `Docker <https://www.docker.com/>`_ allows us to run tasks as containers (think of them as lightweight VMs). We can provision a general-purpose `Amazon Elastic Compute Cloud (AWS EC2) <https://aws.amazon.com/ec2/>`_ to serve as our Docker host. If we want, say, a PostgreSQL addon, we can simply bring up a new container for each addon we want based on the `official PostgreSQL Docker image <https://hub.docker.com/_/postgres/>`_. If we want a RabbitMQ addon, we can bring up a new container based on the `official RabbitMQ Docker image <https://hub.docker.com/_/rabbitmq/>`_. This delegates the responsibility of ensuring CPU and memory fairness to Docekr.

Does this solution scale to multiple machines, if it needs to? While there is nothing stopping us from doing something similar to RDS and provisioning more EC2 instances to serve as more Docker hosts, Docker itself provides a better solution in terms of Docker Swarm. `Docker Swarm <https://docs.docker.com/swarm/>`_ binds together multiple machines and have them serve as one logical Docker host, simplifying our logic. As of this writing, however, we have not had a need to scale to multiple machines.

A missing piece in this picture is how external machines can connect to these containers. Again, consider PostgreSQL. A PostgreSQL server is typically run on port 5432. However, if we have multiple PostgreSQL containers, each acting as PostgreSQL server, we can't very well expose all of them at port 5432. A possible solution is to assign a randomized port to each container, but this means the system will break after we have more than 65535 addons (maximum number of TCP ports).

The solution we came up with is to have a special container that acts as a TCP proxy. This container will know how to talk the PostgreSQL protocol and will run on port 5432. Upon receiving a request from a PostgreSQL client, it figures out the username and uses that as the name of the container to connect to. That is, the request :code:`postgres://username:password@host:5432/db_name` gets translated to :code:`postgres://username:password@username:5432/db_name`, where :code:`username` is also the container name. Docker will make sure that the host name :code:`username` maps to the appropriate container's IP address.

.. image:: /images/addon_proxy.png

This same process is repeated for whatever types of addons we want to support. While having to implement each protocol may sound troubling, we only have to do it until we get an identifying information, like the username. In a lot of cases, this will be the first message sent by the client. The source code for this proxy server is at `/proxy/ <https://github.com/naphatkrit/TigerHost/tree/master/proxy>`_.

TODO do we want to talk about performance? It makes sense if this were a report, but not so if this were a dev documentation

Finally, the class :code:`DockerAddonProvider` as a subclass of :code:`BaseAddonProvider` that provisions a new addon by creating a container on a specified Docker host, and computing the URL in the format that the proxy container expects.
