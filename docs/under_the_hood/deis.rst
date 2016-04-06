.. _under_the_hood/deis:

Deis
=====
`Deis <http://deis.io/>`_ is an open-sourced PaaS project based on Docker that aims to provide the same experience as Heroku. In fact, it more or less does provide everything that TigerHost provides, with the big exception of an addon system.

At the time of this writing, Deis is the backend used in TigerHost. Deis is chosen because it has very similar goals to TigerHost, has great documentation, and is one of the few projects that advertises itself as and looks production ready. However, as stated in :ref:`under_the_hood/paas_backends`, TigerHost talks to its backend(s) using a specified set of API, so it should be easy enough to change to different backend if need be.

.. _under_the_hood/deis//good:
What's Good
--------------
- State of the art documentation, no other way to describe it.
- Detailed instructions on how to deploy on AWS and many other servers.
- It not only supports Heroku buildpacks, but supporting Heroku buildpacks is its primary goal.
- Actively maintained.

.. _under_the_hood/deis//limitations:
Known Limitations
-------------------

- While Deis supports running commands in a deployed container, it does not support running interactive commands. This means that we cannot launch an interactive shell, unlike Heroku. There are more discussions on this `here <https://github.com/deis/deis/issues/117>`_.
- Deis does not do proper escaping on environmental variables/config vars. Therefore, do NOT put shell-reserved-characters into environmental variables (e.g. `, ', ", $). Doing so causes the pre-receive hook on git to fail, meaning a deploy is not possible.
- I have seen an issue where deleting an app and creating a new app with the same name causes :code:`tigerhost run` to start outputing commands from previous runs. The one time this did happen, I was able to fix it by calling :code:`tigerhost run` many times to exhaust the buffer. This happened at the same time as the previous issue of environmental variables escaping, so they may be related.
