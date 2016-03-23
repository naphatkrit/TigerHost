.. _prepare_project:

======================
Prepare Your Project
======================

If you are moving from Heroku, then your project is already ready for TigerHost. You can skip this section.

Depending on how your project is structured, you may need to modify your project to work with TigerHost. This section some general ideas and provides links to tutorials on more specific project structures (django, nodejs, etc.).

.. _prepare_project__core_concept:

Core Concepts
==============
First, let's go over a few core concepts.


.. _prepare_project__core_concept__git:

Git
----
TigerHost is deployed using ``git push``. This means that your project must be living in a ``git`` repository. You don't have to be proficient in ``git`` to deploy on TigerHost - this tutorial will show you all the commands you need. If your project is not currently using ``git``, see :ref:`prepare_project__init_git`.


.. _prepare_project__core_concept__project_per_repo:

A Project Per Repo
-------------------
Each project should have its own repo. Most likely, if you are already using ``git``, you are already doing this. However, if, for example, you are writing an API server with a command-line client, you must make sure that the server and the client each have their own repositories. Otherwise, every time you deploy, your client code will be needlessly cloned.


.. _prepare_project__core_concept__stateless:

Stateless Application
----------------------
TigerHost requires your application to be stateless. This means that your application should not be writing to disk and expect the result to be persistent. This is important because we cannot guarantee that your application will always be started up on the same machine every time you deploy (or every time your app gets restarted due to a machine failure).

If you are using any of the common web modules (django, Flask, NodeJS), most likely, the only state in your application is the database, and most likely, you have a hardcoded database URL. Then, all you have to do is change your app to take this URL from the environmental variables instead. We will have examples of how to do this in the specific project structure guides. You can either host the database yourself, or use one of our database addons - see :ref:`addons`.


.. _prepare_project__init_git:

Initialize a Git Repo
======================
If you are already using ``git``, you can skip this section.

First, create a git repo:

.. code-block:: console

    $ cd /path/to/your/project
    $ git init

You will want to gitignore some compiled files before checking in your
project. In your project folder, create a file called ``.gitignore`` in
your favorite text editor. Add the following lines:

.. code-block:: none

    .DS_Store

Add any more paths that you want to be excluded from version control. For example, if your project is a python project, you will want to add ``*.pyc`` to exclude object files.

Next, you can check in your project.

.. code-block:: console

    $ git add .
    $ git commit -m "initial commit"


Procfile
=========
TigerHost needs to know how to run your project, which is where the ``Procfile`` comes in. This is a file at the root of your project that lists all the types of
processes needed to run your application. Typically, you will just have
one process type: a web process.
If you are already using Heroku, then you
should already have a ``Procfile``, and it is completely compatible with
TigerHost. If not, create a new file ``Procfile`` at the root of your
project and open it up in your favorite text editor. Add the following:

.. code-block:: none

    web: <command to run your project>

The command would be the same command that you type into the console to start your project. For example, if you were using python, and the entry point for your project is ``start_web.py``, you may have the following ``Procfile``.

.. code-block:: none

    web: python start_web.py

For more complicated project, you may have multiple process types, such as a background worker process in addition to a web process. In that case, your ``Procfile`` may look like this:

.. code-block:: none

    web: python start_web.py
    worker: bin/worker.sh


Specific Guides
================

.. toctree::
    :titlesonly:

    specific_projects/prepare_django
