# Release steps

- update version information in repository by editing the following files:
```
    cinemasci/__init__.py
    setup.py
```
- Create a release at github, tagging the version in the normal way.
- Upload release to `pypi.org`:
```
    rm -rf dist 
    rm -rf cinemasci.egg-info 
    python setup.py sdist 
    twine upload dist/*
```

