import os

SOURCE_DATA_URLS = [
    'https://data.lacity.org/api/views/iatr-8mqm/rows.csv?accessType=DOWNLOAD', # 2013
    'https://data.lacity.org/api/views/eta5-h8qx/rows.csv?accessType=DOWNLOAD' # 2014
]


DATA_DIR = "./data-holding/la_crime/"
DOWNLOADED_DATA_DIR = os.path.join(DATA_DIR, "downloaded")
COMPILED_DATA_DIR = os.path.join(DATA_DIR, "compiled")


def setup_space():
    os.makedirs(DOWNLOADED_DATA_DIR, exist_ok = True)
    os.makedirs(COMPILED_DATA_DIR, exist_ok = True)
