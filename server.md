# Cinema simple web server design

## Requirements

1. The Cinema Simple Web Server can serve up a viewer type and one or more cinema databases using python's `-m <module>` capability.
1. The server can be started from the command line in any directory
1. The server can serve Cinema databases that are accessible (through file permissions) to the user, accessed by a relative path 
1. The server can serve databases that are accessible (through file permissions) to the user, accessed by an absolute path

## Implementation 

### Command Line Args

```
$ python -m cinemasci.cview --help
usage: __main__.py [-h] --data DATA --viewer VIEWER [--port PORT]
                   [--assetname ASSETNAME]

Run a Cinema Viewer

optional arguments:
  -h, --help            show this help message and exit
  --data DATA           database to view
  --viewer VIEWER       viewer type to use
  --port PORT           port to use
  --assetname ASSETNAME
                        asset name to use
```

### Example 

1. Type the following in a shell:

```
    python -m cinemasci.cview --viewer explorer --data data/sphere.cdb --port 8200
    http://127.0.0.1:8200/?viewer=explorer&databases=data/sphere.cdb
```

1. Paste the URL printed into a shell into your favorite browser.


