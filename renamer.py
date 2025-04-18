# A GRP UTILITY
# Sometimes, you gotta rename stuff
# usage - python batch_rename.py /path/to/exr/files --pattern "frame_(\d+)" --format "shot.%04d.exr"

import os
import re
import argparse

def extract_frame_number(filename, regex, group_index=1):
    match = regex.search(filename)
    if match:
        try:
            return int(match.group(group_index))
        except ValueError:
            pass
    return None

def batch_rename_files(directory, pattern, new_format, group_index=1):
    """
    Renames all .exr files in the specified directory based on their extracted frame numbers.
    
    Parameters:
    - directory: The path to the directory containing the files.
    - pattern: A compiled regex pattern used to extract the frame number.
    - new_format: A format string (e.g. "frame.%04d.exr") for the new filenames.
    - group_index: The regex group index from which to extract the frame number.
    """
    # List and filter files to only include .exr files
    files = os.listdir(directory)
    exr_files = [f for f in files if f.lower().endswith('.exr')]
    
    # Extract frame numbers and build a list of tuples (frame_number, filename)
    frame_file_map = []
    for f in exr_files:
        frame = extract_frame_number(f, pattern, group_index)
        if frame is not None:
            frame_file_map.append((frame, f))
        else:
            print(f"Warning: No frame number found in file '{f}'. Skipping.")
    
    # Sort the files based on the extracted frame number
    frame_file_map.sort(key=lambda x: x[0])
    
    # Rename files in order
    for idx, (frame, old_name) in enumerate(frame_file_map):
        new_name = new_format % idx  # Uses the index to create a sequential naming order
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        print(f"Renaming: {old_name} -> {new_name}")
        os.rename(old_path, new_path)

def main():
    parser = argparse.ArgumentParser(
        description="Batch rename .exr files by extracting frame numbers and ordering them sequentially."
    )
    parser.add_argument("directory", help="Directory containing the .exr files.")
    parser.add_argument(
        "--pattern",
        default=r"(\d+)",
        help="Regex pattern to extract frame numbers. Default is '(\d+)' which matches the first sequence of digits."
    )
    parser.add_argument(
        "--group",
        type=int,
        default=1,
        help="Regex group index to extract the frame number from. Default is 1."
    )
    parser.add_argument(
        "--format",
        default="frame.%04d.exr",
        help="New filename format string (e.g., 'frame.%04d.exr'). Use a '%d' placeholder for the sequence number."
    )
    args = parser.parse_args()
    
    # Compile the provided regex pattern
    regex = re.compile(args.pattern)
    
    # Perform the batch renaming
    batch_rename_files(args.directory, regex, args.format, args.group)

if __name__ == "__main__":
    main()
