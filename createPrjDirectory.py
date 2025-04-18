# A GRP UTILITY
# Create project directory tree (with GUI)

import os
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog, messagebox

# Path to create folder in.
DIRECTORY_PATH = Path(r"C:\path\to\your\directory") # <- Replace this.
def new_project(project_name):
    base_path = DIRECTORY_PATH / project_name

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

    try:
        for folder in folders:
            (base_path / folder).mkdir(parents=True, exist_ok=True)

        messagebox.showinfo("Done", f"Project '{project_name}' created at:\n{base_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not create folders:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    project_name = simpledialog.askstring("Project Name", "Enter project name:")
    if project_name:
        new_project(project_name)
