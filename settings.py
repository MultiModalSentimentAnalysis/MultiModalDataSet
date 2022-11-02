import os
from pathlib import Path

BASE_DIR = Path(".")
DATA_DIR = BASE_DIR / "dataset"
VIDEO_DIR = BASE_DIR / "videos"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
