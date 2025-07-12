#!/bin/bash

# Ensure two or three arguments are passed
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  echo "Usage: $0 <source> <destination> [extension]"
  echo "  <source>: The source directory containing files to be processed."
  echo "  <destination>: The destination directory where processed files will be saved."
  echo "  [extension]: Optional file extension to filter (default: wav, mp4, jpg)."
  exit 1
fi

SOURCE_DIR=$1
DESTINATION_DIR=$2
EXTENSION=$3

# Build the find command for the extension(s)
FILES=()
if [ -n "$EXTENSION" ]; then
  while IFS= read -r -d '' file; do
    FILES+=("$file")
  done < <(find "$SOURCE_DIR" -type f -iname "*.$EXTENSION" -print0)
else
  while IFS= read -r -d '' file; do
    FILES+=("$file")
  done < <(find "$SOURCE_DIR" -type f \( -iname "*.jpg" -o -iname "*.wav" -o -iname "*.mp4" \) -print0)
fi

TOTAL_FILES=${#FILES[@]}
if [ "$TOTAL_FILES" -eq 0 ]; then
  echo "No files found to transfer."
  exit 0
fi

# Progress bar function
print_progress() {
  local current=$1
  local total=$2
  local width=40
  local percent=$(( 100 * current / total ))
  local filled=$(( width * current / total ))
  local empty=$(( width - filled ))
  printf "\r["
  for ((i=0; i<filled; i++)); do printf "#"; done
  for ((i=0; i<empty; i++)); do printf "-"; done
  printf "] %3d%% (%d/%d)" "$percent" "$current" "$total"
}

# Transfer files with progress
for i in "${!FILES[@]}"; do
  file="${FILES[$i]}"
  print_progress $((i+1)) $TOTAL_FILES
  printf "  %s" "$(basename "$file")"
  exiftool -P -m \
    '-Directory<${FileModifyDate}' \
    '-FileName=%f.%e' \
    -d "$DESTINATION_DIR/%Y/%m/%d" \
    "$file" > /dev/null
  printf "\r"
done
print_progress $TOTAL_FILES $TOTAL_FILES
printf "\nDone!\n"
