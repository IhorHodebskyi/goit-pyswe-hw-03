import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def copy_file(src_path: Path, dest_dir: Path):
    ext = src_path.suffix.lstrip('.') or 'no_ext'
    target_dir = dest_dir / ext
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, target_dir / src_path.name)

def process_directory(src_dir: Path, dest_dir: Path, executor: ThreadPoolExecutor):
    for item in src_dir.iterdir():
        if item.is_file():
            executor.submit(copy_file, item, dest_dir)
        elif item.is_dir():
            executor.submit(process_directory, item, dest_dir, executor)


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <source_directory> [destination_directory]")
        sys.exit(1)
    
    src_dir = Path(sys.argv[1])
    dest_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('dist')
    
    if not src_dir.exists() or not src_dir.is_dir():
        print(f"Error: Source directory '{src_dir}' does not exist or is not a directory.")
        sys.exit(1)
    
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    with ThreadPoolExecutor() as executor:
        process_directory(src_dir, dest_dir, executor)
    
    print(f"Files sorted successfully into '{dest_dir}'")

if __name__ == "__main__":
    main()


