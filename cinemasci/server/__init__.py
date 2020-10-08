import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
from os import listdir
from os import path
from os.path import relpath
from os import getcwd
from os import access
from os import R_OK
import pathlib

#
# global variables - can't seem to add an instance variable to the
# subclass of SimpleHTTPRequestHandler
#
TheDatabase = "CINEMAJUNK" 
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
    print("CinemaInstallPath: {}".format(CinemaInstallPath))

def get_relative_install_path( initpath ):
    global CinemaInstallPath

    result = path.join(CinemaInstallPath, initpath.strip("/"))
    result = relpath(result, getcwd())
    print("REL IN PATH: {}".format(result))
    return result

#
# CinemaReqestHandler
#
# Processes GET requests to find viewers and databases
#
class CinemaRequestHandler(http.server.SimpleHTTPRequestHandler):

    def translate_path(self, path ):
        print("translate_path: {}".format(path))
        return path 

    def log(self, message):
        if False:
            print(message)

    def do_GET(self):
        global TheDatabase
        global CinemaInstallPath
        global ServerInstallPath

        self.log("PATH ORIG: {}".format(self.path))
        query_components = parse_qs(urlparse(self.path).query)
        self.log("QUERY    : {}".format(query_components))
        self.path = self.path.split("?")[0]
        self.log("PATH     : {}".format(self.path))
        self.log("DBPATH   : {}".format(TheDatabase))

        # set attributes from a query in the GET URL
        if "databases" in query_components:
            TheDatabase = query_components["databases"][0]
            self.log("SET DB   : {}".format(TheDatabase))

            for p in TheDatabase.split(","):
                if not path.isdir(p):
                    self.path = ServerInstallPath + "/error_no-database.html"
                    return http.server.SimpleHTTPRequestHandler.do_GET(self)

        if "viewer" in query_components: 
            # handle a request for a viewer 
            viewer = query_components["viewer"][0]
            if viewer == "explorer": 
                # handle a request for the Cinema:Explorer viewer
                self.log("EXPLORER")
                self.path = CinemaInstallPath + "/cinema_explorer.html"
                return http.server.SimpleHTTPRequestHandler.do_GET(self)

            elif viewer == "view": 
                # handle a request for the Cinema:View viewer
                self.log("VIEW")
                self.path = CinemaInstallPath + "/cinema_view.html"
                return http.server.SimpleHTTPRequestHandler.do_GET(self)

            if viewer == "test": 
                # handle a request for the Cinema:Explorer viewer
                self.log("TEST")
                self.path = ServerInstallPath + "/cinema_test.html"
                return http.server.SimpleHTTPRequestHandler.do_GET(self)

            else:
                self.log("VIEWER: -{}-".format(viewer))

        if self.path.startswith("/" + TheDatabase):
            # handle requests to the database

            # remap absolute paths
            if False:
                self.log("DATABASE QUERY : {}".format(self.path))
                if TheDatabase.startswith("/"):
                    self.log("DB QUERY : {}".format(self.path))
                    self.path = relpath(self.path, getcwd())
                    self.log("CWD      : {}".format(getcwd()))
                    self.log("REL DB   : {}".format(self.path))

            self.path = self.path.strip("/")

            if access(self.path, R_OK):
                self.log("ACCESSING: {}".format(self.path))
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            else:
                print("ERROR: cannot access file: {}".format(self.path))

        elif self.path.startswith("/cinema"):
            # handle a requests for sub components of the viewers 
            # NOTE: fragile - requires 'cinema' path be unique

            self.log("CINEMA   : {}".format(self.path))
            self.path = CinemaInstallPath + self.path 
            self.log("        {}".format(self.path))
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        else:
            # everything else
            self.log("NORMAL   : {}".format(self.path))
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_cinema_server( viewer, data, port, assetname=None):
    localhost = "http://127.0.0.1"

    set_install_path()
    my_handler = CinemaRequestHandler 
    with socketserver.TCPServer(("", port), my_handler) as httpd:
        urlstring = "{}:{}/?viewer={}&databases={}".format(localhost, port, viewer, data)
        if not assetname is None:
            urlstring = urlstring + "&assetname{}".format(assetname)
        print(urlstring)
        httpd.serve_forever()

