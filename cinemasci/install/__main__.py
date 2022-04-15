import os
from . import install

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="install a cinema viewer")
    parser.add_argument("--path", required=True, default=None, help="destination for installation (required)") 
    parser.add_argument("--database", 
                                nargs="+",
                                required=True, 
                                default=[], 
                                help="database to view (required)") 
    parser.add_argument("--type", default="remote", help="type of install (local, remote)") 
    parser.add_argument("--viewer", required=True, default='explorer', help="viewer type to use. One of [explorer, simple, view] (required)") 
    args = parser.parse_args()

    installer = install()
    abs_path = os.path.abspath(os.path.expanduser(args.path))
    # convert the list of dbs to the json datastructure needed by the viewer
    dbj = installer.get_database_json( args.viewer, args.database )
    # install the viewer
    installer.install_viewer( abs_path, args.viewer, dbj, args.type )
