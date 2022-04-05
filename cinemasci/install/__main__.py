import os
from . import install

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="install a cinema viewer")
    parser.add_argument("--path", required=True, default=None, help="destination for installation (required)") 
    parser.add_argument("--database", required=True, default=None, help="database to view (required)") 
    parser.add_argument("--type", default="remote", help="type of install (local, remote)") 
    parser.add_argument("--viewer", required=True, default='explorer', help="viewer type to use. One of [explorer, view] (required)") 
    args = parser.parse_args()

    installer = install()
    abs_path = os.path.abspath(os.path.expanduser(args.path))
    installer.install_viewer( abs_path, args.viewer, [args.database], args.type )
