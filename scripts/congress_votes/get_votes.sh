# Pull roll call vote data via govtrack.us rsync server
# https://www.govtrack.us/developers/data
# run this from root of project, e.g.
# bash scripts/congress_votes/get_votes.sh
wkdir=./data-holding/congress/votes/downloaded/govtrack
mkdir -p $wkdir
rsync -avz --delete --delete-excluded --exclude **/text-versions/ \
    govtrack.us::govtrackdata/congress/114/votes/ $wkdir
