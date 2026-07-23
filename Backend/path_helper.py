import os

# Backend folder path
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Project root
ROOT_DIR = os.path.dirname(BACKEND_DIR)

def frontend_path(*paths):
    return os.path.join(ROOT_DIR, "Frontend", *paths)

def backend_path(*paths):
    return os.path.join(ROOT_DIR, "Backend", *paths)

def data_path(*paths):
    return os.path.join(ROOT_DIR, "Data", *paths)

def frontend_files(*paths):
    return os.path.join(ROOT_DIR, "Frontend", "Files", *paths)

def graphics_path(*paths):
    return os.path.join(ROOT_DIR, "Frontend", "Graphics", *paths)

