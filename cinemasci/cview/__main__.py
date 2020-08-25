
def main( cview_type, database ):
    import cinemasci
    import http.server
    import socketserver

    localhost = "http://127.0.0.1"
    PORT      = 8100

    viewer = "cinemasci/cview/{}/cinema_{}.html".format(cview_type, cview_type)
    database = database 

    Handler   = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("{}:{}/{}?databases={}".format(localhost, PORT, viewer, database))
        httpd.serve_forever()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="run a Cinema Viewer")
    parser.add_argument("database", help="database to view") 
    # parser.add_argument("--viewer", default=None, help="viewer type") 
    args = parser.parse_args()

    #if args.viewer is None:
        #args.viewer = "explorer"

    # currently only viewer type explorer is supported
    main( "explorer", args.database) 

