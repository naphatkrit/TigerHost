.. _future_works:

Future Works
====================

At the time of this writing, TigerHost is a functioning prototype. We were able to deploy `ReCal <http://recal.io>`_, a course selection tool with over 3000 registered users.

Before TigerHost can be considered as "ready for production", the following tasks should be completed. Note that time estimates are under the assumption that the feature is worked on by an IW student willing to put in ~20 hours/week.

- Test TigerHost long-term (over a month). In particular, we have heard of issues with docker hosts having to be restarted once or twice a month. We believe Deis already does the right thing here, but this should be tested. **Estimated time: 1 month**
- Set up monitoring for the different components. **Estimated time: 2 weeks**
- Set up backups for the addons server (the only stateful component of the system). **Estimated time: 2 weeks**

Additionally, below are some tasks that should be tackled but need not be done for the initial release.

- Replace Deis as the backend. Deis has issues as detailed :ref:`here <under_the_hood/deis//limitations>`. We should consider switching to Flynn, as Flynn's shortcomings were significant in our initial design but mostly irrelevant in our current design. **Estimated time: 2 weeks**

    - This will involve augmenting the user system to support sharing of apps. Currently, we rely on Deis to handle this, but Flynn does not have a user system.

- Going a step further, we should consider moving away from Docker-based solutions altogether. Docker does not provide the same level of isolation as a virtual machine. Perhaps a candidate would be LXC. We should also take this opportunity to bring all codebases in house. **Estimated time: 2 months**.
