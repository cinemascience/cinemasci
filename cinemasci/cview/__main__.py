import cinemasci
import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
from os.path import relpath
from os import getcwd

TheDatabase = "CINEMAJUNK" 

class CinemaRequestHandler(http.server.SimpleHTTPRequestHandler):

    def log(self, message):
        if False:
            print(message)

    def do_GET(self):
        global TheDatabase

        self.log("PATH ORIG: {}".format(self.path))
        query_components = parse_qs(urlparse(self.path).query)
        self.log("QUERY    : {}".format(query_components))
        self.path = self.path.split("?")[0]
        self.log("PATH     : {}".format(self.path))

        if "databases" in query_components:
            TheDatabase = query_components["databases"][0]
            if not TheDatabase.startswith("/"):
                TheDatabase = "/" + TheDatabase
            self.log("SET DB   : {}".format(TheDatabase))

        if self.path.startswith(TheDatabase):
            self.log("DB QUERY : {}".format(self.path))
            self.path = relpath(self.path, getcwd())
            self.log("CWD      : {}".format(getcwd()))
            self.log("REL DB   : {}".format(self.path))
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == "/explorer":
            self.log("EXPLORER")
            self.path = "cinemasci/cview/cinema_explorer.html" 
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == "/view":
            self.log("VIEW")
            self.path = "cinemasci/cview/cinema_view.html" 
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        elif self.path.startswith("/cinema"):
            self.log("CINEMA   : {}".format(self.path))
            self.path = "cinemasci/cview" + self.path
            self.log("        {}".format(self.path))
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        else:
            self.log("NORMAL   : {}".format(self.path))
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="run a Cinema Viewer")
    parser.add_argument("--data", required=True, default=None, help="database to view") 
    parser.add_argument("--viewer", required=True, default='explorer', help="viewer type to use") 
    parser.add_argument("--port", type=int, default=8000, help="port to use") 
    parser.add_argument("--assetname", default=None, help="asset name to use") 
    args = parser.parse_args()

    # run
    localhost = "http://127.0.0.1"

    my_handler = CinemaRequestHandler 
    with socketserver.TCPServer(("", args.port), my_handler) as httpd:
        if not args.assetname is None:
            print("{}:{}/{}?databases={}".format(localhost, args.port, args.viewer, args.data))
        else:
            print("{}:{}/{}?databases={}&assetname={}".format(localhost, args.port, args.viewer, args.data, args.assetname))
        httpd.serve_forever()

