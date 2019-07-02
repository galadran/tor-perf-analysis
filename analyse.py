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
        if row['state'] != 'SUCCEEDED':
            continue
        try:
            day = datetime.datetime.strptime(row['time'],tFormat).date()
        except:
            day = datetime.datetime.strptime(row['time'],"%Y-%m-%d %H:%M:%S").date()
        if day not in results.keys():
            results[day] = list()
        results[day].append(float(row['latency']))


def summarise(r,s):
    s = np.array(s)
    try:
        st = np.std(s)
    except:
        st = -1 
    return (r,s.size,np.percentile(s,1),np.median(s),np.percentile(s,99),np.mean(s),st)


with open ('daybyday.csv','w',newline='') as f: 
    writer = csv.writer(f)
    writer.writerow(['date','count','1st percentile','median','99th percentile','mean','stdev'])
    for r in tqdm(results.keys()):
        writer.writerow(summarise(r,results[r]))
