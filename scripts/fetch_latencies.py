from tqdm import tqdm
import sqlite3
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time 

def fetchDNSVersionData(versions,db='../data/output.sqlite'):
    db = sqlite3.connect(db)
    sql = db.cursor() 
    where = "WHERE (result = 'SUCCEEDED') AND ("
    for (major,os) in versions:
        if where != "WHERE (result = 'SUCCEEDED') AND (":
            where += ' OR '
        where = where + " ( major = '" + major 
        where = where + "' AND os = '" + os + "')"
    where += ')'
    print(where)    
    sql.execute("""
                SELECT timestamp,latency
                FROM detailed_output """
                + where 
                )
    xD = list()
    yD = list()
    for (t,l) in tqdm(sql.fetchall(),desc='Fetching DNS Data'):
        if "." not in t:
            t = t + ".000"
        dt = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
        #if str(dt )< before or str(dt) > after:
        #   continue
        xD.append(mdates.date2num(dt)) 
        yD.append(float(l))
    return (xD,yD)  

def fetchDNSData(startTimepoint,finishTimepoint,latencyLB,latencyUB,db='../data/output.sqlite'):
    where = """
                WHERE state == 'SUCCEEDED'
                AND latency > """+ latencyLB + """
                AND latency < """ + latencyUB + """
                """
    return fetchSQLDNSData(where,startTimepoint,finishTimepoint,db)

def fetchSQLDNSData(where,before,after,db):
    db = sqlite3.connect(db)
    sql = db.cursor() 
    sql.execute("""
                SELECT timestamp,latency
                FROM output """
                + where 
                )
    xD = list()
    yD = list()
    for (t,l) in tqdm(sql.fetchall(),desc='Fetching DNS Data'):
        if "." not in t:
            t = t + ".000"
        dt = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
        if str(dt )< before or str(dt) > after:
            continue
        xD.append(mdates.date2num(dt)) 
        yD.append(float(l))
    return (xD,yD)

def fetchTorPerf(startTimepoint,finishTimepoint,latencyLB,latencyUB,sources,db='../data/output.sqlite'):
    where = """
                WHERE didtimeout == '0'
                AND dataresponse-datarequest > """ + latencyLB + """
                AND dataresponse-datarequest < """ + latencyUB + " "
    sQuery = ' AND ('
    for s in sources:
        if sQuery == ' AND (':
            sQuery += """ source = '""" + s + "'"
        else:
            sQuery += """ OR source = '""" + s + "' "
    sQuery += ')'
    if sQuery == ' AND ()':
        sQuery = ""
    where = where + sQuery
    return fetchSQLTorPerf(where,startTimepoint,finishTimepoint,db)

def fetchSQLTorPerf(where,before,after,db):
    db = sqlite3.connect(db)
    sql = db.cursor()
    query = """SELECT source,datarequest,dataresponse 
                    FROM torperf 
                    """ 
    sql.execute(query + where )
    
    xD = dict()
    yD = dict()
    for (source,s,f) in tqdm(sql.fetchall(),desc='Fetching torperf data'):
        if source not in yD.keys():
            yD[source] = list()
        if source not in xD.keys():
            xD[source] = list()

        t = time.ctime(int(s.split('.')[0]))
        dt = datetime.datetime.strptime(t, "%a %b %d %H:%M:%S %Y")
        if str(dt )< before or str(dt) > after:
            continue
        
        xD[source].append(mdates.date2num(dt)) 
        yD[source].append(float(f)-float(s))
    
    return (xD,yD)