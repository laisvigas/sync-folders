import argparse
import os
import shutil
import hashlib
import time


def get_arguments():
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Sync interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")
    return parser.parse_args()


def log_action(log_file, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(log_file, "a") as log:
        log.write(log_message + "\n")


def ensure_replica_exists(replica_path, log_file):
    # Create the replica folder if it does not exist.
    if not os.path.exists(replica_path):
        os.makedirs(replica_path)
        log_action(log_file, f"Created missing replica folder: {replica_path}")
    else:
        log_action(log_file, "Replica folder already exists.")


def calculate_md5(file_path):
    # Calculate MD5 hash of a file.
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        return None  # Return None in case of error


def copy_new_files(source_path, replica_path, log_file):
    # Copy new or updated files from source to replica using MD5
    for root, _, files in os.walk(source_path):
        # Calculate the relative path from the source
        relative_path = os.path.relpath(root, source_path)
        target_folder = os.path.join(replica_path, relative_path)

        # Ensure target folder exists
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            log_action(log_file, f"Created missing folder: {target_folder}")

        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(target_folder, file)

            # Compute MD5 hashes
            source_md5 = calculate_md5(source_file)
            replica_md5 = calculate_md5(replica_file) if os.path.exists(replica_file) else None

            # Copy only if the file does not exist or is different
            if replica_md5 is None or source_md5 != replica_md5:
                temp_replica_file = replica_file + ".tmp"
                shutil.copy2(source_file, temp_replica_file)
                os.replace(temp_replica_file, replica_file)
                log_action(log_file, f"Copied: {source_file} -> {replica_file}")


def remove_deleted_files(source_path, replica_path, log_file):
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
                log_action(log_file, f"Deleted: {replica_file}")

        # Remove empty directories not in the source
        if not os.path.exists(source_folder) and not os.listdir(root):
            os.rmdir(root)
            log_action(log_file, f"Removed empty folder: {root}")


if __name__ == "__main__":
    args = get_arguments()
    log_action(args.log_file, "Starting synchronization process")
    
    try:
        while True:
            ensure_replica_exists(args.replica, args.log_file)
            copy_new_files(args.source, args.replica, args.log_file)
            remove_deleted_files(args.source, args.replica, args.log_file)
            log_action(args.log_file, "Synchronization completed")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        log_action(args.log_file, "Synchronization process stopped by user.")