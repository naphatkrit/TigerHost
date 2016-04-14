.. _future_improvements:

Future Improvements
====================

This section lists some future improvements that we should consider making to TigerHost. They are roughly listed in order of importance, in my (Naphat's) opinions.

- Replace Deis as the backend. Deis has issues as detailed :ref:`here <under_the_hood/deis//limitations>`. We should consider switching to Flynn, as Flynn's shortcomings are mostly irrelevant in our current design. Going a step further, we may consider moving away from Docker-based solutions altogether. Docker does not provide the same level of isolation as a virtual machine. Perhaps a candidate would be LXC.
