


#%%

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

results = list()
with open('../data/output.csv',newline='') as f:
    reader = csv.DictReader(f,fieldnames=cNames)
    for row in tqdm(reader):
        name = row['exit']
        if row['state'] != 'SUCCEEDED':
            continue
        results.append(float(row['latency']))

#%%
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(36,24))
a  = plt.subplot(3,1,1)
plt.xlim(0,10)
n, bins, patches = plt.hist(results, bins=1000, range=(0,10),cumulative=False,density=False)
q = plt.subplot(3,1,2)
plt.xlim(0,2)
n, bins, patches = plt.hist(results, bins=400, range=(0,2),cumulative=False,density=False)
s = plt.subplot(3,1,3)
plt.xlabel("Latency (seconds)")
plt.ylabel("Number of Measurements")
plt.xlim(2,10)
n, bins, patches = plt.hist(results, bins=400, range=(2,10),cumulative=False,density=False)
a.set_title("All Requests")
q.set_title("Fast Requests")
s.set_title("Slow Requests")


plt.tight_layout()
plt.savefig('../images/dns_latency_histogram.png')


#%%
