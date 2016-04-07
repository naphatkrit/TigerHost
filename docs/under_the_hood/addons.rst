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


TODO show how the secret addon is implemented.

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
