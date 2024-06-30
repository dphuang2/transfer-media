import os


def list_external_drives():
    volumes = os.listdir("/Volumes")
    external_drives = [vol for vol in volumes if vol != "Macintosh HD"]
    return external_drives


def choose_drive(drives, purpose):
    print(f"\nChoose {purpose} drive:")
    for i, drive in enumerate(drives, 1):
        print(f"{i}. {drive}")

    while True:
        try:
            choice = int(input(f"Enter the number of the {purpose} drive: "))
            if 1 <= choice <= len(drives):
                return drives[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def main():
    external_drives = list_external_drives()

    if not external_drives:
        print("No external drives found.")
        return

    print("External drives found:")
    for drive in external_drives:
        print(f"- {drive}")

    input_drive = choose_drive(external_drives, "input")
    remaining_drives = [d for d in external_drives if d != input_drive]

    if not remaining_drives:
        print("No other external drives available for output.")
        return

    output_drive = choose_drive(remaining_drives, "output")

    print("\nYou have selected:")
    print(f"Input drive: {input_drive}")
    print(f"Output drive: {output_drive}")

    # Here you can add code to work with the selected drives
    # For example:
    input_path = os.path.join("/Volumes", input_drive)
    output_path = os.path.join("/Volumes", output_drive)
    print(f"\nInput drive path: {input_path}")
    print(f"Output drive path: {output_path}")


if __name__ == "__main__":
    main()
