
def main( database, port, cview_type ):
    import cinemasci
    import http.server
    import socketserver

    localhost = "http://127.0.0.1"

    viewer = "cinemasci/cview/{}/cinema_{}.html".format(cview_type, cview_type)
    database = database 

    Handler   = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("{}:{}/{}?databases={}".format(localhost, port, viewer, database))
        httpd.serve_forever()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="run a Cinema Viewer")
    parser.add_argument("--data", default=None, help="database to view") 
    parser.add_argument("--port", type=int, default=8000, help="port to use") 
    parser.add_argument("--viewer", default='explorer', help="viewer type to use") 
    args = parser.parse_args()

    # currently only viewer type explorer is supported
    main( args.data, args.port, args.viewer) 
