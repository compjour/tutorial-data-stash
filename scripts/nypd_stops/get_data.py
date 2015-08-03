"""
python -m scripts.nypd_stops.get_data

data comes from:
http://www.nyc.gov/html/nypd/html/analysis_and_planning/stop_question_and_frisk_report.shtml

Original file are split into YYYY/MMDD.csv files (e.g. one for every day)

Note: This script is all-or-nothing... TODO: Make it less monolithic.
"""

import requests
import csv
from os import makedirs
import os.path
from itertools import groupby
from collections import defaultdict
from scripts.nypd_stops.settings import DOWNLOADED_DATA_DIR, BASE_URL, ZIP_URLS
from scripts.nypd_stops.settings import setup_space
from io import BytesIO
from zipfile import ZipFile

def foo_key(row):
    """
    row is a dict that contains 'datestop'
    `datestop` is a string like `1012012`

    Returns: string "101", e.g. Jan 1, but it doesn't really matter
    """
    d = row['datestop'][:-4]

    return d if d else "NA"


if __name__ == '__main__':
    setup_space()
    # Download the HTML
    urls = [BASE_URL +  z for z in ZIP_URLS]
    for url in urls:
        print("Downloading:", url)
        z = requests.get(url).content
        ## TODO
        ## Unzip and open exactly one YYYY.csv file
        ## script should fail if there is more than one file in the zip
        # with ZipFile(BytesIO(requests.get(z).content)) as zfile:
        #     zfile.extractall(DOWNLOADED_NATION_DIR)

        lines = resp.text.splitlines()
        headers = lines[0].split(',')

        print("Grouping data...")
        dategroups = defaultdict(list)
        c = csv.DictReader(lines)
        for dt, rows in groupby(c, key = foo_key):
            dategroups[dt].extend(list(rows))

        # write files
        for dt, rows in dategroups.items():
            yrslug = os.path.splitext(os.path.basename(url))[0]
            subdir = os.path.join(DOWNLOADED_DATA_DIR, yrslug)
            makedirs(subdir, exist_ok = True)
            fname = os.path.join(subdir, dt + '.csv')
            print("Writing:", fname)
            with open(fname, "w") as f:
                c = csv.DictWriter(f, fieldnames = headers)
                c.writeheader()
                c.writerows(rows)

