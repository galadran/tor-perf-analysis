


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

def drawHistogram(source,results,filename):
    if len(results) < 1000:
        return
    binBoundaries = np.linspace(0,10,1000)
    fig, ax = plt.subplots(3,1,figsize=(36,24))

    ax[0].set_xlim(0,10)
    n, bins, patches = ax[0].hist(results, bins=binBoundaries, range=(0,10),cumulative=False,density=False)
    #ax[0].set_ylim(0,max(n)*1.1)
    
    ax[1].set_xlim(0,2)
    n, bins, patches = ax[1].hist(results, bins=binBoundaries, range=(0,2),cumulative=False,density=False)
    #ax[1].set_ylim(0,max(n)*1.1)

    ax[2].set_xlim(2,10)
    n, bins, patches = ax[2].hist(results, bins='auto', range=(2,10),cumulative=False,density=False)
    #ax[2].set_ylim(0,max(n)*1.1)
    
    ax[2].set_xlabel("Latency (seconds)")
    ax[2].set_ylabel("Number of Measurements")
    ax[0].set_title("All Requests " + source)
    ax[1].set_title("Fast Requests " + source)
    ax[2].set_title("Slow Requests " + source)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

dbpath = '../data/output.sqlite'
latencyLB = '0.0'
latencyUB = '10.0'

db = sqlite3.connect(dbpath)
sql = db.cursor()
sql.execute("""SELECT source,datarequest,dataresponse 
                    FROM torperf 
                    WHERE didtimeout == '0'
                    AND dataresponse-datarequest > """ + latencyLB + """
                    AND dataresponse-datarequest < """ + latencyUB )
results = dict()
earlyResults = dict()
lateResults = dict()
for (source,st,ft) in tqdm(sql.fetchall()):
        t = time.ctime(int(st.split('.')[0]))
        dt = datetime.datetime.strptime(t, "%a %b %d %H:%M:%S %Y")
        day = dt.date()
        latency = float(ft)-float(st)
        if source not in results.keys():
            earlyResults[source] = list()
            lateResults[source] = list()
            results[source] = list()
        if str(day) < '2014':
            earlyResults[source].append(latency)
        else:
            lateResults[source].append(latency)
        results[source].append(latency)


for s in results.keys():
    drawHistogram(s+'_early',earlyResults[s],'../images/torperf_latency_histograms/'+s+'_early.png')
    drawHistogram(s+'_late',lateResults[s],'../images/torperf_latency_histograms/'+s+'_late.png')
    #drawHistogram(s+'_all,results[s],'../images/torperf_latency_histograms/'+s+'_all.png')

