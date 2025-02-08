import argparse
import os

def get_arguments():
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Sync interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")
    return parser.parse_args()

def ensure_replica_exists(replica_path):
    # Create the replica folder if it does not exist.
    print(f"Checking if replica folder exists: {replica_path}")  
    if not os.path.exists(replica_path):
        os.makedirs(replica_path)
        print(f"Created missing replica folder: {replica_path}")  
    else:
        print("Replica folder already exists.")

if __name__ == "__main__":
    args = get_arguments()
    print(f"Source Folder: {args.source}")
    print(f"Replica Folder: {args.replica}")
    print(f"Sync Interval: {args.interval} seconds")
    print(f"Log File: {args.log_file}")

    ensure_replica_exists(args.replica)