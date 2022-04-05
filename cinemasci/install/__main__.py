if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="install a cinema viewer")
    parser.add_argument("--database", required=True, default=None, help="database to view (required)") 
    parser.add_argument("--viewer", required=True, default='explorer', help="viewer type to use. One of [explorer, view] (required)") 
    args = parser.parse_args()

    print(args)
