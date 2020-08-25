from . import cis
from . import cdb
from . import cview

Version = "1.0"

#
# new factory function
#
# creates new objects for a consistent high level interface
#
def new( type, args ):
    result = None
    if type == "cdb":
        if "path" in args:
            result = cdb.cdb(args["path"])

    return result
