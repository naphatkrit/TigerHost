.. _under_the_hood/deis:

Deis
=====
`Deis <http://deis.io/>`_ is an open-sourced PaaS project based on Docker that aims to provide the same experience as Heroku. In fact, it more or less does provide everything that TigerHost provides, with the big exception of an addon system. At the time of this writing, Deis is the backend used in TigerHost.

.. _under_the_hood/deis//why:
Why Deis?
-----------
Deis was one of the three projects in consideration at the start of TigerHost. The other two are :ref:`Flynn <under_the_hood/other_backends/flynn>` and :ref:`Tsuru<under_the_hood/other_backends/tsuru>`. Flynn was out of the running early because of its lack of user system and that it is meant to be used by a single system admin as opposed to a group of users. It should be noted that at the beginning, we were looking for a simpler architecture for TigerHost, namely without the main server and exposing the PaaS backend directly. Now that we have the current architecture in place, Flynn *may* have been a better choice (see :ref:`under_the_hood/future_improvements`).

Tsuru almost became the project of choice. this is because it already has a addon-like system in place (that is, it exposes an API similar to the :ref:`addons API <under_the_hood/addons//addons_api>`). However, the documentation is not as thorough as Deis, and it was decided that the cost of re-engineering the addon API is smaller than the cost of dealing with a less thorough documentation.

Deis is chosen because it has very similar goals to TigerHost, has great documentation, and is one of the few projects that advertises itself as and looks production ready. And even if Deis turns out to be the wrong choice (it hasn't so far), TigerHost talks to its backend(s) using :ref:`a specified set of API <under_the_hood/paas_backends//backend_api>`, it is easy enough to switch to a different project.

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
