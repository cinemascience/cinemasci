import cinemasci
import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
from os import path
from os.path import relpath
from os import getcwd
from os import access
from os import R_OK

#
# global datbase - can't seem to add an instance variable to the
# subclass of SimpleHTTPRequestHandler
#
TheDatabase = "CINEMAJUNK" 
CinemaInstallPath = "cinemasci/cview"

#
# CinemaReqestHandler
#
# Processes GET requests to find viewers and databases
#
class CinemaRequestHandler(http.server.SimpleHTTPRequestHandler):

    def log(self, message):
        if False:
            print(message)

    def do_GET(self):
        global TheDatabase
        global CinemaInstallPath

        self.log("PATH ORIG: {}".format(self.path))
        query_components = parse_qs(urlparse(self.path).query)
        self.log("QUERY    : {}".format(query_components))
        self.path = self.path.split("?")[0]
        self.log("PATH     : {}".format(self.path))

        # set attributes from a query in the GET URL
        if "databases" in query_components:
            TheDatabase = query_components["databases"][0]
            # if not TheDatabase.startswith("/"):
                # TheDatabase = "/" + TheDatabase
            self.log("SET DB   : {}".format(TheDatabase))

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

            else:
                self.log("VIEWER: -{}-".format(viewer))

        if self.path.startswith(TheDatabase):
            # handle requests to the database

            # remap absolute paths
            if TheDatabase.startswith("/"):
                self.log("DB QUERY : {}".format(self.path))
                self.path = relpath(self.path, getcwd())
                self.log("CWD      : {}".format(getcwd()))
                self.log("REL DB   : {}".format(self.path))

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

#
# main
#
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="run a Cinema Viewer")
    parser.add_argument("--data", required=True, default=None, help="database to view (required)") 
    parser.add_argument("--viewer", required=True, default='explorer', help="viewer type to use (required)") 
    parser.add_argument("--port", type=int, default=8000, help="port to use (optional)") 
    parser.add_argument("--assetname", default=None, help="asset name to use (optional)") 
    args = parser.parse_args()

    # run
    localhost = "http://127.0.0.1"

    # mypath = path.abspath(__file__)
    # print(path.dirname(mypath))

    my_handler = CinemaRequestHandler 
    with socketserver.TCPServer(("", args.port), my_handler) as httpd:
        urlstring = "{}:{}/?viewer={}&databases={}".format(localhost, args.port, args.viewer, args.data)
        if not args.assetname is None:
            urlstring = urlstring + "&assetname{}".format(args.assetname)
        print(urlstring)
        httpd.serve_forever()

