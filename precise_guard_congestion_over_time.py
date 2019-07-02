import agate
from tqdm import tqdm
import csv 
import datetime
from statistics import median,mean,stdev
import numpy as np 
cNames = ['guard','target','exit','time','latency','state']
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
            ts = datetime.datetime.strptime(row['time'],tFormat)
        except:
            ts = datetime.datetime.strptime(row['time'],"%Y-%m-%d %H:%M:%S")
        if node not in results.keys():
            results[node] = list()
        results[node].append((row['guard'],ts,float(row['latency'])))
        
for node in tqdm(results.keys()):
    with open ('parsed_by_node/'+node+'_precise_latency.csv','w',newline='') as f: 
        writer = csv.writer(f)
        writer.writerow(['guard','timestamp','latency'])
        for guard, ts,l in results[node]:
            writer.writerow([guard,ts,l])
