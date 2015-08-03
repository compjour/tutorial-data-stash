import os

BASE_URL = 'http://www.nyc.gov/html/nypd/html/analysis_and_planning/'
ZIP_URLS = ['2012_sqf_csv.zip', '2013_sqf_csv.zip', '2014_sqf_csv.zip']
DATA_DIR = "./data-holding/nypd_stops/"
DOWNLOADED_DATA_DIR = os.path.join(DATA_DIR, "downloaded")
COMPILED_DATA_DIR = os.path.join(DATA_DIR, "compiled")


def setup_space():
    os.makedirs(DOWNLOADED_DATA_DIR, exist_ok = True)
    os.makedirs(COMPILED_DATA_DIR, exist_ok = True)

