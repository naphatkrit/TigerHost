.. _run_commands:

=====================
Run One-Off Commands
=====================

You can run a command on your deployed app, just like you could when running your project locally. This is useful for things like database migrations and debugging.

.. note::

    You cannot run interactive commands (like a shell). Interactive commands will be given empty inputs. Keep this in mind if your command requires user input.

.. note::

    A known issue is that if a command fails, the output is empty (``stderr`` is not captured). Take a look at the logs to see what is going on. To see how, see :ref:`view_logs`.

To run a command:

.. code-block:: console

    $ tigerhost run [<command>...]

You can assume the working directory to be the root of your project repository. ``command`` is exactly what you would normally run when running your project locally. For example:

.. code-block:: console

    $ tigerhost run echo 1 2 3

For a more serious example, let's say you want to migrate the database of your django project. The command is ``python manage.py migrate``.

.. code-block:: console

    $ tigerhost run python manage.py migrate
