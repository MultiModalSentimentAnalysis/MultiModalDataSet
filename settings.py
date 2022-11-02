import os
from pathlib import Path

BASE_DIR = Path(".").resolve()
DATA_DIR = BASE_DIR / "dataset"
VIDEO_DIR = BASE_DIR / "videos"
LABELSTUDIO_DIR = BASE_DIR / "label-studio"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


# Define the URL where Label Studio is accessible and the API key for your user account
LABEL_STUDIO_URL = "http://localhost:8080"
API_KEY = "6fe48babe95a95c2581c48411430aaaed298b041"
