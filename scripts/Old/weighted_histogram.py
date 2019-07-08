#TODO - Histogram stacked by weight
#One histogram for each weight quartile and one shared histogram? 

#%%
#grab candidates from sqlite file
#load in data for each relay 

from tqdm import tqdm

import sqlite3
db = sqlite3.connect("../data/output.sqlite")
sql = db.cursor() 

#Get weights of each relay
#Bin by quintile. 
#Swap out mk,os for quintile position. 

sql.execute("""
            SELECT fingerprint,exit_prob FROM consensus
            """)

results = dict()
for (fp,cn) in tqdm(sql.fetchall(),desc='Loading consensus data'):
    if fp not in results.keys():
        results[fp] = list()
    results[fp].append(float(cn))


from numpy import percentile 

all = list()

medians = dict()
for k in results.keys():
    m = percentile(results[k],50) 
    all.append(m)
    medians[k] = m

#%%
from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go

#init_notebook_mode(connected=True)         # initiate notebook for offline plot

h = go.Histogram(x=list(medians.values()))

layout = go.Layout()
fig = go.Figure(data=[h], layout=layout)

plot(fig, filename='histogram')

#%%

bin_ends = [20,40,60,80,100]
bins = percentile(all,bin_ends)

assignments = dict()
for k in medians.keys():
    for i in range(len(bins)):
        if medians[k] <= bins[i]:
            assignments[k] = bin_ends[i]
            break
#Assignments maps each fingerprint to a value between 20,100
#The node's bandwidth lies in the range x, x-20. I.e. 20 means
# the node's median bandwith is in the top 20% of all nodes. 
    
#TODO List Comprehensions. 

#%%

sql.execute("""
            SELECT fingerprint,latency FROM detailed_output
            WHERE result == 'SUCCEEDED'
            """)
results = dict()
for (fp,lt) in tqdm(sql.fetchall(),desc='Loading raw results'):
    if fp not in results.keys():
        results[fp] = list()
    results[fp].append(lt)

percentile99 = dict()
for fp in tqdm(results.keys(),desc='Calculating percentiles'):
    if len(results[fp]) < 1000:
        continue
    if fp not in percentile99.keys():
        percentile99[fp] = list()
    percentile99[fp] = percentile(results[fp],99)

series = dict()
for k in percentile99.keys():
    a = assignments[k]
    if a not in series.keys():
        series[a] = list()
    series[a].append(percentile99[k])

#%%
#Example plotly call 
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go

#init_notebook_mode(connected=True)         # initiate notebook for offline plot

h = list()
for (k,v) in series.items():
    h.append(go.Histogram(x=v,name=str(k)))

layout = go.Layout(barmode='stack')
fig = go.Figure(data=h, layout=layout)

plot(fig, filename='stacked histogram')

#%%
