#!/bin/bash

# Check if the root directory is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <root_directory>"
    exit 1
fi

# Root directory to start the search
ROOT_DIR="$1"

# Function to sanitize the label by removing problematic characters
sanitize_label() {
    local label="$1"
    # Remove any character that is not a letter, number, hyphen, underscore, space, "@", "+", or "&"
    echo "$label" | tr -cd '[:alnum:]-_ @+&'
}

# Function to check and label directories
check_and_label() {
    local dir_path="$1"
    local dd_folder="$(basename "$dir_path")"

    # Check if the directory already has a label
    if [[ "$dd_folder" != *-* ]]; then
        echo "Path $dir_path does not have a label."

        # Open the folder in Finder
        open "$dir_path"

        while true; do
            echo -n "Enter a label for $dir_path: "
            read label < /dev/tty

            if [[ -n "$label" ]]; then
                sanitized_label=$(sanitize_label "$label")
                if [[ -z "$sanitized_label" ]]; then
                    echo "Invalid label provided. Only letters, numbers, hyphens, underscores, spaces, '@', and '+' are allowed."
                else
                    new_name="${dd_folder}-${sanitized_label}"
                    new_path="$(dirname "$dir_path")/$new_name"
                    mv "$dir_path" "$new_path"
                    echo "Renamed $dir_path to $new_path"
                    break
                fi
            else
                echo "No label provided. Skipping $dd_folder."
                break
            fi
        done

        # Close the Finder window
        osascript -e 'tell application "Finder" to close window 1'
    else
        echo "Directory $dd_folder already has a label."
    fi
}

export -f check_and_label
export -f sanitize_label

# Use find and xargs to avoid subshell issue
find "$ROOT_DIR" -type d | grep -E "/[0-9]{4}/[0-9]{2}/[0-9]{2}$" | while IFS= read -r dir; do
    check_and_label "$dir"
done
