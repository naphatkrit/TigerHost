# TigerHost CLI

TigerHost CLI is a tool for developers to interface with TigerHost.

## Project Structure
This project has a very simple structure. It is based on Click, a Python library for writing command-line libraries.

This project also uses two external libraries written by Naphat Sanguansin:

- [click-extensions](https://github.com/naphatkrit/click-extensions) - A set of useful extensions to Click.
- [temp-utils](https://github.com/naphatkrit/temp-utils) - A better interface for dealing with temporary files and folders, based on the built-in `tempfile` module.

## Development
To start developing for TigerHost CLI, in your virtualenv specifically for TigerHost CLI, run:

```
make develop
```
This will install an editable copy of TigerHost CLI into your Python path.

## Run Tests
To run unit tests:

```
py.test
```

To run integration tests:

```
URL=<http://tigerhostapp.com> bin/integration_tests
```
You can replace `http://tigerhostapp.com` with the URL to a local instance of TigerHost.

## Deploy to Pypi
To deploy the current version of the code to Pypi:

1. Update `/tigerhost/__init__.py`, variable `__version__`, appropriately.
2. Run `make deploy`.
