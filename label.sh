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
    echo "Path $dir_path does not have a label."
    echo -n "Enter a label for $dir_path: "
    read label < /dev/tty
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

# Use find and xargs to avoid subshell issue
find "$ROOT_DIR" -type d | grep -E "/[0-9]{4}/[0-9]{2}/[0-9]{2}$" | while IFS= read -r dir; do
  check_and_label "$dir"
done
