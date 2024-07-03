#!/bin/bash

# Function to generate checksums for files in a directory, ignoring .DS_Store files
generate_checksums() {
  local folder=$1
  local checksum_file=$2

  find "$folder" -type f ! -name ".DS_Store" -exec md5 -r {} + | sed "s| $folder/| |" > "$checksum_file"
}

# Function to compare the checksums of two directories
compare_checksums() {
  local folder1=$1
  local folder2=$2
  local checksum_file1="/tmp/folder1_checksums.txt"
  local checksum_file2="/tmp/folder2_checksums.txt"
  local logfile="mismatches.log"

  # Remove existing log file if it exists
  [ -f "$logfile" ] && rm "$logfile"

  # Generate checksums
  generate_checksums "$folder1" "$checksum_file1"
  generate_checksums "$folder2" "$checksum_file2"

  # Compare checksums
  local all_match=true

  while IFS= read -r line; do
    local checksum=$(echo "$line" | cut -d ' ' -f 1)
    local file=$(echo "$line" | cut -d ' ' -f 2-)
    if ! grep -q "$checksum" "$checksum_file2"; then
      echo "Checksum mismatch for file: $file" >> "$logfile"
      all_match=false
    fi
  done < "$checksum_file1"

  while IFS= read -r line; do
    local checksum=$(echo "$line" | cut -d ' ' -f 1)
    local file=$(echo "$line" | cut -d ' ' -f 2-)
    if ! grep -q "$checksum" "$checksum_file1"; then
      echo "Checksum mismatch for file: $file" >> "$logfile"
      all_match=false
    fi
  done < "$checksum_file2"

  if [ "$all_match" = true ]; then
    echo "Checksums match for all files."
  else
    echo "Checksums do not match. See $logfile for details."
  fi

  return 0
}

# Main script
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <folder1> <folder2>"
  exit 1
fi

folder1=$1
folder2=$2

compare_checksums "$folder1" "$folder2"
