#!/bin/python3
# run as:
# python3 scripts/congress_legislators/get_legislators.py
import csv
import requests
from os import makedirs
from collections import OrderedDict
import os.path
import yaml
DATA_DIR = "./datahaus/congress/legislators"
DATA_DOWNLOADS_DIR = os.path.join(DATA_DIR, 'downloaded')
DATA_COMPILED_DIR = os.path.join(DATA_DIR, 'compiled')
CONGRESS_CURRENT_INFO_PATH = os.path.join(DATA_DOWNLOADS_DIR, 'unitedstates-congress_legislators-current.yaml')
# compiled data
COMPILED_LEGISLATORS_PATH = os.path.join(DATA_COMPILED_DIR, 'congress-legislators.csv')
COMPILED_TERMS_PATH = os.path.join(DATA_COMPILED_DIR, 'congress-terms.csv')

CONGRESS_CURRENT_INFO_URL = 'https://github.com/unitedstates/congress-legislators/raw/master/legislators-current.yaml'


def setup_space():
    """
    Creates working directories
    """
    makedirs(DATA_DOWNLOADS_DIR, exist_ok = True)
    makedirs(DATA_COMPILED_DIR, exist_ok = True)


def fetch_congress_current_info():
    """
    Retrieves latest data from unitedstates/congress-legislators (CONGRESS_CURRENT_INFO_URL)
    saves a copy locally

    Returns: a list of the loaded YAML text
    """
    resp = requests.get(CONGRESS_CURRENT_INFO_URL)
    txt = resp.text
    with open(CONGRESS_CURRENT_INFO_PATH, "w") as o:
        o.write(txt)
    return yaml.load(txt)


def extract_all_legislators(data):
    """
    `data` is a list of legislator dicts, as processed from CONGRESS_CURRENT_INFO_PATH

    Returns: a list of legislator dicts, with filtered/flattened select fields
    """
    return [extract_legislator(d) for d in data]


def extract_legislator(obj):
    """
    `obj` is a legislator dict

    Returns: a new dict, with filtered/flattened select fields
    """
    h = OrderedDict()
    h['bioguide_id']    = obj['id']['bioguide']
    h['first_name']     = obj['name'].get('first')
    h['middle_name']    = obj['name'].get('middle')
    h['last_name']      = obj['name'].get('last')
    h['suffix_name']    = obj['name'].get('suffix')
    h['nickname']       = obj['name'].get('nickname')
    h['gender']         = obj['bio'].get('gender')
    h['birthday']       = obj['bio'].get('birthday')
    h['thomas_id']      = obj['id'].get('thomas')
    h['govtrack_id']    = obj['id'].get('govtrack')
    h['opensecrets_id'] = obj['id'].get('opensecrets')

    # add simplified term information
    current_term = max(obj['terms'], key = lambda t: t['start'])
    h['party']               = current_term.get('party')
    h['current_role']        = current_term.get('type')
    h['state']               = current_term.get('state')
    h['district']            = current_term.get('district')
    h['senate_class']        = current_term.get('class')
    h['state_rank']          = current_term.get('state_rank')
    h['current_term_start']  = current_term.get('start')
    h['current_term_end']    = current_term.get('end')
    h['url']                 = current_term.get('url')
    h['address']             = current_term.get('address')
    h['phone']               = current_term.get('phone')
    h['fax']                 = current_term.get('fax')
    h['contact_form']        = current_term.get('contact_form')
    h['rss_url']             = current_term.get('rss_url')
    return h


def extract_all_terms(data):
    """
    `data` is a list of legislator dicts, as processed from CONGRESS_CURRENT_INFO_PATH

    Returns: a list of lists of terms for each legislator
    """
    return [extract_terms(d) for d in data]

def extract_terms(obj):
    """
    `obj` is a legislator dict

    Returns: a list of term dicts, each with a bioguide_id to serve as foreign key
    """
    b_id = obj['id']['bioguide']
    termslist = []
    for term in obj['terms']:
        t = OrderedDict({'bioguide_id': b_id})
        t['role']           = term['type']
        t['start']          = term['start']
        t['end']            = term.get('end')
        t['party']          = term['party']
        t['district']       = term.get('district')
        t['senator_class']  = term.get('class')
        t['state']          = term['state']
        t['state_rank']     = term.get('state_rank')
        termslist.append(t)
    return termslist


if __name__ == '__main__':
    setup_space()
    print("Fetching data from:", CONGRESS_CURRENT_INFO_URL)
    l_data = fetch_congress_current_info()
    print("Saving legislators data to:", COMPILED_LEGISLATORS_PATH)
    with open(COMPILED_LEGISLATORS_PATH, 'w') as f:
        legislators = extract_all_legislators(l_data)
        c = csv.DictWriter(f, fieldnames = list(legislators[0].keys()))
        c.writeheader()
        c.writerows(legislators)

    print("Saving terms data to:", COMPILED_TERMS_PATH)
    with open(COMPILED_TERMS_PATH, 'w') as f:
        termslist = extract_all_terms(l_data)
        c = csv.DictWriter(f, fieldnames = list(termslist[0][0].keys()))
        c.writeheader()
        for terms in termslist:
            c.writerows(terms)
