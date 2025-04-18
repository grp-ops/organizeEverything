from os import scandir, rename, makedirs
from os.path import splitext, exists, join, isfile
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# Set directories
source_dir = r"A:\DOWNLOADS"
dest_dir_sfx = r"A:\DOWNLOADS\sfx"
dest_dir_music = r"A:\DOWNLOADS\music"
dest_dir_video = r"A:\DOWNLOADS\videos"
dest_dir_image = r"A:\DOWNLOADS\images"
dest_dir_documents = r"A:\DOWNLOADS\docs"
dest_dir_zip = r"A:\DOWNLOADS\zipfiles"

# Extensions
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp", ".heic", ".svg", ".ico"]
video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
zipfile_extensions = [".zip", ".rar"]

def make_unique(dest, name):
    # Ensure unique file names.
    filename, extension = splitext(name)
    counter = 1
    while exists(join(dest, name)):
        name = f"{filename}({counter}){extension}"
        counter += 1
    return name

def move_file(dest, entry, name):
    try:
        if not exists(dest):
            makedirs(dest)
        if exists(join(dest, name)):
            name = make_unique(dest, name)
        move(entry.path, join(dest, name))
        logging.info(f"Moved file: {name} -> {dest}")
    except PermissionError:
        logging.error(f"Permission denied while moving {name}")
    except Exception as e:
        logging.error(f"Error moving {name}: {str(e)}")

class MoverHandler(FileSystemEventHandler):
    # Handle file organization.
    def on_modified(self, event):
        # Run when a change is detected in the source directory.
        with scandir(source_dir) as entries:
            for entry in entries:
                if isfile(entry):  # Ignore directories
                    self.check_file_type(entry)

    def check_file_type(self, entry):
        # Determine the type of file and move accordingly.
        name = entry.name
        if self.match_extension(name, audio_extensions):
            dest = dest_dir_sfx if entry.stat().st_size < 10_000_000 or "SFX" in name else dest_dir_music
            move_file(dest, entry, name)
        elif self.match_extension(name, video_extensions):
            move_file(dest_dir_video, entry, name)
        elif self.match_extension(name, image_extensions):
            move_file(dest_dir_image, entry, name)
        elif self.match_extension(name, document_extensions):
            move_file(dest_dir_documents, entry, name)
        elif self.match_extension(name, zipfile_extensions):
            move_file(dest_dir_zip, entry, name)

    @staticmethod
    def match_extension(filename, extensions):
        # Check if file matches given extensions.
        return any(filename.lower().endswith(ext) for ext in extensions)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    observer = Observer()
    event_handler = MoverHandler()
    observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
            loading = print("*" * 10 + " MOVING FILES " + "*" * 10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("User Exited.")
