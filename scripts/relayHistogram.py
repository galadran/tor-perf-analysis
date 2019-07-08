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
with open('../data/output.csv',newline='') as f:
    reader = csv.DictReader(f,fieldnames=cNames)
    for row in tqdm(reader):
        name = row['exit']
        if row['state'] != 'SUCCEEDED':
            continue
        if name not in results.keys():
            results[name] = list()
        results[name].append(float(row['latency']))

def summarise(r,s):
    s = np.array(s)
    try:
        st = np.std(s)
    except:
        st = -1 
    return (r,s.size,np.percentile(s,1),np.median(s),np.percentile(s,99),np.mean(s),st)

firstList = list()
medianList = list()
lastList = list()
for k,v in tqdm(results.items()):
        (_,_,f,m,l,_,_) = summarise(k,v)
        firstList.append(f)
        medianList.append(m)
        lastList.append(l)

import matplotlib.pyplot as plt

plt.figure(figsize=(36,24))
a  = plt.subplot(3,1,1)
plt.xlim(0,10)
n, bins, patches = plt.hist(firstList, bins=250, range=(0,10),cumulative=False,density=False)
q = plt.subplot(3,1,2)
plt.xlim(0,10)
n, bins, patches = plt.hist(medianList, bins=250, range=(0,10),cumulative=False,density=False)
s = plt.subplot(3,1,3)
plt.xlabel("Latency (seconds)")
plt.ylabel("Number of Relays")
plt.xlim(0,10)
n, bins, patches = plt.hist(lastList, bins=250, range=(0,10),cumulative=False,density=False)
a.set_title("1st Percentile")
q.set_title("50th Percentile")
s.set_title("99th Percentile")

plt.tight_layout()
plt.savefig('../images/dns_relay_histogram.png')
