import os

LANDING_PAGE_URL = 'http://www.ons.gov.uk/ons/datasets-and-tables/index.html?pageSize=50&sortBy=none&sortDirection=none&newquery=baby+names'

DATA_DIR = "./data-holding/uk_baby_names/"
DOWNLOADED_DATA_DIR = os.path.join(DATA_DIR, "downloaded")
COMPILED_DATA_DIR = os.path.join(DATA_DIR, "compiled")


def setup_space():
    os.makedirs(DOWNLOADED_DATA_DIR, exist_ok = True)
    os.makedirs(COMPILED_DATA_DIR, exist_ok = True)


