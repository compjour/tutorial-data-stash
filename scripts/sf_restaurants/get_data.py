"""
run:
    $ python -m scripts.sf_restaurants.get_data
"""
from io import BytesIO
import os.path
import requests
from zipfile import ZipFile
from scripts.sf_restaurants.settings import setup_space
from scripts.sf_restaurants.settings import BUSINESS_ZIP_URL, PROGRAM_DATA_URL, DATA_PDF_URL
from scripts.sf_restaurants.settings import DOWNLOADED_DATA_DIR


if __name__ == "__main__":
    setup_space()
    for url in [BUSINESS_ZIP_URL, PROGRAM_DATA_URL]:
        print("Downloading:", url)
        with ZipFile(BytesIO(requests.get(url).content)) as zfile:
            zfile.extractall(DOWNLOADED_DATA_DIR)
    # download PDF for recordkeeping
    pname = os.path.join(DOWNLOADED_DATA_DIR, os.path.basename(DATA_PDF_URL))
    print("Downloading documentation:", DATA_PDF_URL, "\n\tinto:", pname)
    pdfdata = requests.get(DATA_PDF_URL).content
    with open(pname, 'wb') as p:
        p.write(pdfdata)
