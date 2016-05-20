# Addons Server Proxy

This contains the code for the proxy that lives on the addons server. We have three protocols implemented:

- mongo
- postgres
- redis

## Development
To start developing for this project, in your virtualenv specifically for this project, run:

```
make develop
```
This will install an editable copy of the proxy into your Python path.

`proxy` is also now an executable that will run the proxy.

## Run Tests
To run unit tests:

```
py.test
```
