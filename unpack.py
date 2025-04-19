# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer",
# ]
# ///

import re
import shutil
from pathlib import Path
from typing import Annotated

import typer


def get_matching_files(root_path: Path, extension: str) -> list[Path]:
    """
    Find all files with the specified extension
    """
    matching_files: list[Path] = []
    if re.match(r"^[a-zA-Z0-9]+$", extension):
        # Simple extension - use glob for both lowercase and uppercase
        for path in root_path.glob(f"**/*.{extension.lower()}"):
            matching_files.append(path)
        for path in root_path.glob(f"**/*.{extension.upper()}"):
            matching_files.append(path)
        return matching_files

    for path in root_path.glob("**/*"):
        if path.is_file() and re.search(f"\\.({extension})$", path.name, re.IGNORECASE):
            matching_files.append(path)
    return matching_files


def main(
    root_dir: Annotated[str, typer.Argument(help="Root directory to scan")],
    extension: Annotated[
        str,
        typer.Argument(
            help="File extension to process (e.g., 'jpg' or regex pattern like '(jpg|png)')"
        ),
    ],
    pattern: Annotated[
        str,
        typer.Option(help="Regular expression pattern to match filenames to keep"),
    ],
    dry_run: Annotated[
        bool, typer.Option(help="Show what would be moved without actually moving")
    ] = False,
) -> None:
    """
    Organize files in the directory structure:
    - Process files with the specified extension (can be a simple extension or regex pattern)
    - Keep files matching the provided regular expression pattern
    - Move all other matching files to a '_other' directory in the root
    """
    root_path = Path(root_dir).resolve()
    other_dir = root_path / "_other"

    # Create _other directory if it doesn't exist and we're not in dry-run mode
    if not dry_run and not other_dir.exists():
        other_dir.mkdir(parents=True)
        print(f"Created directory: {other_dir}")

    # Find all files with the specified extension
    matching_files: list[Path] = get_matching_files(root_path, extension)

    kept_files = 0
    moved_files = 0
    for file_path in matching_files:
        filename = file_path.name
        should_keep = bool(re.search(pattern, filename))

        if should_keep:
            kept_files += 1
            print(f"Keeping: {file_path.relative_to(root_path)}")
        else:
            moved_files += 1
            dest_path = other_dir / file_path.name
            counter = 1
            original_stem = dest_path.stem
            while dest_path.exists():
                dest_path = other_dir / f"{original_stem}_{counter}{dest_path.suffix}"
                counter += 1

            if dry_run:
                print(
                    f"Would move: {file_path.relative_to(root_path)} -> {dest_path.relative_to(root_path)}"
                )
            else:
                print(
                    f"Moving: {file_path.relative_to(root_path)} -> {dest_path.relative_to(root_path)}"
                )
                shutil.move(file_path, dest_path)

    print("\nSummary:")
    print(f"  Files kept in place: {kept_files}")
    print(
        f"  Files {'would be' if dry_run else ''} moved to {other_dir.relative_to(root_path)}: {moved_files}"
    )


if __name__ == "__main__":
    typer.run(main)
