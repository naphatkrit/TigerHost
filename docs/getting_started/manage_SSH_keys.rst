=================
Manage SSH Keys
=================

TigerHost, like other similar services, use a Git repository as a mechanism to receive the code base to be deployed. Thus to deploy your code, you will use :code:`git push`. To this end, you will **provide TigerHost with an SSH public key (this key may be generated specifically for TigerHost, and this process is explained in this section)**.

Generating an SSH Key
======================

If you are already using ``git``, chances are, you already have a SSH key generated. To verify, run the following command:

.. code-block:: console

    $ ls ~/.ssh

This will list all the files under your ``~/.ssh`` directory. If you see something like ``id_rsa.pub``, ``id_dsa.pub``, etc. If you see one, **and would like to use the same SSH key (this is not necessary, but recommended if you are not familiar with SSH or git)**, you can skip this section.

To generate a new SSH keypair, run:

.. code-block:: console

    $ ssh-keygen -t rsa -b 4096 -C <your_email@example.com>

Replace ``your_email@example.com`` with your actual email, and follow the prompt. This creates a 4096-bit RSA key.

You will also want to add the key to your SSH agent:

.. code-block:: console

    $ ssh-add ~/.ssh/id_rsa

Adding Your SSH Key to TigerHost
=================================

To add an SSH key to TigerHost, run the command:

.. code-block:: console

    $ tigerhost keys:add <key_name> [<key_path>]

``key_name`` is a name you can associate with this key, so you can recognize it later. This is very useful if you have multiple devices that you run TigerHost on. ``key_path`` is the path to your public key file (ending with ``.pub``). If you do not provide a path, ``~/.ssh/id_rsa.pub`` is used.

Listing Your SSH Keys
=====================

You can list all the keys you have added to TigerHost by running:

.. code-block:: console

    $ tigerhost keys

This will list the key names you chose when adding the key as well as an abbreviated content of the public key.

Removing Your SSH Key from TigerHost
====================================

You can remove your SSH key from TigerHost. To do that, run:

.. code-block:: console

    $ tigerhost keys:remove <key_name>

``key_name`` is the name you chose when you added the key.
