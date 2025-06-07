#!/usr/bin/env python3
# Utility Lab – Project Folder Gen - Updated to handle errors
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Set base path
NETWORK_PATH = Path(r"\\192.168.0.195\homes\utilitylab\Clients\UTILITYLAB\Y\Clients 2025")

# Folder structure
FOLDERS = [
    "01_ASSETS/FROM_CLIENT",
    "01_ASSETS/SOURCED/REFERENCE",
    "01_ASSETS/SOURCED/STOCK",
    "01_ASSETS/SOURCED/AUDIO",
    "02_PROJECT_FILES/C4D",
    "02_PROJECT_FILES/C4D/tex",
    "02_PROJECT_FILES/C4D/cache",
    "02_PROJECT_FILES/AE",
    "02_PROJECT_FILES/PYTHON_TOOLS",
    "03_RENDERS/DEV/STILLS",
    "03_RENDERS/DEV/WIREFRAMES",
    "03_RENDERS/FINALS",
    "04_POST/AE",
    "04_POST/EDIT",
    "05_EXPORTS"
]

# Scripts to install
UTILITIES = {
    "rename_sequence.py": '''
import os
import re

def rename_sequence(folder_path):
    pattern = re.compile(r"(.*?)(\\d{3,})(\\..+)")
    for filename in sorted(os.listdir(folder_path)):
        match = pattern.match(filename)
        if match:
            base, frame, ext = match.groups()
            new_name = f"{base}{int(frame):04d}{ext}"
            os.rename(os.path.join(folder_path, filename),
                      os.path.join(folder_path, new_name))
''',
    "cleanup.py": '''
import os

def cleanup(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file in [".DS_Store", "thumbs.db"] or file.endswith("~"):
                os.remove(os.path.join(root, file))
''',
    "generate_summary.py": '''
from pathlib import Path

def generate_summary(base_path):
    summary_path = Path(base_path) / "asset_summary.md"
    with open(summary_path, "w") as f:
        for subdir in Path(base_path, "01_ASSETS").rglob("*"):
            if subdir.is_file():
                f.write(f"- {subdir.relative_to(base_path)}\\n")
'''
}

# Project creation logic
def new_project(project_name):
    base_path = NETWORK_PATH / project_name

    # Handle existing folders
    if base_path.exists():
        confirm = messagebox.askyesno("Folder Exists",
            f"The folder '{project_name}' already exists.\nDo you want to continue and overwrite its contents?")
        if not confirm:
            return

    try:
        for folder in FOLDERS:
            (base_path / folder).mkdir(parents=True, exist_ok=True)

        # Create PureRef file
        pure_ref = base_path / "01_ASSETS/SOURCED/REFERENCE" / f"{project_name}.pur"
        pure_ref.touch()

        # Add utility scripts
        tools_path = base_path / "02_PROJECT_FILES/PYTHON_TOOLS"
        for name, content in UTILITIES.items():
            (tools_path / name).write_text(content.strip())

        # Write log file
        logfile = base_path / "creation_log.md"
        with logfile.open("w") as f:
            f.write(f"# Project: {project_name}\n")
            f.write(f"Created on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("## Folder Structure:\n")
            for folder in FOLDERS:
                f.write(f"- {folder}\n")

        messagebox.showinfo("Done", f"Project '{project_name}' created at:\n{base_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not create folders:\n{e}")

# GUI
def launch_gui():
    def submit(event=None):
        name = entry.get().strip().replace(" ", "_").upper()
        if name:
            new_project(name)
            window.destroy()

    window = tk.Tk()
    window.title("UL Project Gen")
    window.geometry("420x160")
    window.configure(bg="#1e1e1e")

    style = ttk.Style(window)
    style.theme_use("clam")
    style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Helvetica", 11))
    style.configure("TButton", background="#3c3f41", foreground="#ffffff", font=("Helvetica", 10))
    style.configure("TEntry", fieldbackground="#2b2b2b", foreground="#ffffff")

    ttk.Label(window, text="Enter Project Name:").pack(padx=10, pady=(20, 5))
    global entry
    entry = ttk.Entry(window, width=40)
    entry.pack(padx=10, pady=5)
    entry.focus()

    entry.bind("<Return>", submit)
    ttk.Button(window, text="Create Project", command=submit).pack(pady=15)

    window.mainloop()

if __name__ == "__main__":
    launch_gui()
