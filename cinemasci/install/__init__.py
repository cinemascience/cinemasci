import re
import os.path
import shutil
import glob
import json
import cinemasci.viewers

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
