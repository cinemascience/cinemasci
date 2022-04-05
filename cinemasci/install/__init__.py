import re
import os
import shutil
import glob
import json
import cinemasci.viewers

class install:
    INSTALL_ERROR = 0
    INSTALL_OK    = 1

    def __init__(self):
        """The constructor"""
        self.source = cinemasci.path()
        print(self.source)

    def install_viewer(self, destination, vtype, dbs, type="remote"):
        status = install.INSTALL_OK
        print("self.source = {}".format(self.source))

        if not os.path.isdir(os.path.join(destination, "cinema")):
            if os.access(destination, os.W_OK):
                if os.access(self.source, os.R_OK):
                    self.__copy_cinema_dir_to_destination( destination ) 
                    self.__copy_viewer_to_destination( destination, vtype ) 
                    if vtype == "simple" :
                        self.__insert_databases( destination, vtype, dbs )
                    else:
                        self.__write_database_file( destination, vtype, dbs ) 

                    if type == "remote":
                        print("Performing remote install")
                        # nothing to do

                    else:
                        print("Performing local install")
                        self.__install_libs(destination)
                        self.__install_components(destination)
                        self.__install_third_party(destination)

                else:
                    print("ERROR: cannot read from directory {}".format(self.source)) 
                status = install.INSTALL_ERROR
            else:
                print("ERROR: cannot write to directory {}".format(destination))
                status = install.INSTALL_ERROR
        else:
            print("ERROR: cinema install exists; Cannot continue")        
            status = install.INSTALL_ERROR

        return status

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

    #
    #
    #
    def __insert_databases( self, dest, viewer, dbs):
        dest_viewer     = os.path.join( dest, "cinema_{}.html".format(viewer) )
        dest_viewer_tmp = os.path.join( dest, "cinema_{}.tmp.html".format(viewer) )
        with open(dest_viewer, 'r') as dviewer:
            with open(dest_viewer_tmp, 'w') as rviewer:
                writeline = True
                for line in dviewer:
                    if writeline:
                        if "CINEMA_DB_START" in line:
                            rviewer.write("            var dataSets = ")
                            alldbs = []
                            for db in dbs:
                                alldbs.append(db["directory"])
                            rviewer.write(json.dumps(alldbs))
                            rviewer.write("\n")
                            writeline = False
                        else:
                            rviewer.write(line)
                    elif "CINEMA_DB_END" in line:
                        writeline = True


    #
    # write a json-compliant db datset to a file
    #
    def __write_database_file(self, destination, viewer, dbs):
        version = cinemasci.viewers.version()
        dbfile = os.path.join( destination, "cinema", viewer, version, "databases.json")

        with open(dbfile, "w") as output:
            json.dump(dbs, output, indent=4)

    def __install_components(self, destination):
        compSrc  = os.path.join(destination, "components")
        compDest = os.path.join(self.source, "components")
        if not os.path.isdir(compDest):
            print("Installing Components ...")
            shutil.copytree( compSrc, compDest ) 

    def __install_libs(self, destination):
        libsSrc         = os.path.join(self.source, "viewers", "cinema", "lib") 
        libsDest        = os.path.join(destination, "cinema", "lib")
        print("Installing libs ...")
        print(libsSrc)
        print(libsDest)
        shutil.copytree( libsSrc, libsDest ) 

    def __install_third_party(self, destination):
        thirdPartySrc   = os.path.join(self.source, "viewers", "third_party") 
        libsDest        = os.path.join(destination, "cinema", "lib")
        print("Installing third party ...")
        print(libsSrc)
        print(libsDest)
        shutil.copytree( thirdPartySrc, libsDest ) 

