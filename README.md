# transfer-media

## Scripts

### transfer.sh

Organizes and copies media files from a source directory to a destination directory, optionally filtering by file extension. Files are organized into date-based folders, and their original filenames are preserved.

**Best Practice:**
It is recommended to organize all files you want to transfer into their own folder on the SD card before running the transfer. This helps avoid accidental transfer of unwanted files and makes the process more manageable.

**Example:**

```sh
./transfer.sh /Volumes/SD_Card/DCIM/7-12-2025_Import ~/Downloads/test mp4
```

**Usage:**

```sh
./transfer.sh <source> <destination> [extension]
```

- `<source>`: The source directory containing files to be processed.
- `<destination>`: The destination directory where processed files will be saved.
- `[extension]`: (Optional) File extension to filter (e.g., jpg, wav, mp4). If omitted, defaults to jpg, wav, and mp4.

**Example:**

```sh
./transfer.sh /path/to/source /path/to/destination mp4
```

---

### label.sh

Interactively labels date-based folders (e.g., `/YYYY/MM/DD`) under a root directory by appending a user-provided label to the folder name. Prompts the user for a label if the folder does not already have one.

**Usage:**

```sh
./label.sh <root_directory>
```

- `<root_directory>`: The root directory to start searching for date-based folders.

**Example:**

```sh
./label.sh /path/to/destination
```

The script will prompt you to enter a label for each unlabelled date folder it finds.

---

### grade.sh

Applies the DJI D-Log M → Rec.709 3D LUT to DJI (e.g. Osmo Pocket 3) footage recorded in D-Log M mode, restoring standard coloring. Keeps 4K 10-bit HEVC at near-transparent quality and copies audio untouched. Graded copies are saved next to each input, suffixed with `-graded`.

**Usage:**

```sh
./grade.sh <file_or_directory>
```

- `<file_or_directory>`: A single MP4, or a directory of MP4s to grade in place. Already-graded files are skipped.

**Example:**

```sh
./grade.sh /Volumes/Dylan1TB/Vlogs/2024/01
```

Requires `ffmpeg` (e.g. `brew install ffmpeg`). The LUT (`DLogM_to_Rec709.cube`) must sit next to the script.
