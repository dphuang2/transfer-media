import os
import time
from datetime import datetime


def list_external_drives():
    volumes = os.listdir("/Volumes")
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


def find_mp4_files(input_path):
    mp4_files = []
    for root, dirs, files in os.walk(input_path):
        if "DCIM" in root.split(os.sep):
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


def main():
    external_drives = list_external_drives()

    if not external_drives:
        print("No external drives found.")
        return

    input_drive = choose_drive(external_drives, "input")
    output_drive = choose_drive(external_drives, "output")

    input_path = os.path.join("/Volumes", input_drive)
    output_path = os.path.join("/Volumes", output_drive)

    mp4_files = find_mp4_files(input_path)

    for file in mp4_files:
        file_date = extract_date_from_file(file)
        if file_date:
            dest_path = get_destination_path(output_path, file_date)
            print(f"File: {file}")
            print(f"Date: {file_date}")
            print(f"Destination: {dest_path}")
            existing_files = find_mp4_files(dest_path)
            if file in existing_files:
                print(
                    f"File {file} already exists in the destination path: {dest_path}"
                )
        else:
            print(f"Couldn't extract date from file: {file}")
            print(f"This file will not be moved.")


if __name__ == "__main__":
    main()
