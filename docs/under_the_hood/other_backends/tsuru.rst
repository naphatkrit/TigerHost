.. _under_the_hood/other_backends/tsuru:

Tsuru
========

`Tsuru <https://tsuru.io/>`_ is an open-sourced PaaS project based on Docker. This is the solution we almost went with because it has everything we want (addon system, Heroku interface), but ultimately decided against it because of poor documentation and our own desire to be more flexible by using PaaS backends purely for deployment, not addon.

.. _under_the_hood/other_backends/tsuru//good:

What's Good
-------------
- Autoscaling built-in to Tsuru. That is, Tsuru will provision more machines as needed.
- Ridiculously good support. The Tsuru team replies really quickly, even on weekends.
- Has an addon-like system.
- User system is confusing. There is something known as a role, which gives users permissions. There are two default roles: team-creator and team-member. A team defines who has access to an app. Each app must belong to a team, but a user does not have a default team, so a user must first create a team. I think the Heroku (and Deis) model is to have one team per app, and hide this layer.

.. _under_the_hood/other_backends/tsuru//bad:

What's Bad
-----------
- Poor documentation.
- Along the same line, the instruction for installing is unclear. There is no one script to install Tsuru with all its dependencies, and the instruction does not cover all the dependencies needed.
