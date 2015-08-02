import os

SOURCE_DATA_URLS = {
    'incidents': 'https://www.dallasopendata.com/api/views/tbnj-w5hb/rows.csv?accessType=DOWNLOAD',
    'arrests': 'https://www.dallasopendata.com/api/views/r4wm-ig9m/rows.csv?accessType=DOWNLOAD',
    'charges': 'https://www.dallasopendata.com/api/views/uzgk-dxyv/rows.csv?accessType=DOWNLOAD'
}


DATA_DIR = "./data-holding/dallas_crime/"
DOWNLOADED_DATA_DIR = os.path.join(DATA_DIR, "downloaded")
COMPILED_DATA_DIR = os.path.join(DATA_DIR, "compiled")

DOWNLOADED_INCIDENTS_DIR = os.path.join(DOWNLOADED_DATA_DIR, 'incidents')

def setup_space():
    os.makedirs(DOWNLOADED_INCIDENTS_DIR, exist_ok = True)
    os.makedirs(COMPILED_DATA_DIR, exist_ok = True)

