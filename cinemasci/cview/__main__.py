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

def main( database, port, cview_type ):

    localhost = "http://127.0.0.1"

    my_handler = CinemaRequestHandler 
    with socketserver.TCPServer(("", port), my_handler) as httpd:
        print("{}:{}/{}?databases={}".format(localhost, port, cview_type, database))
        httpd.serve_forever()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="run a Cinema Viewer")
    parser.add_argument("--data", default=None, help="database to view") 
    parser.add_argument("--port", type=int, default=8000, help="port to use") 
    parser.add_argument("--viewer", default='explorer', help="viewer type to use") 
    parser.add_argument("--new", default='explorer', help="viewer type to use") 
    args = parser.parse_args()

    # currently only viewer type explorer is supported
    main( args.data, args.port, args.viewer) 
