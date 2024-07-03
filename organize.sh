#!/bin/bash

# Ensure two arguments are passed
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <source> <destination>"
  echo "  <source>: The source directory containing files to be processed."
  echo "  <destination>: The destination directory where processed files will be saved."
  exit 1
fi

# Assign positional arguments to variables
SOURCE_DIR=$1
DESTINATION_DIR=$2

# Run the exiftool command with the provided source and destination directories
exiftool -r -P -o . \
  '-FileName<$FileModifyDate/${FileModifyDate#;DateFmt("%Y-%m-%d_%H%M%S")}_%f%-c.%e' \
  '-FileName<$DateTimeOriginal/${DateTimeOriginal#;DateFmt("%Y-%m-%d_%H%M%S")}_%f%-c.%e' \
  '-FileName<$FileModifyDate/${model;}/${FileModifyDate#;DateFmt("%Y-%m-%d_%H%M%S")}_${model}_%f%-c.%e' \
  '-FileName<$DateTimeOriginal/${model;}/${DateTimeOriginal#;DateFmt("%Y-%m-%d_%H%M%S")}_${model}_%f%-c.%e' \
  -d "$DESTINATION_DIR/%Y/%m/%d" "$SOURCE_DIR"
