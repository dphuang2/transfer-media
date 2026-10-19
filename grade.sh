#!/bin/bash

# Check if a file or directory is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <file_or_directory>"
    echo "  <file_or_directory>: An MP4 recorded in DJI D-Log M, or a directory containing them."
    echo "  Graded copies are saved next to each input, suffixed with -graded."
    exit 1
fi

INPUT="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LUT="$SCRIPT_DIR/DLogM_to_Rec709.cube"

if ! command -v ffmpeg > /dev/null; then
    echo "ffmpeg is required but not installed. Install it with: brew install ffmpeg"
    exit 1
fi

if [ ! -f "$LUT" ]; then
    echo "LUT not found at $LUT"
    exit 1
fi

# Collect MP4 files (skip already-graded outputs)
FILES=()
if [ -d "$INPUT" ]; then
    while IFS= read -r -d '' file; do
        FILES+=("$file")
    done < <(find "$INPUT" -maxdepth 1 -type f \( -iname "*.mp4" \) ! -iname "*-graded*" -print0)
elif [ -f "$INPUT" ]; then
    FILES+=("$INPUT")
else
    echo "No such file or directory: $INPUT"
    exit 1
fi

if [ "${#FILES[@]}" -eq 0 ]; then
    echo "No MP4 files found to grade."
    exit 0
fi

for file in "${FILES[@]}"; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    name="${base%.*}"
    ext="${base##*.}"
    output="$dir/${name}-graded.${ext}"

    if [ -f "$output" ]; then
        echo "Skipping $base (already graded)."
        continue
    fi

    echo "Grading $base ..."
    ffmpeg -y -v warning -stats -i "$file" \
        -vf "lut3d=$LUT,format=yuv420p10le" \
        -c:v libx265 -preset medium -crf 18 -tag:v hvc1 \
        -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
        -c:a copy -movflags +faststart \
        "$output"
    echo "Saved $output"
done

echo "Done!"
