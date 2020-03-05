# Cinemagic python tools

A set of python tools for reading, writing and viewing Cinema databases

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

