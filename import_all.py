from glob import glob 
import os
from tqdm import tqdm
from json import loads
import sqlite3
from datetime import datetime

##TODO 
#Destroy file if it exists
#Import all outputs 
#Import all consensus 
#Convert datetimes to linux epochs (what about ms?)
#Label outputs with consensus data

class Consensus:
    
    def __init__(self, ts,fp,v,b,e,c,a):
        self.timestamp = str(datetime.strptime(ts,"%Y%m%d_%H%M"))
        self.fingerprint = fp
        if v == "Unknown":
            self.version = "Unknown"
            self.os = "Unknown"
            self.major = "-1"
            self.minor = "-1"
            self.release = "Unknown"
        else:
            self.version = v.split(" on ")[0].replace("Tor ","")
            self.major = int(self.version.split(".")[1])
            self.minor = int(self.version.split(".")[2])
            self.release = self.version.split(".")[3]
            self.os = v.split(" on ")[1]
        self.bandwidth = int(b)
        self.exit_prob = float(e)
        self.country = c
        self.as_name = a
        
    def as_tuple(self):
        return (self.timestamp,self.fingerprint,self.major,self.minor,self.release,self.os,\
            self.bandwidth,self.exit_prob,self.country,self.as_name,self.version)

def process(sql,timestamp,contents):
    if "_relays" not in contents.keys():
        return
    relays = contents["_relays"]
    for r in relays:
        c = Consensus(timestamp,r["fingerprint"],r.get("platform","Unknown"),\
            r.get("bandwidth_rate",0),r.get("exit_probability",0),\
            r.get("country_name","Unknown"),r.get("as_name","Unknown"))
        sql.execute("INSERT INTO consensus VALUES " + str(c.as_tuple()))    


db = sqlite3.connect("output.sqlite")
sql = db.cursor() 

for p in tqdm(glob("exits-json-raw_historical/**/*.json",recursive=True)):
    if "results_latest" in p:
        continue
    f = open(p,'r')
    c = f.read()
    j = loads(c)
    ts = p.split("/")[-1].split("_")[-2] +"_"+ p.split("/")[-1].split("_")[-1].replace(".json","")
    process(sql,ts,j)

db.commit()
db.close()
    
