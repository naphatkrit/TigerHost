# TigerHost
A PaaS service for Princeton

Originally developed by: Naphat Sanguansin

Project Advisor: Jérémie Lumbroso

TigerHost is a large project comprised of many smaller projects. First, read the high-level documentation, which lives under /docs. To read it, either go to http://tigerhostapp.com/docs or build the documentation locally by following the README inside /docs.

Having read the high-level documentation, you should be familiar with some of the different components of TigerHost. Each of these components correspond to a subproject in this repo:

| Subproject Directory | Component | Description |
| --- | --- | --- |
| `/client` | CLI Client | This is the command-line client that developers who use TigerHost install. It is a Python [Click](http://click.pocoo.org/6/) project. |
| `/deis` | PaaS Backend (Deis) | This is not really a subproject, but rather a pointer to the Deis git repository. It is a git submodule. |
| `/deploy` | TigerHost Deployment CLI | This is a Python [Click](http://click.pocoo.org/6/) project for deploying TigerHost on AWS. |
| `/docs` | Documentation | This is the source code for the TigerHost documentation. |
| `/nginx` | The Main Server's Nginx Server | This is the actual web server that serves the contents of the main server. This is how we configured http://tigerhostapp.com to point to the main server and http://tigerhostapp.com/docs to the documentation. |
| `/proxy` | Addons Server | The majority of this subproject has to do with the proxy that forwards connections to the appropriate docker containers. |
| `/web` | Main Server | This is a Django project that acts as the main server (everything at the root domain http://tigerhostapp.com). It is a Python [Django](https://www.djangoproject.com/) project. |

If you are new to this project, I recommend taking a look at `/web` first.
