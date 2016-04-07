.. _under_the_hood/addons:

Addons
=======

.. note::
    A note on terminology: an *addon* refers to a resource, such as a database, while an *addon provider* refers to the server on which the database is running on.

.. _under_the_hood/addons//responsibility:
Responsibility
----------------
An addon is responsible for provisioning a new resource for an app, managing the resource life time, and making the resource available via a URL. Anything can become an addon provider as long as it satisfies the addon provider API.

.. _under_the_hood/addons//addons_api:
The Addons API
----------------
Creating a new addon provider is simply a matter of creating a subclass of :code:`BaseAddonProvider`, which has four methods: :code:`begin_provision`, :code:`deprovision`, :code:`get_config`, and :code:`provision_complete`. Note that every method should be non-blocking, i.e. computationally expensive tasks must be done in the background.

.. autoclass:: api_server.addons.providers.base_provider.BaseAddonProvider
    :members:


.. _under_the_hood/addons//case_study_secret:
Case Study: The :code:`secret` Addon
+++++++++++++++++++++++++++++++++++++++
As a case study, let's take a look at how the :code:`secret` addon is implemented. The goal of the :code:`secret` addon is to generate a cryptographically secure symmetric secret key, available as the environmental variable :code:`SECRET_KEY`.

First, import the modules and classes we will need:

.. code-block:: python

    from django.utils import crypto
    from uuid import uuid4

    from api_server.addons.providers.base_provider import BaseAddonProvider

Next, we need to subclass :code:`BaseAddonProvider`.

.. code-block:: python

    class SecretAddonProvider(BaseAddonProvider):

        config_name = 'SECRET_KEY'

        def begin_provision(self, app_id):
            raise NotImplementedError

        def provision_complete(self, uuid):
            raise NotImplementedError

        def get_config(self, uuid):
            raise NotImplementedError

        def deprovision(self, uuid):
            raise NotImplementedError

The :code:`secret` addon does not need to actually bring up any resource; it just needs to generate a random string when setting the config variable.

.. code-block:: python

    ...
    def begin_provision(self, app_id):
        return {
            'message': 'A secret key will be stored into {}.'.format(self.config_name),
            'uuid': uuid4(),
        }
    ...

The key :code:`message` will be displayed to the user. The addon still needs to return a uuid, even if it does not need it to keep track of resources.

Similarly, the method :code:`provision_complete` is meant to check if provision has completed, and if not, return an estimate of how long before the server should check again. In this case, we do not need to provision anything.

.. code-block:: python

    ...
    def provision_complete(self, uuid):
        return True, 0
    ...

Returning :code:`True` implies that provision is complete.

The function :code:`get_config` is where the interesting logic happens. Here, the addon will tell TigerHost what config variable to set.

.. code-block:: python

    ...
    def get_config(self, uuid):
        return {
            'config': {
                self.config_name: crypto.get_random_string(length=100)
            }
        }
    ...

Here, we are setting a random string chosen from [A-Za-z0-9] of length 100 (~585 bits of entropy) to the config variable :code:`SECRET_KEY`.

Lastly, for deprovision, we simply tell the user to unset the config variable themselves (as it may not be safe for us to do it automatically). We did not provision any resources, so there is nothing to clean up.

.. code-block:: python

    ...
    def deprovision(self, uuid):
        return {
            'message': 'Please remove {} from your config manually.'.format(self.config_name)
        }
    ...

.. _under_the_hood/addons//how:

How It Works
---------------
Internally, an addon is represented as a state machine.

.. image:: /images/addon_state_machine.png

There are two terminal states: :code:`deprovisioned` and :code:`error`. Every nonterminal state has a transition to the terminal states. Furthermore, each state is optionally associated with a task responsible for advancing the state.

The :code:`waiting_for_provision` state is associated with a task that checks the state of the addon by calling :code:`provision_complete` on the addon provider. If the provision is complete, then transition accordingly. Otherwise, waits a specified amount of time before trying again.

The :code:`provisioned` state represents an addon whose resource is available, but the appropriate config variable is not yet set in the app. There is a task associated that takes care of that and transitions the addon to :code:`ready`.

The :code:`ready` state is simply an addon that is available and in use by an app. It does not have any task associated with it.

At any time, the user can choose to deprovision an addon, which is why every state has a transition to the :code:`deprovisioned` state. The :code:`deprovisioned` state has a task that kicks off the actual deprovision process by calling :code:`deprovision` on the addon provider. It does not, however, waits for the deprovision to complete, as there is no need to.

Notice that every task are designed to be non-blocking. This is intentional, as the tasks are run in the background by a limited number of `Celery <http://www.celeryproject.org/>`_, shared across all addons. We can guarantee that the addon providers' methods are non-blocking because we control the code.
