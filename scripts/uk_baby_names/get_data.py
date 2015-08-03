"""
python -m scripts.uk_baby_names.get_data

data comes from the UK's data search:
http://www.ons.gov.uk/ons/datasets-and-tables/index.html?pageSize=50&sortBy=none&sortDirection=none&newquery=baby+names

Info page is here:
http://www.ons.gov.uk/ons/rel/vsob1/baby-names--england-and-wales/index.html

"""

import os.path
import requests
from lxml import html
from urllib.parse import urljoin
from scripts.uk_baby_names.settings import DOWNLOADED_DATA_DIR, LANDING_PAGE_URL
from scripts.uk_baby_names.settings import setup_space




if __name__ == '__main__':
    setup_space()
    # Download the HTML
    print("Downloading landing page:", LANDING_PAGE_URL)
    # data URLs look like:
    # http://assets.sunlightfoundation.com.s3.amazonaws.com/expenditures/house/2014Q1-detail.csv
    doc = html.fromstring(requests.get(LANDING_PAGE_URL).text)
    hrefs = doc.xpath('//a[contains(@href, "baby-names")]/@href')
    for h in hrefs:
        url = urljoin(LANDING_PAGE_URL, h)
        print("Downloading:", url)
        x = requests.get(url)
        fname = os.path.join(DOWNLOADED_DATA_DIR, os.path.basename(url))
        with open(fname, 'wb') as f:
            f.write(x.content)
