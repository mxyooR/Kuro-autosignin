import os

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
STATIC_PATH = os.path.join(PROJECT_PATH, "static")
PICTURE_PATH = os.path.join(STATIC_PATH, "pictures")
TMP_PATH = os.path.join(STATIC_PATH, "tmp")
TMP_BACKGROUND_PATH = os.path.join(TMP_PATH, "background")


def mk_dir(file_path: str):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
