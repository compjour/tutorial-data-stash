#!/bin/python3
# python3 scripts/congress_votes/compile_votes.py
"""
Creates two CSVs from all the JSONs in the govtrack/2015 subfolder:
    - roll-call-votes.csv
    - member-votes.csv
"""
from glob import glob
from os import makedirs
import csv
import json
import os.path

DATA_DIR = "./data-holding/congress/votes/downloaded/govtrack/2015"
OUTPUT_DIR = './data-holding/congress/votes/compiled'
OUTPUT_ROLL_CALL_VOTES_PATH = os.path.join(OUTPUT_DIR, 'roll-call-votes.csv')
OUTPUT_MEMBER_VOTES_PATH = os.path.join(OUTPUT_DIR, 'member-votes.csv')


COMMON_VOTE_FIELDS = ['vote_id', 'category', 'chamber', 'date', 'congress',
    'number', 'type', 'result_text',   'result',
    'updated_at',  'session', 'requires', 'question', 'source_url']
OPTIONAL_FLAT_VOTE_FIELDS = ['subject', 'record_modified']
AMENDMENT_VOTE_FIELDS = ['amendment_author', 'amendment_purpose', 'amendment_number', 'amendment_type']
BILL_VOTE_FIELDS = ['bill_congress', 'bill_number', 'bill_title', 'bill_type']
NOM_VOTE_FIELDS = ['nomination_number', 'nomination_title']
ALL_VOTE_FIELDS = COMMON_VOTE_FIELDS + (OPTIONAL_FLAT_VOTE_FIELDS + AMENDMENT_VOTE_FIELDS +
    BILL_VOTE_FIELDS + NOM_VOTE_FIELDS)

def setup_space():
    makedirs(OUTPUT_DIR, exist_ok = True)

def extract_roll_call_vote(rcvote):
    """
    `rcvote` is a roll call vote dict

    Returns: a dict containing:
        - COMMON_VOTE_FIELDS
        and optionally:
            - subject (flat text field)
            - record_modified (flat text field in date format)
            - AMENDMENT_VOTE_FIELDS
            - BILL_VOTE_FIELDS
            - NOM_VOTE_FIELDS
    """
    d = {}
    # extract common fields
    for f in COMMON_VOTE_FIELDS:
        d[f] = rcvote[f]
    for f in OPTIONAL_FLAT_VOTE_FIELDS:
        d[f] = rcvote.get(f)
    if rcvote.get('amendment'):
        for f in AMENDMENT_VOTE_FIELDS:
            # only Senate amendments have purposes, and only House Amendments have authors
            if rcvote['chamber'] == 's' and f == 'amendment_author':
                pass
            elif rcvote['chamber'] == 'h' and f == 'amendment_purpose':
                pass
            else:
                d[f] = rcvote['amendment'][f.replace('amendment_', '')]
    if rcvote.get('bill'):
        for f in BILL_VOTE_FIELDS:
            # House bill objects don't have the title field
            if rcvote['chamber'] == 'h' and f == 'bill_title':
                pass
            else:
                d[f] = rcvote['bill'][f.replace('bill_', '')]
    if rcvote.get('nomination'):
        for f in NOM_VOTE_FIELDS:
            d[f] = rcvote['nomination'][f.replace('nomination_', '')]
    return d

def extract_member_votes(rcvote):
    """
    `rcvote` is a roll call vote dict

    Returns: a list of dicts, each dict containing:
        - vote_id
        - member_id (either a bioguide_id or a Senate lis_id)
        - vote: "Aye"/"Nay"/"Present"/"Not Voting"
    """
    vote_id = rcvote['vote_id']
    memvotes = []
    for vote_val, votes in rcvote['votes'].items():
        for v in votes:
            d = {'vote_id': vote_id, 'vote': vote_val, 'member_id': v['id']}
            memvotes.append(d)
    return memvotes

if __name__ == '__main__':
    setup_space()
    rc_csv = csv.DictWriter(open(OUTPUT_ROLL_CALL_VOTES_PATH, 'w'),
        fieldnames = ALL_VOTE_FIELDS)
    rc_csv.writeheader()
    mv_csv = csv.DictWriter(open(OUTPUT_MEMBER_VOTES_PATH, 'w'),
        fieldnames = ['vote_id', 'member_id', 'vote'])
    mv_csv.writeheader()

    jsonfiles = glob(os.path.join(DATA_DIR, '**/*.json'))
    for jname in jsonfiles:
        data = json.load(open(jname))
        rc_csv.writerow(extract_roll_call_vote(data))
        mv_csv.writerows(extract_member_votes(data))

