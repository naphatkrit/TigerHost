# TigerHost Main Server
This is a [Django](https://www.djangoproject.com/) project.

## Project Structure
Each subfolder in here (aside from `/bin` and `/settings`) is a Django app. The server configuration is in `/settings/dev.py`. (TODO this file should be appropriately renamed once we confirm that the production environment uses the same settings file as the development environment.)

| Django App | Description |
| --- | --- |
| `api_server` | This is the main Django app, where all the APIs are implemented and connections to PaaS backends and addons server happens. |
| `aws_db_addons` | (NOT USED) This implements an addon provider that creates a new AWS RDS database for each addon. |
| `cas` | This is an authentication app that handles CAS. Much of this code is inherited from ReCal. |
| `docker_addons` | This implements an addon provider that talks to the Addons Server (the one based on Docker). |
| `wsse` | This is an authentication app that partially implements the WSSE protocol. It is fully functional, but does not defend against replay attacks. |

## Install Requirements
In a separate virtualenv used exclusively for the main server, run:
```
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

## Run Tests
To run unit tests:
```
py.test
```
To run integration tests, first make sure your database is migrated and fixtures are loaded:
```
python manage.py migrate
python manage.py loaddata api_server/fixtures/test_user.json
```

Then run:
```
bin/integration_tests <DEIS_URL>
```
## Add a New API Endpoint
Every API endpoint is an implementation of `api_server.api.api_base_view.ApiBaseView`. Implement the `get()`, `put()`, `post()`, and/or `delete()` methods as appropriate. Then, edit `api_server.urls` to make the endpoint available.

## Add a New Addon Provider
To add a new kind of addon means to provide an implementation of `api_server.addons.providers.base_provider.BaseAddonProvider`. For examples, take a look at these:

- `api_server.addons.providers.secret_provider.SecretAddonProvider`
- `aws_db_addons.providers.rds_provider.RdsAddonProvider`
- `docker_addons.provider.DockerAddonProvider`

Once you have an implementation of an addon provider, edit the settings file (`settings.dev`), variable `ADDON_PROVIDERS`.

## Add a New PaaS Backend
To add a new PaaS backend means to provide an implementation of `api_server.clients.base_client.BaseClient` and `api_server.clients.base_authenticated_client.BaseAuthenticatedClient`. Note that there will be a login method in `BaseClient` where you will return a `BaseAuthenticatedClient`. For examples, see:

- `api_server.clients.deis_client.DeisClient`

Once you have an implementation of a client, edit the settings file (`settings.dev`), variable `PAAS_BACKENDS`.

If you want to change which backend is the default backend, edit the variable `DEFAULT_PAAS_BACKEND`.
