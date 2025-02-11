
# Folder Synchronization Program

## Description

This program synchronizes files between two folders. It performs a one-way synchronization where the replica folder matches the content of the source folder. It periodically checks for changes and logs all file creation, copying, and removal actions to both the console and a specified log file.

## Features

- One-way synchronization from the source folder to the replica folder.
- Periodic synchronization, based on a user-defined interval.
- Logs all operations (file creation, copying, and removal) to the console and a log file.
- Command-line arguments for easy configuration (source folder, replica folder, sync interval, log file).

## Usage

Run the script with the following command:

```bash
python sync_folders.py source_folder replica_folder sync_interval log_file
```

- `source_folder`: Path to the source folder.
- `replica_folder`: Path to the replica folder.
- `sync_interval`: Sync interval in seconds.
- `log_file`: Path to the log file where operations will be logged.

Example:

```bash
python sync_folders.py /path/to/source_folder /path/to/replica_folder 5 /path/to/log_file.txt
```

This will synchronize the two folders every 5 seconds and log actions to `sync_log.txt`.

