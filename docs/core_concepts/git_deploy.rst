.. _core_conepts/git_deploy:

Git Deployment
=================

TigerHost uses the familiar interface of git for deployment. Of course, this means that you have to be using git to deploy on TigerHost. Each app is given a git remote URL, and the URL is stored as the remote "tigerhost" in your git repository on app creation. To deploy, simply push to this remote (:code:`git push tigerhost master`). You don't even have to interact with the TigerHost CLI tool!
