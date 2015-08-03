"""
python -m scripts.house_expenditures.get_data

data comes cleaned from Sunlight Foundation:
https://sunlightfoundation.com/tools/expenditures/

Original file are split into YYYY-MM.csv (from `QUARTER` and `DATE`) and written
    into a subdirectory for reach file

    Creates a file for every year-month as well as YYYY- for entries that don't have a month
    in the date.

Note: This script is all-or-nothing... TODO: Make it less monolithic.
"""

import requests
import csv
from os import makedirs
from time import sleep
import os.path
import re # who needs HTML parsing?
from itertools import groupby
from collections import defaultdict
from scripts.house_expenditures.settings import DOWNLOADED_DATA_DIR, LANDING_PAGE_URL
from scripts.house_expenditures.settings import setup_space


def foo_key(row):
    """
    row is a dict that contains 'QUARTER' and 'DATE' field
    `DATE` is a string like `09-25`
    `QUARTER` is a string like `2010Q3`

    Returns: string "2010-09"
    """
    yr = row['QUARTER'][0:4]
    mth = row['DATE'][0:2]
    return "%s-%s" % (yr, mth)


if __name__ == '__main__':
    setup_space()
    # Download the HTML
    print("Downloading landing page:", LANDING_PAGE_URL)
    # data URLs look like:
    # http://assets.sunlightfoundation.com.s3.amazonaws.com/expenditures/house/2014Q1-detail.csv
    html = requests.get(LANDING_PAGE_URL).text
    urls = sorted(list(set(re.findall(r'http://assets.+?-detail\.csv', html))))
    print(len(urls), 'CSVs found')

    for url in urls:
        print("Downloading:", url)
        resp = requests.get(url)
        lines = resp.text.splitlines()
        headers = lines[0].split(',')

        print("Grouping data...")
        dategroups = defaultdict(list)
        c = csv.DictReader(lines)
        for dt, rows in groupby(c, key = foo_key):
            dategroups[dt].extend(list(rows))

        # write files
        for dt, rows in dategroups.items():
            slug = os.path.basename(url).split('-')[0] # e.g. 2014Q1
            subdir = os.path.join(DOWNLOADED_DATA_DIR, slug)
            makedirs(subdir, exist_ok = True)
            fname = os.path.join(subdir, dt + '.csv')
            print("Writing:", fname)
            with open(fname, "w") as f:
                c = csv.DictWriter(f, fieldnames = headers)
                c.writeheader()
                c.writerows(rows)
        print("Sleeping before next fetch...")
        sleep(10)
