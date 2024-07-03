#!/usr/bin/env python3

import argparse
import os
from datetime import datetime
import hashlib
import shutil
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def list_external_drives(test_dir=None):
    directory = test_dir if test_dir is not None else "/Volumes"
    volumes = os.listdir(directory)
    return [vol for vol in volumes if vol != "Macintosh HD"]


def choose_drive(drives, purpose):
    print(f"Choose {purpose} drive:")
    for i, drive in enumerate(drives, 1):
        print(f"{i}. {drive}")

    while True:
        try:
            choice = int(input(f"Enter the number of the {purpose} drive: "))
            if 1 <= choice <= len(drives):
                return drives[choice - 1]
            else:
                logging.warning("Invalid choice. Please try again.")
        except ValueError:
            logging.warning("Please enter a valid number.")


def find_mp4_files(input_path):
    return find_files_with_ext(input_path, "mp4")


def find_files_with_ext(input_path, ext):
    mp4_files = []
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith(f".{ext}"):
                mp4_files.append(os.path.join(root, file))
    return mp4_files


def extract_date_from_file(file_path):
    try:
        stat = os.stat(file_path)
        return datetime.fromtimestamp(stat.st_mtime)
    except Exception as e:
        logging.error(f"Error extracting date from {file_path}: {str(e)}")
    return None


def get_day_labels(media_directory) -> dict[str, dict[str, str]]:
    for root, dirs, files in os.walk(media_directory):
        for file in files:
            os.remove(os.path.join(root, file))
    return {}


def get_destination_path(output_path, file_date, without_videos=False):
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
        "" if without_videos else "Videos",
        str(file_date.year),
        f"{file_date.month:02d}-{month_names[file_date.month-1]}",
    )


def calculate_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def organize(directory: str):

    # move original folder to "{folder_name}_Original"
    new_folder = f"{directory}_Original"
    counter = 1
    while os.path.exists(new_folder):
        new_folder = f"{directory}_Original_{counter}"
        counter += 1
    os.rename(directory, new_folder)
    logging.info(f"Renamed original folder to {new_folder}")
    os.makedirs(directory)
    mp4_files = find_mp4_files(new_folder)

    for file in mp4_files:
        file_date = extract_date_from_file(file)
        if file_date:
            dest_path = get_destination_path(directory, file_date, without_videos=True)
        else:
            logging.warning(f"Couldn't extract date from file: {file}")
            logging.warning(f"This file will not be moved.")


def transfer(volume_directory: str = "/Volumes"):
    external_drives = list_external_drives(volume_directory)
    if not external_drives:
        logging.error("No external drives found.")
        return

    input_drive = choose_drive(external_drives, "input")
    output_drive = choose_drive(external_drives, "output")

    logging.debug(f"Selected input drive: {input_drive}")
    logging.debug(f"Selected output drive: {output_drive}")

    input_path = os.path.join(volume_directory, input_drive)
    output_path = os.path.join(volume_directory, output_drive)

    mp4_files = find_mp4_files(input_path)

    for file in mp4_files:
        file_date = extract_date_from_file(file)
        if file_date:
            dest_path = get_destination_path(output_path, file_date)
            logging.debug(f"File: {file}")
            logging.debug(f"Date: {file_date}")
            logging.debug(f"Destination: {dest_path}")
            existing_files = find_mp4_files(dest_path)
            for existing_file in existing_files:

                source_checksum = calculate_checksum(file)
                dest_checksum = calculate_checksum(
                    os.path.join(dest_path, os.path.basename(existing_file))
                )

                if source_checksum == dest_checksum:
                    logging.warning(
                        f'Detected duplicate file "{os.path.relpath(dest_path, output_path)}", not overriding'
                    )
                    break

                if os.path.basename(file) == os.path.basename(existing_file):
                    logging.warning(
                        f'Detected duplicate file "{os.path.relpath(dest_path, output_path)}" with the same name, not overriding'
                    )
                    break
            else:
                # If the for loop didn't break, then copy the file
                dest_file_path = os.path.join(dest_path, os.path.basename(file))
                os.makedirs(dest_path, exist_ok=True)
                shutil.copy2(file, dest_file_path)
                logging.info(f"Copied file to {dest_file_path}")
        else:
            logging.warning(f"Couldn't extract date from file: {file}")
            logging.warning(f"This file will not be moved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transfer media files.")
    parser.add_argument(
        "-v",
        "--volume_directory",
        help="Specify the volume directory",
        type=str,
    )
    parser.add_argument(
        "-o",
        "--organize",
        help="Organize target dirctory",
        type=str,
    )
    args = parser.parse_args()
    if args.organize is not None:
        organize(args.organize)
    else:
        transfer(args.volume_directory)
