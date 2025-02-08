import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Sync interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_arguments()
    print(f"Source Folder: {args.source}")
    print(f"Replica Folder: {args.replica}")
    print(f"Sync Interval: {args.interval} seconds")
    print(f"Log File: {args.log_file}")
