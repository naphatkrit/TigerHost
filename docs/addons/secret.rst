.. _addons/secret:

The :code:`secret` Addon
==========================


================  =============
Config Variable   Value
================  =============
SECRET_KEY        symmetric secret key
================  =============


The :code:`secret` addon creates a cryptographically secure string suitable for use a symmetric secret key. The string is chosen from :code:`[a-zA-Z0-9]` and is 100 characters long, resulting in ~585 bits of entropy.

The secret is not stored anywhere on TigerHost (except on the app's config variable).
