#!/bin/bash

# Ensure two or three arguments are passed
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  echo "Usage: $0 <source> <destination> [extension]"
  echo "  <source>: The source directory containing files to be processed."
  echo "  <destination>: The destination directory where processed files will be saved."
  echo "  [extension]: Optional file extension to filter (default: wav, mp4, jpg)."
  exit 1
fi

# Assign positional arguments to variables
SOURCE_DIR=$1
DESTINATION_DIR=$2
EXTENSION=$3

# Construct the exiftool command with optional extension filtering
if [ -n "$EXTENSION" ]; then
  EXIFTOOL_CMD="exiftool -r -P -ext ${EXTENSION} -o ."
else
  EXIFTOOL_CMD="exiftool -r -P -ext jpg -ext wav -ext mp4 -o ."
fi

# Organize into date-based folders, but preserve original filename
EXIFTOOL_CMD+=" -d \"$DESTINATION_DIR/%Y/%m/%d\" \"$SOURCE_DIR\""

# Print the command for verification
echo "Running command: $EXIFTOOL_CMD"

# Execute the command
eval $EXIFTOOL_CMD
