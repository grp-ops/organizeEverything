# Utility Lab
# Create project directory tree (Command Line Variant)
# Add as an alias command to bashrc/zshrc for easier use: Eg. -> alias newprj="python3 /home/username/scripts/CLI_createPrjDirectory.py"

import os
from pathlib import Path

def new_project(project_name):
    base_path = Path.cwd() / project_name

    folders = [
        "01_ASSETS/FROM_CLIENT",
        "01_ASSETS/SOURCED",
        "02_PROJECT_FILES/C4D",
        "02_PROJECT_FILES/AE",
        "03_RENDERS/DEV",
        "03_RENDERS/DEV/STILLS",
        "03_RENDERS/DEV/WIREFRAMES",
        "03_RENDERS/FINALS",
        "04_POST/AE",
    ]

    for folder in folders:
        folder_path = base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)

    print(f"Project structure for '{project_name}' created at {base_path}")

if __name__ == "__main__":
    project_name = input("Enter the project folder name (default: NEW_PROJECT): ").strip() or "NEW_PROJECT"
    new_project(project_name)
