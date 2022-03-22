import re
import os.path
import shutil
import glob

__format__ = {
    "tab" : "            "
}

__paths__ = {}

__databases__ = {}

__verbose__ = False


def set_databases(dbs):
    global __databases__

    __databases__ = dbs

def get_abspath(path):
    return os.path.abspath(os.path.expanduser(path))

def get_viewer_version(viewer):
    global __paths__

    version = None

    dirs = glob.glob(os.path.join(__paths__["indir"], viewer, "*"))

    for d in dirs:
        version = os.path.split(d)[1]
    
    return version

# hack
def update_explorer_database_file(path):
    # get the version
    version = None
    dirs = glob.glob(os.path.join(path, "cinema", "explorer", "*"))
    print("dirs: {}".format(dirs))
    for d in dirs:
        version = os.path.split(d)[1]

    dbfile = os.path.join( path, "cinema", "explorer", version, "databases.json")

    dbs = glob.glob(os.path.join(path, "*.cdb"))

    write_database_file(dbfile, dbs)

def write_explorer_database_file():
    global __paths__
    global __databases__

    version = get_viewer_version("explorer")
    dbfile = os.path.join( __paths__["explorer"], version, "databases.json")

    write_database_file(dbfile, __databases__)

def write_database_file(path, databases):
    # TODO: check for path attribute in each database

    with open(path, "w") as output:
        output.write("[\n")
        first = True
        for db in databases:
            if first:
                first = False
            else:
                output.write(",\n")

            output.write("{\n")
            output.write("    \"name\": \"{}\",\n".format(db["path"]))
            output.write("    \"directory\": \"{}\"".format(db["path"]))
            if "selection" in db:
                output.write(",\n    \"selection\": {\n")
                firstvar = True
                for v in db["selection"]:
                    if firstvar:
                        firstvar = False
                    else:
                        output.write(",\n")
                    output.write("        \"{}\": {}".format(v, db["selection"][v]))
                output.write("\n                 }\n")

            output.write("}")

        output.write("\n]\n")

def explorer(indir, outdir, outfile, dbs):
    set_databases(dbs)
    return install_core("explorer", indir, outdir, outfile)


def compare(indir, outdir, outfile, dbs):
    # cinema_compare only supports loading one or two cdb's
    if len(dbs) > 2:
        print("ERROR: cinema_compare supports loading 1 or 2 databases but was given {}\n".format(len(dbs)))
        return False
    set_databases(dbs)
    return install_core("compare", indir, outdir, outfile)


def install_core(viewer, indir, outdir, outfile):
    print("Trying to install Cinema::{}".format(viewer))

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
        if viewer == "compare":
            result = install_compare()
        elif viewer == "explorer":
            result = install_explorer()
        else:
            print("ERROR: unrecognized viewer type ({})".format(viewer))

        # to make the output nice and formatted ...
        print("")
        result = True

    return result

#
# specific install for compare
#
# assumes all checks have been done, and that global variables are correct
#
def install_compare():
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
    __paths__["compare"]     = os.path.join( __paths__["cinema_out"], "compare") 
    __paths__["explorer"]    = os.path.join( __paths__["cinema_out"], "explorer")

    # must be done after the above are set, so that version function works
    version = get_viewer_version(viewer)
    print("version: {}".format(viewer))
    __paths__["fullInfile"]  = os.path.join( __paths__["indir"], viewer, version, "cinema_{}.html".format(viewer)) 

    if __verbose__:
        print("indir       : {}".format(__paths__["indir"]))
        print("outdir      : {}".format(__paths__["outdir"]))
        print("cinema_out  : {}".format(__paths__["cinema_out"]))
        print("explorer    : {}".format(__paths__["explorer"]))
        print("compare     : {}".format(__paths__["compare"]))
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
    libsSrc  = os.path.join(__paths__["indir"], "lib")
    libsDest = os.path.join(__paths__["cinema_out"], "lib")
    if not os.path.isdir(libsDest):
        print("Installing libs ...")
        shutil.copytree( libsSrc, libsDest ) 
