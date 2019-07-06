import agate
from tqdm import tqdm
import csv 
import datetime
from statistics import median,mean,stdev
import numpy as np 
cNames = ['target','exit','time','latency','state']
# tT = agate.Text()
# nT = agate.Number()
# cTypes = [tT,tT,agate.DateTime,nT,tT]

# table = agate.Table.from_csv('output.csv',cNames,cTypes)

tFormat = "%Y-%m-%d %H:%M:%S.%f"

results = dict()
with open('output.csv',newline='') as f:
    reader = csv.DictReader(f,fieldnames=cNames)
    for row in tqdm(reader):
        node = row['exit']
        if row['state'] != 'SUCCEEDED':
            continue
        try:
            day = datetime.datetime.strptime(row['time'],tFormat).date()
        except:
            day = datetime.datetime.strptime(row['time'],"%Y-%m-%d %H:%M:%S").date()
        if node not in results.keys():
            results[node] = dict()
        if day not in results[node].keys():
            results[node][day] = list()
        results[node][day].append(float(row['latency']))


def summarise(r,s):
    s = np.array(s)
    try:
        st = np.std(s)
    except:
        st = -1 
    return (r,s.size,np.percentile(s,1),np.median(s),np.percentile(s,99),np.mean(s),st)

toClear = list()
for node in tqdm(results.keys()):
    if len(results[node].keys()) < 356:
        toClear.append(node)

for n in toClear:
    results.pop(n)

for node in results.keys():
    with open (node+'.csv','w',newline='') as f: 
        writer = csv.writer(f)
        writer.writerow(['date','count','1st percentile','median','99th percentile','mean','stdev'])
        for r in tqdm(results[node].keys()):
            writer.writerow(summarise(r,results[node][r]))
