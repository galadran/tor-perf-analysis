#Take each relay and Calculate the 99th percentile
#Take the slowest 1/3 of relays
#Dump out their consensus information over time
# How many nodes changed version during our sample? 

import sqlite3
from collections import Counter 

def getMajorVersions(sql):
    sql.execute("SELECT distinct fingerprint,major from consensus where fingerprint in \
            (select fingerprint from consensus Group by fingerprint \
                Having count(distinct(major)) > 1) \
                order by fingerprint ASC")

    duplicate_relays = sql.fetchall()
    dupes = dict()
    for (f, major) in duplicate_relays:
        if f not in dupes.keys():
            dupes[f] = list()
        dupes[f].append(major)
    return dupes

def getTotalUpdates(dupes):
    totals = Counter()
    for v in dupes.values():
        totals.update([len(v)-1])
    return totals 

db = sqlite3.connect("output.sqlite")
sql = db.cursor() 

dupeVersions = getMajorVersions(sql)
totalUpdates = getTotalUpdates(dupeVersions)
for updates,frequency in totalUpdates.items():
    print(str(frequency) + " nodes updated major version "+str(updates)+" time(s)")

upgraders = set(dupeVersions.keys())
versions = set(dupeVersions.values())



#
# Get all 
#

# How many consensuses are they in? 
# Distribution of exit probs
# Distribution of bandwidth rates
# Distribution of versions (go by majority of time?)
# Distribution of locations
# Distribution of os's 