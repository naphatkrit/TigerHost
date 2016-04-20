.. _getting_started/prepare_project:

======================
Prepare Your Project
======================

If you are moving from Heroku, then your project is already ready for TigerHost. See :ref:`getting_started/prepare_project//heroku`.

Depending on how your project is structured, you may need to modify your project to work with TigerHost. Check if your project is using one of the structures available in our :ref:`specific project guides <getting_started/prepare_project//specific_guides>`. If not, you can follow this section, which discusses general steps applicable to all projects.

You may also want to check out :ref:`core_concepts/index` to understand why these changes are needed.

.. _getting_started/prepare_project//heroku:

Migrating From Heroku
======================
TigerHost is fully compatible with Heroku. In particular, there will be no code change to your project repository. Furthermore, the TigerHost CLI tool is written with Heroku compatibility in mind. A lot of the commands have a counterpart, such as :code:`tigerhost apps` and :code:`heroku apps`. Important commands are discussed in the next :ref:`section <getting_started/deploy_app>`. You can skip to it.

.. _getting_started/prepare_project//specific_guides:

Specific Guides
================

.. toctree::
    :titlesonly:

    specific_projects/prepare_django

.. _getting_started/prepare_project//init_git:

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
