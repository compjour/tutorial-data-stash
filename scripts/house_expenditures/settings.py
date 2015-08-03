import os

LANDING_PAGE_URL = 'https://sunlightfoundation.com/tools/expenditures/'

DATA_DIR = "./data-holding/house_expenditures/"
DOWNLOADED_DATA_DIR = os.path.join(DATA_DIR, "downloaded")
COMPILED_DATA_DIR = os.path.join(DATA_DIR, "compiled")


def setup_space():
    os.makedirs(DOWNLOADED_DATA_DIR, exist_ok = True)
    os.makedirs(COMPILED_DATA_DIR, exist_ok = True)

