"""
The Museum of Modern Art Collection Metadata
This data is provided by MoMA for research purposes only.
via https://github.com/MuseumofModernArt/collection
Digital Object Identifier:
[![DOI](https://zenodo.org/badge/15218/MuseumofModernArt/collection.svg)](https://zenodo.org/badge/latestdoi/15218/MuseumofModernArt/collection)
"""

SOURCE_DATA_URL = 'https://github.com/MuseumofModernArt/collection/blob/master/Artworks.csv?raw=true'

import os

DATA_DIR = "./data-holding/moma/"
DOWNLOADED_DATA_DIR = os.path.join(DATA_DIR, "downloaded/artworks")
COMPILED_DATA_DIR = os.path.join(DATA_DIR, "compiled")


def setup_space():
    os.makedirs(DOWNLOADED_DATA_DIR, exist_ok = True)
    os.makedirs(COMPILED_DATA_DIR, exist_ok = True)
