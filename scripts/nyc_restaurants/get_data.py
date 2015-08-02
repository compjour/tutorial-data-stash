"""
python -m scripts.nyc_restaurants.get_data

data comes from:
https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j

Original file is split into by-month/year (of inspection date) files for easier version control

"""
import requests
import csv
import os.path
from itertools import groupby
from collections import defaultdict
from scripts.nyc_restaurants.settings import DOWNLOADED_DATA_DIR, SOURCE_DATA_URL
from scripts.nyc_restaurants.settings import setup_space


def foo_date(row):
    """ return 2015-09 from INSPECTION DATE value of '09/25/2015' """
    mth, day, yr = row['INSPECTION DATE'].split('/')
    return "%s-%s" % (yr, mth)

if __name__ == '__main__':
    print("Downloading:", SOURCE_DATA_URL)
    resp = requests.get(SOURCE_DATA_URL)
    print("Grouping data...")
    lines = resp.text.splitlines()
    headers = lines[0].split(',')
    dategroups = defaultdict(list)
    for dt, rows in groupby(csv.DictReader(lines), key = foo_date):
        dategroups[dt].extend(list(rows))

    for dt, rows in dategroups.items():
        fname = os.path.join(DOWNLOADED_DATA_DIR, dt + '.csv')
        print("Writing:", fname)
        with open(fname, "w") as f:
            c = csv.DictWriter(f, fieldnames = headers)
            c.writeheader()
            c.writerows(rows)
