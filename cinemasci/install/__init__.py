import re
import os.path
import shutil
import glob
import cinemasci.viewers

__format__ = {
    "tab" : "            "
}

__paths__ = {}

__databases__ = {}

__verbose__ = False

def smoketest():
    print(cinemasci.path())
    print(cinemasci.viewers.version())

    # source
    shutil.copytree( "testing/data/sedov1.cdb", "testing/scratch/smoketest/sedov1.cdb" ) 
    shutil.copytree( "testing/data/sphere.cdb", "testing/scratch/smoketest/sphere.cdb" ) 

    # all expansions of the path should work 
    cdb = "./testing/scratch/smoketest/sphere.cdb"
        # path expanded here
    abs_cdb = os.path.abspath(os.path.expanduser(cdb))
    # can print these out if you'd like
    # print("absolute path")
    # print(abs_cdb)
    destination = os.path.dirname(abs_cdb)
    # print("destination")
    # print(destination)
    cdb = os.path.basename(abs_cdb)
    # print("cdb")
    # print(cdb)

    # explorer install
    if True:
        copy_cinema_dir_to_destination( destination ) 
        copy_viewer_to_destination( destination, "explorer" ) 
        dbs = [
            {
                "name": "first",
                "path": "sphere.cdb"
            },
            {
                "name": "second",
                "path": "sedov1.cdb"
            }
        ]
        write_explorer_database_file( destination, dbs ) 

    # viewer install
    if False:
        copy_cinema_dir_to_destination( destination ) 
        copy_viewer_to_destination( destination, "view" ) 

    # clean up
    if False:
        os.rmdir("testing/scratch/smoketest")

def set_databases(dbs):
    global __databases__

    __databases__ = dbs

def write_explorer_database_file( path, databases ):
    version = cinemasci.viewers.version()
    dbfile = os.path.join( path, "cinema", "explorer", version, "databases.json")

    with open(dbfile, "w") as output:
        output.write("[\n")
        first = True

        for db in databases:
            if first:
                first = False
            else:
                output.write(",\n")

            output.write("{\n")
            output.write("    \"name\": \"{}\",\n".format(db["name"]))
            output.write("    \"directory\": \"{}\"".format(db["path"]))
            output.write("\n}")

        output.write("\n]\n")

def write_view_database_file(path, databases):
    with open(path, "w") as output:
        output.write("[\n")
        first = True

        for db in databases:
            if first:
                first = False
            else:
                output.write(",\n")

            output.write("{\n")
            output.write("    \"name\": \"{}\",\n".format(db["name"]))
            output.write("    \"directory\": \"{}\"".format(db["path"]))
            output.write("\n}")

        output.write("\n]\n")

def explorer(indir, outdir, outfile, dbs):
    set_databases(dbs)
    return install_core("explorer", indir, outdir, outfile)


def view(indir, outdir, outfile, dbs):
    set_databases(dbs)
    return install_core("view", indir, outdir, outfile)


def install_core(viewer, indir, outdir, outfile):
    print("Trying to install Cinema::{}".format(viewer))
    print(viewer)
    print(indir)
    print(outdir)
    print(outfile)

    result = False

    if install_check(viewer, indir, outdir, outfile):
        print("Installing Cinema::{} ...".format(viewer))

        # create a standard installation location
        if not os.path.isdir(__paths__["cinema_out"]):
            os.mkdir(__paths__["cinema_out"])

        # install support code 
        install_libs()
        install_components()

        # install the basic components in a standard place
        viewerSrcDir  = os.path.join(__paths__["indir"], viewer)
        viewerDestDir = os.path.join(__paths__["cinema_out"], viewer)
        shutil.copytree( viewerSrcDir, viewerDestDir ) 

        # specialized install for this viewer 
        # -----------------------------------
        if viewer == "view":
            result = install_view()
        elif viewer == "explorer":
            result = install_explorer()
        else:
            print("ERROR: unrecognized viewer type ({})".format(viewer))

        # to make the output nice and formatted ...
        print("")
        result = True

    return result

#
# specific install for view
#
# assumes all checks have been done, and that global variables are correct
#
def install_view():
    global __paths__
    global __databases__

    with open(__paths__["fullInfile"], 'r') as iFile, open(__paths__["fullOutfile"], 'w') as oFile:
        for line in iFile:
            oFile.write(line);
            if re.search('START', line):
                oFile.write("{}dataSets = [\n".format(__format__["tab"]))
                first = True
                for db in __databases__:
                    if (first):
                        first = False
                    else:
                        oFile.write(",\n")

                    oFile.write("{}    \"{}\"".format(__format__["tab"], db["path"]))
                oFile.write("\n{}]\n".format(__format__["tab"]))
                
def install_explorer():
    shutil.copyfile(__paths__["fullInfile"], __paths__["fullOutfile"])
    write_explorer_database_file()

#
# sets global path variables, and checks status for install
#
def install_check(viewer, indir, outdir, outfile):
    global __paths__
    global __verbose__

    installState = True

    __paths__["indir"]       = get_abspath(indir) 
    __paths__["outdir"]      = get_abspath(outdir) 
    __paths__["cinema_out"]  = os.path.join( __paths__["outdir"], "cinema") 
    __paths__["fullOutfile"] = os.path.join( __paths__["outdir"], outfile )
    __paths__["view"]        = os.path.join( __paths__["cinema_out"], "view") 
    __paths__["explorer"]    = os.path.join( __paths__["cinema_out"], "explorer")

    # must be done after the above are set, so that version function works
    version = cinemaci.viewers.version() 
    print("version: {}".format(viewer))
    __paths__["fullInfile"]  = os.path.join( __paths__["indir"], "cinema_{}.html".format(viewer)) 

    if __verbose__:
        print("indir       : {}".format(__paths__["indir"]))
        print("outdir      : {}".format(__paths__["outdir"]))
        print("cinema_out  : {}".format(__paths__["cinema_out"]))
        print("explorer    : {}".format(__paths__["explorer"]))
        print("view        : {}".format(__paths__["view"]))
        print("fullInfile  : {}".format(__paths__["fullInfile"]))
        print("fullOutfile : {}".format(__paths__["fullOutfile"]))

    # check status for install
    if not os.path.isdir(__paths__["indir"]):
        print("ERROR: {} does not exist".format(__paths__["indir"]))
        installState = False;
    elif not os.path.isfile(__paths__["fullInfile"]):
        print("ERROR: {} does not exist".format(__paths__["fullInfile"]))
        installState = False;
    elif not os.path.isdir(__paths__["outdir"]):
        print("ERROR: {} does not exist".format(__paths__["outdir"]))
        installState = False;
    elif os.path.isfile(__paths__["fullOutfile"]):
        print("ERROR: {} exists".format(__paths__["fullOutfile"]))
        installState = False;

    return installState

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
