import os
from app.config import LOG_ROOT_DIR

def list_log_files():
    files_with_paths = []
    for root, _, files in os.walk(LOG_ROOT_DIR):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), LOG_ROOT_DIR)
            files_with_paths.append(relative_path.replace('\\', '/'))
    print("List of Log files:")
    print(files_with_paths)
    return files_with_paths