# TigerHost Deployment CLI

TigerHost Deployment CLI is a tool for easily bringing up an instance of TigerHost on AWS. It assumes that you have configured your AWS credentials somehow (the easiest way is to run `aws configure`).

## Project Structure
This project has a very simple structure. It is based on Click, a Python library for writing command-line libraries.

This project also uses two external libraries written by Naphat Sanguansin:

- [click-extensions](https://github.com/naphatkrit/click-extensions) - A set of useful extensions to Click.
- [temp-utils](https://github.com/naphatkrit/temp-utils) - A better interface for dealing with temporary files and folders, based on the built-in `tempfile` module.

This project also depends on the TigerHost CLI for its git library. This is not refactored into a separate library because the library was taken from another open-sourced project.

## Development
To start developing for TigerHost Deployment CLI, in your virtualenv specifically for TigerHost CLI, run:

```
make develop
```
This will install an editable copy of TigerHost Deployment CLI into your Python path.

Note that setting the environmental variable `DEBUG` to anything nonempty will disable communications with AWS, allowing the CLI to do a dry run.

## Run Tests
To run unit tests:

```
py.test
```

## Deploy to Pypi
To deploy the current version of the code to Pypi:

1. Update `/deploy/__init__.py`, variable `__version__`, appropriately.
2. Run `make deploy-pypi`.
