#!/usr/bin/env python3

import os
from datetime import datetime
import hashlib


def list_external_drives(test_dir=None):
    directory = test_dir if test_dir is not None else "/Volumes"
    volumes = os.listdir(directory)
    return [vol for vol in volumes if vol != "Macintosh HD"]


def choose_drive(drives, purpose):
    print(f"\nChoose {purpose} drive:")
    for i, drive in enumerate(drives, 1):
        print(f"{i}. {drive}")

    while True:
        try:
            choice = int(input(f"Enter the number of the {purpose} drive: "))
            if 1 <= choice <= len(drives):
                return drives[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def find_mp4_files_in_sd_card(input_path):
    mp4_files = []
    for root, dirs, files in os.walk(input_path):
        if "DCIM" in root.split(os.sep):
            for file in files:
                if file.lower().endswith(".mp4"):
                    mp4_files.append(os.path.join(root, file))
    return mp4_files


def find_mp4_files(input_path):
    mp4_files = []
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith(".mp4"):
                mp4_files.append(os.path.join(root, file))
    return mp4_files


def extract_date_from_file(file_path):
    try:
        stat = os.stat(file_path)
        return datetime.fromtimestamp(stat.st_mtime)
    except Exception as e:
        print(f"Error extracting date from {file_path}: {str(e)}")
    return None


def get_destination_path(output_path, file_date):
    month_names = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    return os.path.join(
        output_path,
        "Videos",
        str(file_date.year),
        f"{file_date.month:02d}-{month_names[file_date.month-1]}",
    )


def calculate_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


import argparse


def main(volume_directory=None):
    parser = argparse.ArgumentParser(description="Transfer media files.")
    parser.add_argument(
        "-v",
        "--volume_directory",
        help="Specify the volume directory",
        type=str,
        default="/Volumes",
    )
    args = parser.parse_args()
    if volume_directory is not None:
        args.volume_directory = volume_directory

    external_drives = list_external_drives(args.volume_directory)
    if not external_drives:
        print("No external drives found.")
        return

    input_drive = choose_drive(external_drives, "input")
    output_drive = choose_drive(external_drives, "output")

    print(f"Selected input drive: {input_drive}")
    print(f"Selected output drive: {output_drive}")

    input_path = os.path.join(args.volume_directory, input_drive)
    output_path = os.path.join(args.volume_directory, output_drive)

    mp4_files = find_mp4_files_in_sd_card(input_path)

    for file in mp4_files:
        file_date = extract_date_from_file(file)
        if file_date:
            dest_path = get_destination_path(output_path, file_date)
            print(f"File: {file}")
            print(f"Date: {file_date}")
            print(f"Destination: {dest_path}")
            existing_files = find_mp4_files(dest_path)
            for existing_file in existing_files:

                source_checksum = calculate_checksum(file)
                dest_checksum = calculate_checksum(
                    os.path.join(dest_path, os.path.basename(existing_file))
                )

                if source_checksum == dest_checksum:
                    print(
                        f'Detected duplicate file "{os.path.relpath(dest_path, output_path)}", not overriding'
                    )
                else:
                    confirmation = input(
                        f'Checksum mismatch for file "{file}". Do you want to proceed with the transfer? (yes/no): '
                    )
                    if confirmation.lower() == "yes":
                        print(f'Proceeding with transfer of file "{file}".')
                    else:
                        print(f'Transfer of file "{file}" cancelled.')
        else:
            print(f"Couldn't extract date from file: {file}")
            print(f"This file will not be moved.")


if __name__ == "__main__":
    main()
