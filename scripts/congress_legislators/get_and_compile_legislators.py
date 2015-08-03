#!/bin/python3
# run as:
# python3 scripts/congress_legislators/get_and_compile_legislators.py
"""
Produces
- ./data-holding/congress_legislators/compiled/legislators.csv
- ./data-holding/congress_legislators/compiled/terms.csv
- ./data-holding/congress_legislators/compiled/social-media-accounts.csv

"""
import csv
import requests
from os import makedirs
from collections import OrderedDict
import os.path
import yaml
DATA_DIR = "./data-holding/congress_legislators"
DATA_DOWNLOADS_DIR = os.path.join(DATA_DIR, 'downloaded')
DATA_COMPILED_DIR = os.path.join(DATA_DIR, 'compiled')
CONGRESS_CURRENT_INFO_PATH = os.path.join(DATA_DOWNLOADS_DIR, 'unitedstates-congress_legislators-current.yaml')
CONGRESS_SOCMEDIA_INFO_PATH = os.path.join(DATA_DOWNLOADS_DIR, 'unitedstates-congress_legislators-social_media.yaml')
# compiled data
COMPILED_LEGISLATORS_PATH = os.path.join(DATA_COMPILED_DIR, 'legislators.csv')
COMPILED_TERMS_PATH = os.path.join(DATA_COMPILED_DIR, 'terms.csv')
COMPILED_SOCMEDIA_PATH = os.path.join(DATA_COMPILED_DIR, 'social-media-accounts.csv')
# Use my fork since it contains twitter ids
CONGRESS_CURRENT_INFO_URL = 'https://github.com/dannguyen/congress-legislators/raw/master/legislators-current.yaml'
CONGRESS_SOCMEDIA_INFO_URL = 'https://raw.githubusercontent.com/dannguyen/congress-legislators/master/legislators-social-media.yaml'

SOC_MEDIA_FIELDS = [s + '_' + x for s in ['twitter', 'facebook', 'youtube', 'instagram'] for x in ['id', 'username']]


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

def fetch_congress_social_media_info():
    """
    Retrieves latest data from unitedstates/congress-legislators (CONGRESS_SOCMEDIA_INFO_URL)
    saves a copy locally

    Returns: a list of the loaded YAML text
    """
    resp = requests.get(CONGRESS_SOCMEDIA_INFO_URL)
    txt = resp.text
    with open(CONGRESS_SOCMEDIA_INFO_PATH, "w") as o:
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
    h['senate_lis_id']  = obj['id'].get('lis')
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
    h['role']        = current_term.get('type')
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


def extract_member_social_media_info(obj):
    """
    `obj` is a social media dict from:
    - id:
        bioguide: E000295
        thomas: '02283'
        govtrack: 412667
    social:
        twitter: SenJoniErnst
        facebook: senjoniernst
        facebook_id: '351671691660938'
        youtube_id: UCLwrmtF_84FIcK3TyMs4MIw
        instagram: senjoniernst
        instagram_id: 1582702853

    Returns: a dict including bioguide_id as a foreign key
    """
    d = {'bioguide_id': obj['id']['bioguide']}
    s = obj['social']
    for n in ['twitter', 'facebook', 'youtube', 'instagram']:
        d[n + '_username'] = s.get(n)
        d[n + '_id'] = s.get(n + '_id')
    return d

def extract_all_social_media_info(data):
    """
    `data` is a list of legislator social media dicts, as processed from CONGRESS_SOCMEDIA_INFO_PATH

    Returns: a list of lists of socmedia accounts for each legislator
    """
    return [extract_member_social_media_info(d) for d in data]



if __name__ == '__main__':
    setup_space()
    # Fetch data
    print("Fetching data from:", CONGRESS_CURRENT_INFO_URL)
    leg_data = fetch_congress_current_info()
    print("Fetching data from:", CONGRESS_SOCMEDIA_INFO_URL)
    soc_data = fetch_congress_social_media_info()


    # Compile data
    print("Saving legislators data to:", COMPILED_LEGISLATORS_PATH)
    with open(COMPILED_LEGISLATORS_PATH, 'w') as f:
        legislators = extract_all_legislators(leg_data)
        c = csv.DictWriter(f, fieldnames = list(legislators[0].keys()))
        c.writeheader()
        c.writerows(legislators)

    print("Saving terms data to:", COMPILED_TERMS_PATH)
    with open(COMPILED_TERMS_PATH, 'w') as f:
        termslist = extract_all_terms(leg_data)
        c = csv.DictWriter(f, fieldnames = list(termslist[0][0].keys()))
        c.writeheader()
        for terms in termslist:
            c.writerows(terms)

    print("Saving social_media data to:", COMPILED_SOCMEDIA_PATH)
    with open(COMPILED_SOCMEDIA_PATH, 'w') as f:
        socaccounts = extract_all_social_media_info(soc_data)
        c = csv.DictWriter(f,
            fieldnames = ['bioguide_id'] + SOC_MEDIA_FIELDS)
        c.writeheader()
        c.writerows(socaccounts)
