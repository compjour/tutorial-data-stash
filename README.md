# tutorial-data-stash

The raw data and scripts to collect them, as used and mirrored for Stanford Computational Journalism data tutorials at http://tutorials.compjour.org.

Currently kind of hacked together, will eventually be a more formalized framework for fetching and packaging data in different formats and different stages of cleaning, so that they can be used as practice for both data gathering and analysis.

The [data-holding](data-holding/) directory contains the downloaded files and some of their compiled versions. Some of the bigger files have been split into smaller files so that they'd fit more gracefully into version control, but I haven't written the compilation scripts to re-assemble. The ultimate goal is to have scripts that produce downloadable links to easy-to-use CSVs and SQLite databases for class exercises (as soon as I finish learning SQLalchemy).

The [scripts](scripts/) directory contains the (mostly Python 3) scripts for fetching them. I've been writing them as I go, so each subfolder/project is a bit different depending on my mood at that moment and whether I've learned from mistakes in fetching the other datasets.

### Inventory so far

- [Congress legislator data](https://github.com/unitedstates/congress-legislators) from the unitedstates project. The compilation script creates 3 separate CSVs: [legislator information, term info, and social media accounts](data-holding/congress_legislators/compiled/).
- [Congress vote data for the 114th Congress via Govtrack.us rsync server](https://www.govtrack.us/developers/data). The compilation script converts Govtrack's JSON into two flat CSV files for easier import into SQL: [member-votes.csv and roll-call-votes.csv](data-holding/congress_votes/compiled/)
- Congress Twitter data - Using the social media account info from the [unitedstates project](https://github.com/unitedstates/congress-legislators) (which lists official accounts, not campaign accounts), I've collected the most recent tweets from each Congressmember, profile data, user_ids of who they follow, and profiles of the most followed users by congressmembers. However, most of the collecting code lives in my [Ruby datajanitor repo](https://github.com/datajanitor/diaries). I've simply moved the resulting data files to this _repo's_ [compiled directory](data-holding/twitter/congress/compiled/).
- [San Francisco Police Department incident data](https://data.sfgov.org/Public-Safety/SFPD-Incidents-from-1-January-2003/tmnf-yvry)
- Dallas Police Department datasets: [incidents](https://www.dallasopendata.com/Police/Dallas-Police-Public-Data-RMS-Incidents/tbnj-w5hb), [arrests](https://www.dallasopendata.com/Police/Dallas-Police-Public-Data-RMS-Arrest/r4wm-ig9m), and [charges](https://www.dallasopendata.com/Police/Dallas-Police-Public-Data-RMS-Arrest-Charge/uzgk-dxyv)
- Los Angeles Police Department incidents from [2013](https://data.lacity.org/A-Safe-City/LAPD-Crime-and-Collision-Raw-Data-for-2013/iatr-8mqm) and [2014](https://data.lacity.org/A-Safe-City/LAPD-Crime-and-Collision-Raw-Data-2014/eta5-h8qx)
- [Southern Nevada (e.g. Las Vegas) restaurant inspections database](http://www.southernnevadahealthdistrict.org/restaurants/inspect-downloads.php
)
- [New York restaurant inspections data](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j), which is a flat table containing all restaurants, inspections, violations, and violation codes.
- [San Francisco restaurant inspections](https://extxfer.sfdph.org/food/)
- [Social Security Administration baby names](http://www.ssa.gov/oact/babynames/limits.html), nationwide and per-state.
- The metadata for [The Museum of Modern Art collection](https://github.com/MuseumofModernArt/collection)
- U.S. House member and staff expenditures, [as collected and cleaned by the Sunlight Foundation](https://sunlightfoundation.com/tools/expenditures/)
- [UK Baby names](http://www.ons.gov.uk/ons/rel/vsob1/baby-names--england-and-wales/index.html)

Todo:

- [Iowa State Salaries](https://data.iowa.gov/Government/State-of-Iowa-Salary-Book/s3p7-wy6w)
- [Florida State Salaries](http://dmssalaries.herokuapp.com/salaries)
- Death row data from TX, FL, CA
- Stop and frisk, 2012,2013,2014
