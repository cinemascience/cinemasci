import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
from os import chdir
from os import path
from os.path import relpath
from os import getcwd
from os import access
from os import R_OK
import pathlib
import json
from .. import cdb

#
# global variables - can't seem to add an instance variable to the
# subclass of SimpleHTTPRequestHandler
#
CinemaInstallPath = "CINEMAJUNK"
ServerInstallPath = "CINEMAJUNK"

def set_install_path():
    global CinemaInstallPath
    global ServerInstallPath

    ServerInstallPath = str(pathlib.Path(__file__).parent.absolute())
    CinemaInstallPath = str(pathlib.Path(__file__).parent.absolute())
    # edit the path to get the correct installation path
    CinemaInstallPath = CinemaInstallPath.strip("/server")
    CinemaInstallPath = "/" + CinemaInstallPath + "/viewers"

def verify_cinema_databases( viewer, databases, assetname ):
    result = False

    for db in databases:
        if viewer == "view":
            # this is the default case
            if assetname is None:
                assetname = "FILE"

            db = cdb.cdb(db)
            db.read_data_from_file()

            if db.parameter_exists(assetname):
                result = True
            else:
                print("")
                print("ERROR: Cinema viewer \'view\' is looking for a column named \'{}\', but the".format(assetname)) 
                print("       the cinema database \'{}\' doesn't have one.".format(db)) 
                print("")
                print("       use \'--assetname <name>\' where <name> is one of these possible values") 
                print("       that were found in \'{}\':".format(db))
                print("")
                print("           \"" + ' '.join(db.get_parameter_names()) + "\"")
                print("")
                result = False
                break;
        else:
            result = True

    return result 

#
# CinemaSimpleReqestHandler
#
# Processes GET requests to find viewers and databases
#
class CinemaSimpleRequestHandler(http.server.SimpleHTTPRequestHandler):

    @property
    def databases(self):
        return self._databases

    @databases.setter
    def databases(self, value):
        self._databases = value

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value

    @property
    def assetname(self):
        return self._assetname

    @assetname.setter
    def assetname(self, value):
        self._assetname = value

    @property
    def viewer(self):
        return self._viewer

    @viewer.setter
    def viewer(self, value):
        self._viewer = value

    def translate_path(self, path ):
        # print("translate_path: {}".format(path))
        return path

    def log(self, message):
        if self.verbose:
            print(message)

    def log_message( self, format, *args ):
        pass

    def do_GET(self):
        global CinemaInstallPath
        global ServerInstallPath

        self.log(" ")
        self.log("PATH     : {}".format(self.path))

        # the request is for a viewer
        if self.path == "/":
            if False:
                # this was an old test; still here as an example error
                if not path.isdir(self.base_path):
                    self.log("ERROR")
                    self.path = ServerInstallPath + "/error_no-database.html"
                    return http.server.SimpleHTTPRequestHandler.do_GET(self)

            if self.viewer == "explorer": 
                # handle a request for the Cinema:Explorer viewer
                self.log("EXPLORER")
                self.path = CinemaInstallPath + "/cinema_explorer.html"
                self.log(self.path)
                return http.server.SimpleHTTPRequestHandler.do_GET(self)

            elif self.viewer == "view": 
                # handle a request for the Cinema:View viewer
                self.log("VIEW")
                self.path = CinemaInstallPath + "/cinema_view.html"
                return http.server.SimpleHTTPRequestHandler.do_GET(self)

            if self.viewer == "test": 
                # handle a request for the Cinema:Explorer viewer
                self.log("TEST")
                self.path = ServerInstallPath + "/cinema_test.html"
                return http.server.SimpleHTTPRequestHandler.do_GET(self)

            else:
                self.log("VIEWER: {}".format(self.viewer))


        if self.path.endswith("cinema_attributes.json"):
            # this is a request to the server for attributes
            self.log("ATTRIBUTE REQUEST") 

            if (not self.assetname == None):
                json_string = "{{\"assetname\" : \"{}\"}}".format(self.assetname)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(json_string))
                self.end_headers()
                self.wfile.write(str.encode(json_string))
            return

        if self.path.endswith("databases.json"):
            self.log("DATABASES   : {}".format(self.path))
            json_string = self.get_database_json()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(json_string))
            self.end_headers()
            self.wfile.write(json_string.encode())
            return


        if self.path.startswith("/cinema/"):
            # handle a requests for sub components of the viewers 
            # NOTE: fragile - requires 'cinema' path be unique

            self.log("CINEMA   : {}".format(self.path))
            self.path = CinemaInstallPath + self.path 
            self.log("         : {}".format(self.path))
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        else:
            # everything else
            self.log("NORMAL   : {}".format(self.path))
            self.path = relpath(self.path.strip("/"), getcwd())
            # self.log("UPDATED  : {}".format(self.path))
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def get_database_json( self ):
        dbj = [] 
        if   self.viewer == "explorer": 
            for db in self.databases:
                dbj.append({    "name": db,
                                "directory": db 
                           })
        elif self.viewer == "view":
            dbs = []
            for db in self.databases:
                dbs.append( {
                                "name": db,
                                "location": db
                            }
                          )
            dbj.append({    
                        "database_name": db,
                        "datasets": dbs,
                       })
        elif self.viewer == "simple": 
            for db in self.databases:
                dbj.append(db)

        return json.dumps(dbj, indent=4)

def run_cinema_server( viewer, rundir, databases, port, assetname="FILE"):
    localhost = "http://127.0.0.1"

    chdir(rundir)
    if verify_cinema_databases(viewer, databases, assetname) :
        set_install_path()
        cin_handler = CinemaSimpleRequestHandler
        cin_handler.verbose   = False
        cin_handler.viewer    = viewer
        cin_handler.assetname = assetname
        cin_handler.databases = databases
        with socketserver.TCPServer(("", port), cin_handler) as httpd:
            urlstring = "{}:{}".format(localhost, port)
            print(urlstring)
            httpd.serve_forever()

