import os
import sys
import label_studio
from pathlib import Path
sys.path.append(str(Path(".").resolve()))
from settings import DATA_DIR

# symlink
static_path = Path(os.path.abspath(label_studio.__file__)).parent / "core" / "static_build"
print(static_path)
print(DATA_DIR)

symlink_dataset_path = static_path / "dataset"
try:
    os.symlink(DATA_DIR, symlink_dataset_path)
except:
    print("symlink already exists")



