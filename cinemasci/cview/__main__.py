
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
    parser.add_argument("viewer", help="viewer type") 
    parser.add_argument("database", help="database to view") 
    args = parser.parse_args()

    main( args.viewer, args.database) 

