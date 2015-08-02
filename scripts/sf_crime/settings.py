import os

SOURCE_DATA_URL = 'https://data.sfgov.org/api/views/tmnf-yvry/rows.csv?accessType=DOWNLOAD'

DATA_DIR = "./data-holding/sf_crime/"
DOWNLOADED_DATA_DIR = os.path.join(DATA_DIR, "downloaded")
COMPILED_DATA_DIR = os.path.join(DATA_DIR, "compiled")

def setup_space():
    os.makedirs(DOWNLOADED_DATA_DIR, exist_ok = True)
    os.makedirs(COMPILED_DATA_DIR, exist_ok = True)
