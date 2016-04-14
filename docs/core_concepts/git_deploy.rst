.. _core_conepts/git_deploy:

Git Deployment
=================

TigerHost uses the familiar interface of git for deployment. Of course, this means that you have to be using git to deploy on TigerHost. You don't have to be proficient in ``git`` to deploy on TigerHost - the :ref:`getting started tutorial <getting_started>` will show you all the commands you need.

.. _core_concepts/git_deploy//push:

Git Push to Deploy
---------------------
Each app is given a git remote URL, and the URL is stored as the remote "tigerhost" in your git repository on app creation. To deploy, simply push to this remote (:code:`git push tigerhost master`). You don't even have to interact with the TigerHost CLI tool!

.. _core_concepts/git_deploy//project_per_repo:

A Project Per Repo
-------------------
It is best practice to only use the git repo for the specific web app you are deploying. For example, if you are writing an API server with a command-line client, you must make sure that the server and the client each have their own repositories. Otherwise, every time you deploy, your client code will be needlessly cloned, slowing down deployment. Or, if your project contains several web apps, and they cannot be deployed together, they must each be contained on a separate repository, and deployed through a separate TigerHost project.
