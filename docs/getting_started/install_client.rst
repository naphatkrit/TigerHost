================================
Install The TigerHost CLI Client
================================

Get pip
=======

If you don’t already have pip on your system, you need to install it.
Follow the official guide
`here <https://pip.pypa.io/en/stable/installing/>`__. Note that even if
your project is not a python project, you still need pip to install the
TigerHost command-line client, since it is distributed using Pypi.

Use virtualenv
==============

If your project is not a python project, you can skip this and just use the global python environment.

It is highly recommended that you use
`virtualenv <https://virtualenv.pypa.io/en/latest/>`__ to manage your
python packages. Here are the recommended steps:

.. code-block:: console

    $ pip install virtualenv virtualenvwrapper
    ...
    $ mkvirtualenv yourproject

Installation
============

Using pip
---------

First, switch to your virtual environment (skip if you are not using virtualenv).

.. code-block:: console

    $ workon yourproject

Now you can install the TigerHost command-line client.

.. code-block:: console

    $ pip install tigerhost

Installing From the Source
--------------------------

An alternative way to using Pypi is to get the source and use pip to
install from there. First, clone the repository:

.. code-block:: console

    $ git clone https://github.com/naphatkrit/TigerHost-Client

Now, install:

.. code-block:: console

    $ cd TigerHost-Client
    $ pip install .
