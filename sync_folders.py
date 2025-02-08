import argparse
import os
import shutil
import hashlib

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


def calculate_md5(file_path):
    # Calculate MD5 hash of a file.
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def copy_new_files(source_path, replica_path):
    # Copy new or updated files from source to replica using MD5
    for root, _, files in os.walk(source_path):
        # Calculate the relative path from the source
        relative_path = os.path.relpath(root, source_path)
        target_folder = os.path.join(replica_path, relative_path)

        # Ensure target folder exists
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(target_folder, file)

            # Compute MD5 hashes
            source_md5 = calculate_md5(source_file)
            replica_md5 = calculate_md5(replica_file) if os.path.exists(replica_file) else None

            # Copy only if the file does not exist or is different
            if replica_md5 is None or source_md5 != replica_md5:
                shutil.copy2(source_file, replica_file)
                print(f"Copied: {source_file} -> {replica_file}")


if __name__ == "__main__":
    args = get_arguments()
    print(f"Source Folder: {args.source}")
    print(f"Replica Folder: {args.replica}")
    print(f"Sync Interval: {args.interval} seconds")
    print(f"Log File: {args.log_file}")

    ensure_replica_exists(args.replica)
    copy_new_files(args.source, args.replica)