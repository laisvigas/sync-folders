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
                

def remove_deleted_files(source_path, replica_path):
    # Remove files and directories in replica that don't exist in source
    for root, dirs, files in os.walk(replica_path, topdown=False):
        relative_path = os.path.relpath(root, replica_path)
        source_folder = os.path.join(source_path, relative_path)

        # Remove files not in the source
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_folder, file)

            if not os.path.exists(source_file):
                os.remove(replica_file)
                print(f"Deleted file: {replica_file}")

        # Remove empty directories not in the source
        for dir_name in dirs:
            replica_dir = os.path.join(root, dir_name)
            source_dir = os.path.join(source_folder, dir_name)

            if not os.path.exists(source_dir):
                shutil.rmtree(replica_dir)
                print(f"Deleted directory: {replica_dir}")


if __name__ == "__main__":
    args = get_arguments()
    print(f"Source Folder: {args.source}")
    print(f"Replica Folder: {args.replica}")
    print(f"Sync Interval: {args.interval} seconds")
    print(f"Log File: {args.log_file}")

    ensure_replica_exists(args.replica)
    copy_new_files(args.source, args.replica)
    remove_deleted_files(args.source, args.replica)