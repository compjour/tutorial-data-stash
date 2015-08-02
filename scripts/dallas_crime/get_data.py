"""
python -m scripts.dallas_crime.get_data

data comes from Socrata:
http://www.dallaspolice.net/publicdata/

creates:
    - dallas_crime/downloaded/arrests.csv
    - dallas_crime/downloaded/charges.csv
    - dallas_crime/downloaded/incidents/[split files]

The incidents file is split into by-month/year (of reported incident date, 'EDate')
    CSV files for easier version control

Note that EDate does not equal Date1. TODO: Research this
"""

import requests
import csv
import os.path
from itertools import groupby
from collections import defaultdict
from scripts.dallas_crime.settings import DOWNLOADED_DATA_DIR, DOWNLOADED_INCIDENTS_DIR
from scripts.dallas_crime.settings import SOURCE_DATA_URLS
from scripts.dallas_crime.settings import setup_space


def foo_date(row):
    """
    row is a dict that contains 'EDate' field
    `EDate` is a string like `09/25/2015 12:00:00 AM`

    Returns: string "2015-09"
    """
    dstr = row['EDate'] # this field may be empty...
    mth, day, yr = dstr.split(' ')[0].split('/')
    return "%s-%s" % (yr, mth)


if __name__ == '__main__':
    setup_space()
    for datatype, url in SOURCE_DATA_URLS.items():
        print("Downloading", datatype, ':', url)
        resp = requests.get(url)
        txt = resp.text
        if datatype == 'incidents':
            # facet by date, save into separate files
            lines = txt.splitlines()
            headers = lines[0].split(',')
            print("Grouping data...")
            dategroups = defaultdict(list)
            c = csv.DictReader(lines)
            for dt, rows in groupby(c, key = foo_date):
                dategroups[dt].extend(list(rows))
            # write files
            for dt, rows in dategroups.items():
                fname = os.path.join(DOWNLOADED_INCIDENTS_DIR, dt + '.csv')
                print("Writing:", fname)
                with open(fname, "w") as f:
                    c = csv.DictWriter(f, fieldnames = headers)
                    c.writeheader()
                    c.writerows(rows)

        else: # for non incident data, just save the raw text
            fname = os.path.join(DOWNLOADED_DATA_DIR, datatype + '.csv')
            print("Writing:", fname)
            with open(fname, "w") as f:
                f.write(txt)
