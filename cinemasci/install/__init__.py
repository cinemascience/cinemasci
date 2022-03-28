import re
import os.path
import shutil
import glob
import json
import cinemasci.viewers

__format__ = {
    "tab" : "            "
}

__paths__ = {}

__databases__ = {}

__verbose__ = False

def old_smoketest():
    print(cinemasci.path())
    print(cinemasci.viewers.version())

    viewers = ["explorer", "view"]
    src_dbs = ["sphere.cdb", "sedov1.cdb", "sedov2.cdb"]
    dbs = {
        "explorer": 
        [ 
                {
                    "name": "sphere",
                    "directory": "sphere.cdb"
                },
                {
                    "name": "sedov",
                    "directory": "sedov1.cdb"
                }
        ],
        "view": 
        [
            { 
                "database_name": "sphere",
                "datasets":
                [
                    {
                        "name": "sphere",
                        "location": "sphere.cdb"
                    }
                ]
            },
            { 
                "database_name": "sedov",
                "datasets":
                [
                    {
                        "name": "sedov1",
                        "location": "sedov1.cdb"
                    },
                    {
                        "name": "sedov2",
                        "location": "sedov2.cdb"
                    }
                ]
            }
        ]
    }

    src_basepath = "./testing/data"
    for v in viewers:
        print("Viewer: {}".format(v))
        # basics
        res_basepath = "./testing/scratch/smoketest/{}".format(v)

        # expand path
        abs_basepath = os.path.abspath(os.path.expanduser(res_basepath))

        # copy data to testing area
        for db in src_dbs:
            print("    copying data {}".format(db))
            shutil.copytree( "{}/{}".format(src_basepath, db), "{}/{}".format(res_basepath, db) ) 

        # viewer install
        destination = abs_basepath
        install_viewer( destination, v, dbs[v] )

def install_viewer(destination, viewer, dbs):
    copy_cinema_dir_to_destination( destination ) 
    copy_viewer_to_destination( destination, viewer ) 
    write_database_file( destination, viewer, dbs ) 

def write_database_file(destination, viewer, dbs):
    version = cinemasci.viewers.version()
    dbfile = os.path.join( destination, "cinema", viewer, version, "databases.json")

    with open(dbfile, "w") as output:
        json.dump(dbs, output, indent=4)

def install_components():
    compSrc  = os.path.join(__paths__["indir"], "components")
    compDest = os.path.join(__paths__["cinema_out"], "components")
    if not os.path.isdir(compDest):
        print("Installing Components ...")
        shutil.copytree( compSrc, compDest ) 

def install_libs():
    libsSrc  = os.path.join(__paths__["indir"], "cinema", "lib")
    libsDest = os.path.join(__paths__["cinema_out"], "lib")
    if not os.path.isdir(libsDest):
        print("Installing libs ...")
        shutil.copytree( libsSrc, libsDest ) 

#
# copy the cinema directory to a destination folder
#
def copy_cinema_dir_to_destination( dest ):
    sourcedir = os.path.join( cinemasci.path(), "viewers" )
    cinemalib = os.path.join( sourcedir, "cinema" )
    shutil.copytree( cinemalib, os.path.join( dest, "cinema" ) ) 

#
# copy a viewer to the destination 
#
def copy_viewer_to_destination( dest, viewer ):
    source_viewer = os.path.join( cinemasci.path(), "viewers", "cinema_{}.html".format(viewer) )
    dest_viewer   = os.path.join( dest, "cinema_{}.html".format(viewer) )
    shutil.copyfile( source_viewer, dest_viewer )
