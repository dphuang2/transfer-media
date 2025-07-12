# transfer-media

## Scripts

### transfer.sh

Organizes and copies media files from a source directory to a destination directory, optionally filtering by file extension. Files are organized into date-based folders, and their original filenames are preserved.

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
