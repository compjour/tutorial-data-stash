"""
python -m scripts.sf_crime.get_data

data comes from Socrata:
https://data.sfgov.org/Public-Safety/SFPD-Incidents-from-1-January-2003/tmnf-yvry

Original file is split into by-month/year (of reported incident date, 'Date')
    CSV files for easier version control
"""

import requests
import csv
import os.path
from itertools import groupby
from collections import defaultdict
from scripts.sf_crime.settings import DOWNLOADED_DATA_DIR, SOURCE_DATA_URL
from scripts.sf_crime.settings import setup_space


def foo_date(row):
    """
    row is a dict that contains 'Date' field
    `Date` is a string like `09/25/2015`

    Returns: string "2015-09"
    """
    mth, day, yr = row['Date'].split('/')
    return "%s-%s" % (yr, mth)


if __name__ == '__main__':
    setup_space()
    print("Downloading:", SOURCE_DATA_URL)
    resp = requests.get(SOURCE_DATA_URL)
    lines = resp.text.splitlines()
    headers = lines[0].split(',')

    print("Grouping data...")
    dategroups = defaultdict(list)
    c = csv.DictReader(lines)
    for dt, rows in groupby(c, key = foo_date):
        dategroups[dt].extend(list(rows))

    # write files
    for dt, rows in dategroups.items():
        fname = os.path.join(DOWNLOADED_DATA_DIR, dt + '.csv')
        print("Writing:", fname)
        with open(fname, "w") as f:
            c = csv.DictWriter(f, fieldnames = headers)
            c.writeheader()
            c.writerows(rows)
