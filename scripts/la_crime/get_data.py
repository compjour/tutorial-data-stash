"""
python -m scripts.la_crime.get_data

data comes from:
https://data.lacity.org/A-Safe-City/LAPD-Crime-and-Collision-Raw-Data-for-2013/iatr-8mqm
https://data.lacity.org/A-Safe-City/LAPD-Crime-and-Collision-Raw-Data-2014/eta5-h8qx

Original files are split into by-month/year (of reported incident date, 'Date Rptd')
    CSV files for easier version control
"""

import requests
import csv
import os.path
from itertools import groupby
from collections import defaultdict
from scripts.la_crime.settings import DOWNLOADED_DATA_DIR, SOURCE_DATA_URLS
from scripts.la_crime.settings import setup_space





def foo_datestr(datestr):
    """
    note: this key function operates on a string only
    `datestr` is a string like `09/25/2015`
    return string "2015-09"
    """
    mth, day, yr = datestr.split('/')
    return "%s-%s" % (yr, mth)


# Caveats:
# If the different datasets contain reported crimes outside of their year, this
# is going to cause some problems.
# This is mitigated by making sure both years have the same schema
#  and then accumulating all of the incidents into one collection before writing
#  the files
#
# (this is some really sloppy convoluted code, that abstracts for a non-existent 2+ year scenario)

if __name__ == '__main__':
    setup_space()
    coll = []
    for url in SOURCE_DATA_URLS:
        d = {'url': url}
        print("Downloading:", url)
        resp = requests.get(url)
        d['lines'] = resp.text.splitlines()
        d['headers'] = d['lines'][0].split(',')
        coll.append(d)

    print("Grouping data...")
    headers = coll[0]['headers']
    dategroups = defaultdict(list)
    for d in coll:
        # cheapo way to make sure schema is the same
        if sorted(d['headers']) == sorted(headers):
            c = csv.DictReader(d['lines'])
            for dt, rows in groupby(c, key = lambda row: foo_datestr(row['Date Rptd'])):
                dategroups[dt].extend(list(rows))
        else:
            print(str(sorted(d['headers'])), 'does not match', str(sorted(headers)))
            raise

    # write files
    for dt, rows in dategroups.items():
        fname = os.path.join(DOWNLOADED_DATA_DIR, dt + '.csv')
        print("Writing:", fname)
        with open(fname, "w") as f:
            c = csv.DictWriter(f, fieldnames = headers)
            c.writeheader()
            c.writerows(rows)
