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
MAX_JOBS=4  # Number of parallel jobs

# Prepare for cleanup
PROGRESS_FILE=$(mktemp)
cleanup() {
  echo -e "\nAborting. Cleaning up..."
  rm -f "$PROGRESS_FILE" "$PROGRESS_FILE.lock"
  # Kill all child jobs
  jobs -p | xargs -r kill 2>/dev/null
  exit 130
}
trap cleanup SIGINT SIGTERM

echo 0 > "$PROGRESS_FILE"

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
  rm -f "$PROGRESS_FILE" "$PROGRESS_FILE.lock"
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

# Semaphore function to limit parallel jobs
semaphore() {
  local max=$1
  while (( $(jobs -rp | wc -l) >= max )); do
    sleep 0.2
  done
}

# Function to process a single file
process_file() {
  local file="$1"
  # Compute the target directory using exiftool date format
  local target_dir
  target_dir=$(exiftool -s3 -d "$DESTINATION_DIR/%Y/%m/%d" -FileModifyDate "$file")
  mkdir -p "$target_dir"
  exiftool -P -m \
    -o "$target_dir/%f.%e" \
    "$file" 2>&1 | grep -Ev 'already exists|files weren'\''t updated due to errors|image files updated'
  # Simple progress update (not atomic, but good enough for small parallelism)
  local n=$(<"$PROGRESS_FILE")
  n=$((n+1))
  echo "$n" > "$PROGRESS_FILE"
  print_progress "$n" "$TOTAL_FILES"
  printf "  %s\n" "$(basename "$file")"
}

# Export functions and variables for subshells
export -f process_file print_progress
export DESTINATION_DIR TOTAL_FILES PROGRESS_FILE

# Main parallel loop
for file in "${FILES[@]}"; do
  semaphore "$MAX_JOBS"
  process_file "$file" &
done
wait

# Final progress
print_progress "$TOTAL_FILES" "$TOTAL_FILES"
printf "\nDone!\n"
rm -f "$PROGRESS_FILE" "$PROGRESS_FILE.lock"
