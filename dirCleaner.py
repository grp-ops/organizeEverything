# A GRP UTILITY
# Clean up large directories by file type.

import os
import shutil
from pathlib import Path
import argparse

def organize_directory(directory_path):
    # Group files by type
    categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'],
        'Audio': ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.ts', '.jsx', '.tsx'],
    }
    
    # Check if directory exists
    directory = Path(directory_path)
    if not directory.exists() or not directory.is_dir():
        print(f"Error: {directory_path} is not a valid directory")
        return
    
    print(f"Sorting files in: {directory_path}")
    
    # Track progress
    total_files = 0
    moved_files = 0
    
    # Go through each file
    for file_path in directory.iterdir():
        if file_path.is_file():
            total_files += 1
            file_extension = file_path.suffix.lower()
            
            # Figure out where it belongs
            target_category = 'Others'  # Default bucket
            for category, extensions in categories.items():
                if file_extension in extensions:
                    target_category = category
                    break
            
            # Make folder if it doesn't exist
            category_dir = directory / target_category
            if not category_dir.exists():
                category_dir.mkdir()
                print(f"Created directory: {target_category}")
            
            # Move the file
            try:
                target_path = category_dir / file_path.name
                # Handle naming conflicts
                if target_path.exists():
                    base_name = file_path.stem
                    extension = file_path.suffix
                    counter = 1
                    while target_path.exists():
                        new_name = f"{base_name}_{counter}{extension}"
                        target_path = category_dir / new_name
                        counter += 1
                
                shutil.move(str(file_path), str(target_path))
                moved_files += 1
                print(f"Moved: {file_path.name} → {target_category}/{target_path.name}")
            except Exception as e:
                print(f"Error moving {file_path.name}: {e}")
    
    # Completed message
    print("Completed.")
    print(f"Total files processed: {total_files}")
    print(f"Files moved: {moved_files}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in a directory by type")
    parser.add_argument("directory", nargs="?", default=os.getcwd(),
                        help="Directory to organize (default: current directory)")
    args = parser.parse_args()
    
    organize_directory(args.directory)
