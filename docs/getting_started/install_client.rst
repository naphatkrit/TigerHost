================================
Install The TigerHost CLI Client
================================

Get pip
=======

If you don’t already have pip on your system, you need to install it.

Pip may installed on Mac OS X using the alternate Python package manager "easy install" that is provided by Apple: :code:`sudo easy_install pip`

On other systems, you may use the installer provided by pip on its `official page <https://pip.pypa.io/en/stable/installing/>`_.

Note that even if
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
    $ echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
    ...
    $ mkvirtualenv yourproject

You may need to change the second command depending on where pip installed virtualenvwrapper. See the output of the installation to confirm. (If you can run :code:`mkvirtualenv`, you are good to go.)

Installation
============

Using pip
---------

First, switch to your virtual environment (skip if you are not using virtualenv).

.. code-block:: console

    $ workon yourproject

Now you can install the TigerHost command-line client using pip (this is possible because TigerHost is distributed using Pypi).

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
