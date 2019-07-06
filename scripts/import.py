from json import loads 
from glob import glob 
import os
import code
from tqdm import tqdm
import csv

#Given JSON Files, create a CSV of results

def interact():
    code.InteractiveConsole(locals=globals()).interact()

class Result:
    
    def __init__(self, target,exit,state,time,latency):
        self.target = target
        self.exit = exit 
        self.state = state
        self.time = time 
        self.latency = latency    

def process(name, contents):
    results = []

    for target in contents.keys():
        if target == "_relays":
            continue
        for exit in contents[target].keys():
            for (state,time,latency) in contents[target][exit]:
                results.append(Result(target,exit,state,time,latency))
    return results
#Glob files 
print(os.getcwd())
results = []
for p in tqdm(glob("exits-json-raw/**/*.json",recursive=True)):
    f = open(p,'r')
    c = f.read()
    j = loads(c)
    results.extend(process(f,j))

f = open("output.csv",'w',newline='')
w = csv.writer(f,dialect='excel')
tuplise = lambda x : (x.target,x.exit,x.time,x.latency,x.state)
rows = map(tuplise,results)
for r in tqdm(rows):
    w.writerow(r)
