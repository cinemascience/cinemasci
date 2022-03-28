import re
import os
import shutil
import glob
import json
import cinemasci.viewers

class install:

    def __init__(self):
        """The constructor"""
        self.source = cinemasci.path()
        print(self.source)

    def install_viewer(self, destination, viewer, dbs):
        if os.access(destination, os.W_OK):
            if os.access(self.source, os.R_OK):
                self.__copy_cinema_dir_to_destination( destination ) 
                self.__copy_viewer_to_destination( destination, viewer ) 
                self.__write_database_file( destination, viewer, dbs ) 
            else:
                print("ERROR: cannot read from directory {}".format(self.source)) 
        else:
            print("ERROR: cannot write to directory {}".format(destination)) 

    def __write_database_file(self, destination, viewer, dbs):
        version = cinemasci.viewers.version()
        dbfile = os.path.join( destination, "cinema", viewer, version, "databases.json")

        with open(dbfile, "w") as output:
            json.dump(dbs, output, indent=4)

    def __install_components(self):
        compSrc  = os.path.join(__paths__["indir"], "components")
        compDest = os.path.join(__paths__["cinema_out"], "components")
        if not os.path.isdir(compDest):
            print("Installing Components ...")
            shutil.copytree( compSrc, compDest ) 

    def __install_libs(self):
        libsSrc  = os.path.join(__paths__["indir"], "cinema", "lib")
        libsDest = os.path.join(__paths__["cinema_out"], "lib")
        if not os.path.isdir(libsDest):
            print("Installing libs ...")
            shutil.copytree( libsSrc, libsDest ) 

    #
    # copy the cinema directory to a destination folder
    #
    def __copy_cinema_dir_to_destination(self, dest ):
        cinemalib = os.path.join( self.source, "viewers", "cinema" )
        shutil.copytree( cinemalib, os.path.join( dest, "cinema" ) ) 

    #
    # copy a viewer to the destination 
    #
    def __copy_viewer_to_destination( self, dest, viewer ):
        source_viewer = os.path.join( cinemasci.path(), "viewers", "cinema_{}.html".format(viewer) )
        dest_viewer   = os.path.join( dest, "cinema_{}.html".format(viewer) )
        shutil.copyfile( source_viewer, dest_viewer )
