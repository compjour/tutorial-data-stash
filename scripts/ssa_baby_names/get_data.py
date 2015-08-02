"""
run:
    $ python -m scripts.ssa_baby_names.get_data

Downloads the names and namesbystate zip files from the Social Security Administration
    and unzips their contents to ssa_baby_names/downloaded
"""
from scripts.ssa_baby_names.settings import setup_space
from scripts.ssa_baby_names.settings import DOWNLOADED_NATION_DIR, DOWNLOADED_STATES_DIR
from io import BytesIO
from zipfile import ZipFile
import os.path
import requests
NATION_ZIP_URL = 'http://www.ssa.gov/OACT/babynames/names.zip'
STATES_ZIP_URL = 'http://www.ssa.gov/oact/babynames/state/namesbystate.zip'


if __name__ == '__main__':
    setup_space()
    # Get the nationwide data
    print("Downloading:", NATION_ZIP_URL)
    with ZipFile(BytesIO(requests.get(NATION_ZIP_URL).content)) as zfile:
        zfile.extractall(DOWNLOADED_NATION_DIR)
    # Now get the states
    print("Downloading:", STATES_ZIP_URL)
    with ZipFile(BytesIO(requests.get(STATES_ZIP_URL).content)) as zfile:
        zfile.extractall(DOWNLOADED_STATES_DIR)
