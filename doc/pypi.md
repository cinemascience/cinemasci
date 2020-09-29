```
rm -rf dist 
rm -rf cinemasci.egg-info 
python setup.py sdist 
twine upload dist/*
```
