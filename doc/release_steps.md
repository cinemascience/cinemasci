# Release steps

- update version information in repository by editing the following files:
```
    version.md
    cinemasci/__init__.py
    setup.py
```
- push changes to github
- Create a release at github, tagging the version in the normal way.
- `git pull` in local repository, to update tags
- Create release: 
```
    rm -rf dist 
    rm -rf cinemasci.egg-info 
    python setup.py sdist 
```
- Publish on `pypi` **OR**:
```
    twine upload dist/*
```
- Publish on `testpypi` **OR**:
```
    twine upload --repository testpypi dist/*
```

