
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

def worker(qIn,qOut):
    db = sqlite3.connect("output.sqlite", isolation_level=None)
    db.execute("PRAGMA synchronous = OFF")
    db.execute("PRAGMA journal_mode = WAL")
    sql = db.cursor() 
    while True:
        try:
            (target,fingerprint,timestamp,latency,state) = qIn.get(False)
        except Empty as E:
            continue
        labels = getLabels(sql,fingerprint,timestamp)
        if labels is None:
            continue 
        (ts,fp,major,minor,rel,os,ctry,bdwth,exit_prob,as_name,version) = labels 
        qOut.put((timestamp,fp,major,minor,rel,os,ctry,bdwth,exit_prob,as_name,version,target,latency,state))
        #sql.execute("INSERT INTO detailed_output VALUES " \
        #    +str( (timestamp,fp,major,minor,rel,os,ctry,bdwth,exit_prob,as_name,version,target,latency,state)))
    #db.commit()

def writeFun(qOut):
    db = sqlite3.connect("output.sqlite", isolation_level=None)
    db.execute("PRAGMA synchronous = OFF")
    db.execute("PRAGMA journal_mode = WAL")
    sql = db.cursor() 
    while True:
        try:
            (timestamp,fp,major,minor,rel,os,ctry,bdwth,exit_prob,as_name,version,target,latency,state) = qOut.get(False)
        except Empty as E:
            continue
        sql.execute("INSERT INTO detailed_output VALUES " \
            +str( (timestamp,fp,major,minor,rel,os,ctry,bdwth,exit_prob,as_name,version,target,latency,state)))
    db.commit()

def watcher(qIn,qOut):
    from time import sleep
    #TODO use tqdm with manual updates
    old = qIn.qsize()
    t = tqdm(total=old,desc='Building new rows')
    while not qIn.empty():
        newOld = qIn.qsize()
        t.update(old-newOld)
        old = newOld
        sleep(1)
    t.close()
    old = qOut.qsize()
    t = tqdm(total=old,desc='Writing out new rows')
    while not qOut.empty():
        newOld = qOut.qsize()
        t.update(old-newOld)
        old = newOld
        sleep(1)
    t.close()

if __name__ == "__main__":
    printing("Warning - Currently this has to be forcibly terminated once finished") #TODO fix
    db = sqlite3.connect("output.sqlite", isolation_level=None)
    db.execute("PRAGMA synchronous = OFF")
    db.execute("PRAGMA journal_mode = WAL")
    sql = db.cursor() 
    sql.execute("SELECT * FROM output")
    outputs =  sql.fetchall()
    qIn = Queue()
    qOut = Queue()
    threads = []

    for o in tqdm(outputs):
        qIn.put(o)
    w = Process(target=watcher,args=(qIn,qOut))
    w.start()
    for i in range(0,8):
        p = Process(target=worker,args=(qIn,qOut))
        p.start()
        threads.append(p)
    writer = Process(target=writeFun,args=(qOut,))
    writer.start()
    for p in threads:
        p.join()
    writer.join()
    w.join()
    sql.commit()


