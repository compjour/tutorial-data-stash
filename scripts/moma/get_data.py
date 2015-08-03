"""
python -m scripts.moma.get_data

Data comes from The Museum of Modern Art
https://github.com/MuseumofModernArt/collection

Original CSV is split into year files based on acquisition date (`DateAcquired`)
    files for easier version control
"""
import requests
import csv
import os.path
from itertools import groupby
from collections import defaultdict
from scripts.moma.settings import DOWNLOADED_DATA_DIR, SOURCE_DATA_URL
from scripts.moma.settings import setup_space


def fookey(row):
    """ return 1994 from `DateAcquired` value of '1995-01-17' """
    yr = row['DateAcquired'].split('-')[0]
    return yr if yr else "None"

if __name__ == '__main__':
    setup_space()
    print("Downloading:", SOURCE_DATA_URL)
    resp = requests.get(SOURCE_DATA_URL)
    print("Grouping data...")
    lines = resp.text.splitlines()
    headers = lines[0].split(',')
    dategroups = defaultdict(list)
    for dt, rows in groupby(csv.DictReader(lines), key = fookey):
        dategroups[dt].extend(list(rows))

    for dt, rows in dategroups.items():
        fname = os.path.join(DOWNLOADED_DATA_DIR, dt + '.csv')
        print("Writing:", fname)
        with open(fname, "w") as f:
            c = csv.DictWriter(f, fieldnames = headers)
            c.writeheader()
            c.writerows(rows)
