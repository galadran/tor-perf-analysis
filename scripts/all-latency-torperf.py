


#%%

from tqdm import tqdm
import csv 
import datetime
from statistics import median,mean,stdev
import numpy as np 
import sqlite3
import time
import numpy as np
import matplotlib.pyplot as plt

def drawHistogram(results,filename,binCount):
    plt.figure(figsize=(36,24))
    a  = plt.subplot(3,1,1)
    plt.xlim(0,10)
    n, bins, patches = plt.hist(results, bins=binCount, range=(0,10),cumulative=False,density=False)
    q = plt.subplot(3,1,2)
    plt.xlim(0,2)
    n, bins, patches = plt.hist(results, bins=binCount, range=(0,2),cumulative=False,density=False)
    s = plt.subplot(3,1,3)
    plt.xlabel("Latency (seconds)")
    plt.ylabel("Number of Measurements")
    plt.xlim(2,10)
    n, bins, patches = plt.hist(results, bins=binCount, range=(2,10),cumulative=False,density=False)
    a.set_title("All Requests")
    q.set_title("Fast Requests")
    s.set_title("Slow Requests")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

dbpath = '../data/output.sqlite'
latencyLB = '0.0'
latencyUB = '10.0'

db = sqlite3.connect(dbpath)
sql = db.cursor()
sql.execute("""SELECT datarequest,dataresponse 
                    FROM torperf 
                    WHERE didtimeout == '0'
                    AND dataresponse-datarequest > """ + latencyLB + """
                    AND dataresponse-datarequest < """ + latencyUB )
results = list()
earlyResults = list()
lateResults = list()
for (st,ft) in tqdm(sql.fetchall()):
        t = time.ctime(int(st.split('.')[0]))
        dt = datetime.datetime.strptime(t, "%a %b %d %H:%M:%S %Y")
        day = dt.date()
        latency = float(ft)-float(st)
        if str(day) < '2014':
            earlyResults.append(latency)
        else:
            lateResults.append(latency)
        results.append(latency)

drawHistogram(earlyResults,'../images/torperf_latency_histogram_early.png',100)
drawHistogram(lateResults,'../images/torperf_latency_histogram_late.png',100)
drawHistogram(results,'../images/torperf_latency_histogram_all.png',100)
drawHistogram(earlyResults,'../images/torperf_latency_granular_histogram_early.png',1000)
drawHistogram(lateResults,'../images/torperf_latency_granular_histogram_late.png',1000)
drawHistogram(results,'../images/torperf_latency_granular_histogram_all.png',1000)
