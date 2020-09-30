# `cinemasci` python tools
[![Build Status](https://travis-ci.org/cinemascience/cinemasci.svg?branch=master)](https://travis-ci.org/cinemascience/cinemasci)

A set of python tools for reading, writing and viewing Cinema databases

## installation

The latest release of this module is available on `pypi.org`, and you can install it in the normal way, with `pip`:

```
    pip install cinemasci
```

You can also install it locally from source using the `setup.py` file.

## `cinemasci` submodules

- [cdb](doc/cdb.md): Tools for reading, writing and manipulating a cinema database.
- [cis](doc/cis.md): Tools for reading, writing and manipulating *composable image sets*.
- [pynb](doc/pynb.md): A Jupyter notebook viewer for simple databases.
- [server](doc/server.md): A simple server to help view databases, using the `viewers` submodule.
- [viewers](https://github.com/cinemascience/cinema_viewers): Viewers (submodule)

## Creating new Cinema objects

High level Cinema objects can be created with the high level `new()` command, which takes a `typename` and `dict of args` as arguments:

```
import cinemasci

my_database = cinemasci.new("cdb", {"path": "path/to/database.cdb"})
```

## Unit testing

All code shall be committed with unit testing, using python's `unittest` module. All tests shall be run on code commit, with the following command, which will automatically run all files in the testing directory:

```
    python -m unittest discover testing
```

For each submodule included:

1. There shall be a unit testing file in `testing/` named `test_<modulename>.py`
2. All tests are expected to **pass**.

## Coding standards

This project uses coding standards spelled out in [PEP8](https://www.python.org/dev/peps/pep-0008/)

