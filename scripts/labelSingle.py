
#For each output
#Label with consensus data

# Fingerprint + timestamp, find right consensus, add extra values 

import sqlite3
from datetime import datetime,timedelta
from tqdm import tqdm
from multiprocessing import Process, Queue
from queue import Empty
def strToTime(time):
    if "." not in time:
        time = time + ".0"
    return datetime.strptime(time,"%Y-%m-%d %H:%M:%S.%f")

def getLabels(sql,target,time):
    #TODO Get the consensus row from the table
    #Shuld latest consensus not before time, ref target
    #Ensure within 24 hour window. 
    query = 'SELECT * FROM consensus WHERE fingerprint = "'+ target + '" AND datetime(timestamp) <= \
            datetime("'+time+'") ORDER BY timestamp DESC LIMIT 1'
    sql.execute(query)
    r = sql.fetchone()
    if r is None:
        return None
    (ts,fp,major,minor,rel,os,ctry,bdwth,exit_prob,as_name,version) = r
    assert(strToTime(ts) - strToTime(time) < timedelta(1))
    return (ts,fp,major,minor,rel,os,ctry,bdwth,exit_prob,as_name,version)

if __name__ == "__main__":
    db = sqlite3.connect("output.sqlite")#, isolation_level=None)
    #db.execute("PRAGMA synchronous = OFF")
    #db.execute("PRAGMA journal_mode = WAL")
    sql = db.cursor() 
    sql.execute("SELECT * FROM output")
    outputs =  sql.fetchall()
    for o in tqdm(outputs):
        (target,fingerprint,timestamp,latency,state) = o
        labels = getLabels(sql,fingerprint,timestamp)
        if labels is None:
            continue 
        (ts,fp,major,minor,rel,os,ctry,bdwth,exit_prob,as_name,version) = labels 
        sql.execute("INSERT INTO detailed_output VALUES " \
            +str( (timestamp,fp,major,minor,rel,os,ctry,bdwth,exit_prob,as_name,version,target,latency,state)))
        
