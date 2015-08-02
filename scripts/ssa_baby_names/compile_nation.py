"""
run:
    $ python -m scripts.ssa_baby_names.compile_nation

creates:
    data-holding/ssa_baby_names/compiled/nation.csv
    (this is not included in the repo due to size)
"""
from scripts.ssa_baby_names.settings import DOWNLOADED_NATION_DIR, COMPILED_NATION_PATH
from glob import glob
import os.path
import re

if __name__ == '__main__':
    # open up the file to write to
    c = open(COMPILED_NATION_PATH, 'w')
    c.write("name,sex,count,year\n")
    # glob up the downloaded individual files
    filespath = os.path.join(DOWNLOADED_NATION_DIR, 'yob*.txt')
    for fname in glob(filespath):
        # get the year from the filename
        year = re.search("\d{4}", fname).group()
        print("Reading...", year)
        # open the file
        for line in open(fname, 'r').readlines():
            # add ",year" to each line
            row = line.strip() + ',' + year + "\n"
            c.write(row)
    # done
    c.close()
