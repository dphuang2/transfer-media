#!/bin/bash

# Check if the root directory is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <root_directory>"
  exit 1
fi

# Root directory to start the search
ROOT_DIR="$1"

# Function to check and label directories
check_and_label() {
  local dir_path="$1"
  local dd_folder="$(basename "$dir_path")"

  # Check if the directory already has a label
  if [[ "$dd_folder" != *-* ]]; then
    echo "Directory $dd_folder does not have a label."
    read -p "Enter a label for $dd_folder: " label
    if [[ -n "$label" ]]; then
      new_name="${dd_folder}-${label}"
      new_path="$(dirname "$dir_path")/$new_name"
      mv "$dir_path" "$new_path"
      echo "Renamed $dir_path to $new_path"
    else
      echo "No label provided. Skipping $dd_folder."
    fi
  else
    echo "Directory $dd_folder already has a label."
  fi
}

export -f check_and_label

# Find all directories matching the YYYY/MM/DD pattern and process them
find "$ROOT_DIR" -type d -regextype posix-extended -regex ".*/[0-9]{4}/[0-9]{2}/[0-9]{2}$" -exec bash -c 'check_and_label "$0"' {} \;
