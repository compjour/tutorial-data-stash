"""
run:
    $ python -m scripts.las_vegas_restaurants.get_data
"""
from io import BytesIO
import os.path
import requests
from zipfile import ZipFile
from scripts.las_vegas_restaurants.settings import setup_space
from scripts.las_vegas_restaurants.settings import DATA_ZIP_URL
from scripts.las_vegas_restaurants.settings import DOWNLOADED_DATA_DIR, SCHEMA_URL


if __name__ == "__main__":
    setup_space()
    print("Downloading:", DATA_ZIP_URL)
    with ZipFile(BytesIO(requests.get(DATA_ZIP_URL).content)) as zfile:
        zfile.extractall(DOWNLOADED_DATA_DIR)
    # download schema.sql.txt for recordkeeping
    pname = os.path.join(DOWNLOADED_DATA_DIR, os.path.basename(SCHEMA_URL))
    print("Downloading schema:", SCHEMA_URL, "\n\tinto:", pname)
    pdfdata = requests.get(SCHEMA_URL).content
    with open(pname, 'wb') as p:
        p.write(pdfdata)
