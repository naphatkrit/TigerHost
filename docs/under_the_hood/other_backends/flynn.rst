.. _under_the_hood/other_backends/flynn:

Flynn
=========

`Flynn <https://flynn.io/>`_ is an open-sourced project based on Docker, but unlike Deis (or Heroku), it is much more ambitious. In particular, Flynn aims to be able to deploy anything that can be deployed on a unix system, not just web applications. Flynn has Heroku buildpack support as well.

.. note::
    In hindsight, Flynn may actually be a very good match as a backend. In particular, its limitations are not too relevant given that we are putting TigerHost as an extra layer between Flynn and end-users. So if we run into problems with Deis, we may want to spend time switching to Flynn.

.. _under_the_hood/other_backends/flynn//good:

What's Good
-------------
- Extremely flexible, can run any kind of applications and expose any ports.
  - In particular, it may be possible to run both addons and apps on Flynn.

..  _under_the_hood/other_backends/flynn//bad:

What's Bad
------------
- Not meant as a public cloud. It's meant for a single sysadmin to use to easily deploy apps.
  - This means there is no user system.
  - Apps have access to Flynn API itself. This may not be much worse than other projects, as it seems that Docker itself cannot guarantee much security.
