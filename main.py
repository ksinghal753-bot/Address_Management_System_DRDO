"""Workspace entrypoint for the Address Management System.

This proxy allows the nested application to be started from the outer workspace root
using `python main.py` and through VS Code run/debug.
"""

import os
import sys
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "Address-Management-Offline-System-main"
if not APP_DIR.is_dir():
    raise FileNotFoundError(
        f"Nested application folder not found: {APP_DIR}\n"
        "Please make sure the repository is unpacked correctly."
    )

# Ensure the nested app imports correctly
sys.path.insert(0, str(APP_DIR))
os.chdir(str(APP_DIR))

if __name__ == "__main__":
    runpy.run_path(str(APP_DIR / "main.py"), run_name="__main__")
