import os


BUSINESS_ZIP_URL = 'https://extxfer.sfdph.org/food/SFBusinesses.zip'
PROGRAM_DATA_URL = 'https://extxfer.sfdph.org/food/SFFoodProgram_Complete_Data.zip'
DATA_PDF_URL = 'https://extxfer.sfdph.org/food/File%20Specifications.pdf'

DATA_DIR = "./data-holding/sf_restaurants/"
DOWNLOADED_DATA_DIR = os.path.join(DATA_DIR, "downloaded")
COMPILED_DATA_DIR = os.path.join(DATA_DIR, "compiled")


def setup_space():
    os.makedirs(DOWNLOADED_DATA_DIR, exist_ok = True)
    os.makedirs(COMPILED_DATA_DIR, exist_ok = True)
