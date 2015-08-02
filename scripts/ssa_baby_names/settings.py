import os

DATA_DIR = "./data-holding/ssa_baby_names/"
DOWNLOADED_DATA_DIR = os.path.join(DATA_DIR, "downloaded")
COMPILED_DATA_DIR = os.path.join(DATA_DIR, "compiled")

DOWNLOADED_NATION_DIR = os.path.join(DOWNLOADED_DATA_DIR, 'nation')
DOWNLOADED_STATES_DIR = os.path.join(DOWNLOADED_DATA_DIR, 'states')

COMPILED_NATION_PATH = os.path.join(COMPILED_DATA_DIR, 'nation.csv')
COMPILED_STATES_PATH = os.path.join(COMPILED_DATA_DIR, 'states.csv')

def setup_space():
    os.makedirs(DOWNLOADED_NATION_DIR, exist_ok = True)
    os.makedirs(DOWNLOADED_STATES_DIR, exist_ok = True)
    os.makedirs(COMPILED_DATA_DIR, exist_ok = True)
