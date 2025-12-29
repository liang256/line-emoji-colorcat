import re
import sys
from pathlib import Path


def rename_files(folder=None):
    """Rename files by extracting numbers and converting to 3-digit format.

    Example: 'image_00034_out.png' -> '034.png'
    """
    if folder:
        folder_path = Path(folder)
    else:
        folder_path = Path.cwd()

    if not folder_path.exists():
        print(f"Error: Folder {folder_path} does not exist")
        return

    # Find all PNG files
    png_files = list(folder_path.glob("*.png"))

    if not png_files:
        print("No PNG files found in folder")
        return

    renamed = 0
    for file in png_files:
        # Extract all numbers from filename
        numbers = re.findall(r'\d+', file.stem)

        if not numbers:
            print(f"Skipping {file.name} - no numbers found")
            continue

        # Use the first number found
        number = int(numbers[0])

        # Create new name with 3 digits
        new_name = f"{number:03d}.png"
        new_path = file.parent / new_name

        # Check if target already exists
        if new_path.exists() and new_path != file:
            print(f"Skipping {file.name} - {new_name} already exists")
            continue

        # Rename
        if new_path != file:
            file.rename(new_path)
            print(f"{file.name} -> {new_name}")
            renamed += 1

    print(f"\nRenamed {renamed} files")


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else None
    rename_files(folder)
