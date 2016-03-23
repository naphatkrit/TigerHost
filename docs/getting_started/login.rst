================
Login
================

TigerHost CLI client uses API keys for authentication. Each user has an API key. This key should be kept secret; anyone with your API key can access your account through the CLI client.

Login
=====

To login, run the command:

.. code-block:: console

    $ tigerhost login

This will ask you for your netID, and instructs you to go to a web page and get your API key. This page is protected with CAS, so you will need your Princeton University's credentials to log in. Remember to keep this API key secret.

Your key will be stored in ``.tigerhost/user.json`` and
can be retrieved with:

.. code-block:: console

    $ tigerhost user:info

Logout
======
To log out:

.. code-block:: console

    $ tigerhost logout

This will delete the file ``.tigerhost/user.json``.
