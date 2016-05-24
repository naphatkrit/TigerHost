.. _getting_started/deploy_app:

======================
Deploy an App
======================
This document will show you how to deploy an app. Think of an app as a single website. Most projects correspond to exactly one app, but a project may also have multiple apps (say, one for production and one for testing).

Create an App
==============
From inside your project (must be a ``git`` repository), run:

.. code-block:: console

    $ tigerhost create <app_name>

This will also create a new git remote named ``tigerhost`` . This is how
TigerHost keeps track of which app your repo corresponds to. Note that
for any TigerHost commands, you can override this and explicitly specify
which app to use with ``--app <app_name>`` or ``-a <app_name>``.

Deploy
=======

In TigerHost, you deploy with a git push.

.. code-block:: console

    $ git push tigerhost <branch_name>

Typically, the branch you want to push is the master branch.

Your app will be available at ``<app_name>.tigerhostapp.com``.
