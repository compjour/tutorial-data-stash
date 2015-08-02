"""
http://www.southernnevadahealthdistrict.org/restaurants/inspect-downloads.php
"""
import os

DATA_ZIP_URL = 'http://www.southernnevadahealthdistrict.org/restaurants/download/restaurants.zip'
SCHEMA_URL = 'http://www.southernnevadahealthdistrict.org/restaurants/download/restaurants.sql.txt'

DATA_DIR = "./data-holding/las_vegas_restaurants/"
DOWNLOADED_DATA_DIR = os.path.join(DATA_DIR, "downloaded")
COMPILED_DATA_DIR = os.path.join(DATA_DIR, "compiled")


def setup_space():
    os.makedirs(DOWNLOADED_DATA_DIR, exist_ok = True)
    os.makedirs(COMPILED_DATA_DIR, exist_ok = True)
