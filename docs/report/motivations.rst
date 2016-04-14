.. _report/motivations:

Motivations
============

TigerHost is designed for students who want to focus on development and not deployment.

.. _report/motivations//traditional:

Traditional Deployment
------------------------
Traditional deployment is infeasible for any small group of developers and certainly for any student group. In the industry, whole teams are dedicated to figuring out deployment and keeping the system up and running. This is because deployment consists of several daunting tasks and decisions, as outlined below.

First, one must figure out where the project should be deployed. A department-funded project may choose to deploy on a local machine run by the specific department. A more independent project may pick one of the several cloud providers (`Amazon Web Service <https://aws.amazon.com/>`_, `Microsoft Azure <https://azure.microsoft.com/>`_, `Digital Ocean <https://www.digitalocean.com/>`_, etc.).

Additionally, if one goes with a cloud provider, there is an additional task of figuring out how to concisely bringing up the required machines, keeping them up and running, and updating them if required, collectively known as infrastructure management. AWS provides `CloudFormation <https://aws.amazon.com/cloudformation/>`_ for this purpose. There are also platform-agnostic solutions like `Terraform <https://www.terraform.io/>`_. Researching into infrastructure management is overkill for any student projects, as these projects likely only require one machine, yet not doing due diligence here can prove to be fatal later whenever a machine goes down.

Lastly, there is the task of turning a blank machine into a machine capable of running the project, a task known as configuration management. There are two important properties to consider: idempotence and automatic deploys. If the configuration management script is idempotent, then it can be run not only on blank machines, but also machines already running the project. The script figures out the difference between the current state of a machine and the desired state, and then does a series of operations to bring the machine from the current state to the desired state. Idempotence is crucial, as it allows installing a project and updating the project to be one and the same task. Furthermore, one may want automatic deploys. For example, one may want to run the idempotent configuration management script whenever there is a new commit in the master branch of the project repository. This is less crucial for student projects.

There are several solutions to configuration management. A quick and dirty shell script will do, but is neither idempotent (without substantial effort) nor automatic. Alternatively, tools like `Ansible <https://www.ansible.com/>`_, `Chef <https://www.chef.io/>`_, and `Puppet <https://puppet.com/>`_ are idempotent, but are not necessarily automatic. Doing automatic deployment usually involves setting up a separate machine (with Puppet, this is known as the Puppet Master) that will monitor changes to the project and trigger an update on the slave machines (the machines actually running the project).

If every student developer has to go through the traditional deployment tasks, there would be no student apps actually deployed and available for use. Fortunately, there are simpler and better solutions that provide platform-as-a-service (PaaS), one of which is Heroku.

.. _report/motivations//heroku:

Heroku
--------
`Heroku <https://heroku.com>`_ is a PaaS that abstracts away deployment as a Git remote. A deploy is as simple as a Git push, an interface that developers are most likely already familiar with if they version control their projects. In fact, a lot of the most popular projects on campus already use Heroku for deployment, among them being codePost, ReCal, and TigerBook.

The biggest issue with Heroku is cost. Take `ReCal <http://recal.io>`_, a popular course selection service with over 3000 registered users. The ReCal developers pay over $100 per month to use Heroku (about half of that goes into the database, with the other half going into the CPU cost). This is a substantial burden to put on student for what is essentially a service to the community.

As another example, take codePost, an internal website used by the Princeton Computer Science department. The codePost team pays about $250 per month to deploy on Heroku. While codePost may not be a student project, it is a project sponsored by the Computer Science department. What if there is a Heroku-like service that the department can run for not much more monetary cost, while at the same time extending the same benefit to other student-run projects? This is exactly what TigerHost is.

.. _report/motivations//open_sourced:

Existing Open-Sourced PaaS Solutions
---------------------------------
There are existing open-sourced PaaS projects that aim to offer a Heroku-like experience. We will discuss these projects in details later. See :ref:`under_the_hood/deis` and :ref:`under_the_hood/other_backends/index`. TigerHost does not aim to reinvent the wheels. Rather, TigerHost builds on top of these projects and add three major benefits:

- Most of the existing open-sourced projects do not provide a resource-as-a-service solution (Heroku calls this the addon system). This means that users of these projects will be able to deploy stateless apps, but will need to provision and manage stateful resources like databases themselves, and managing these resources is arguably as troublesome as managing a custom infrastructure described :ref:`previously <report/motivations//traditional>`. TigerHost provides an addon system so that student developers can use TigerHost as a one-stop solution.

- TigerHost abstracts away the open-sourced projects under a defined :ref:`API <under_the_hood/paas_backends//backend_api>`, making it a simple task to switch to a different PaaS project if need be.

- TigerHost supports talking to multiple open-sourced projects at the same time, allowing for more flexible setups (such as having a cluster for production and a different cluster for development).
