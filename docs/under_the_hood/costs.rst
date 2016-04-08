.. _under_the_hood/costs:

Costs
======
How much does it cost to run TigerHost? This section discusses the minimal setup.

As discussed throughout :ref:`under_the_hood/index`, TigerHost is comprised of three primary components: the main TigerHost server, a PaaS backend, and an addon server. A minimal setup would require the following setup:

- main TigerHost server - A small machine to run the main server. This can be a cheap machine, as most of the computations do not take place here.
- addon server - This is the tricky part. As of this writing, we do not have a need to turn the addon server into a cluster, so we can rely on one machine for now. The machine should be decently powerful with a lot of RAM, as we will have multiple Docker containers running.
- PaaS backend (using Deis) - 3 machines with at least 8 GB of RAM each. This is simply Deis's minimum requirements.

.. _under_the_hood/costs//aws:

AWS Configurations
--------------------

=============  ==============  =============  =========== ==========
Component      instance type   Cost (hourly)  # Instances Total cost (30.5 days)
=============  ==============  =============  =========== ==========
main server    t2.medium       $0.052         1           $38.07
addon server   t2.large        $0.104         1           $76.13
Deis           m4.large        $0.120         3           $263.52
Total                                                     $377.72
=============  ==============  =============  =========== ==========

.. _under_the_hood/costs//changes:

Potential Changes
------------------
- The main server may not need to be t2.medium. In fact, I suspect t2.small may do.
- The addon server may need to be upgraded to m4.large or turned into a cluster.
- Right now, even the TigerHost database is run on the addon server to save cost. We may want to run this on a dedicated RDS instance.
- These prices are on-demand. Since we will be running TigerHost over a long time, we can switch to a reserved model, which will bring down the cost.
