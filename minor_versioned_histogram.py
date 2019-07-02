#TODO - Histogram stacked by major version and OS
#One histogram for each major version and OS and one shared histogram? 

#TODO - Histogram stacked by weight
#One histogram for each weight quartile and one shared histogram? 

#%%
#grab candidates from sqlite file
#load in data for each relay 

from tqdm import tqdm

import sqlite3
db = sqlite3.connect("output.sqlite")
sql = db.cursor() 

sql.execute("""
            SELECT fingerprint,major,minor,os,latency FROM detailed_output
            WHERE result == 'SUCCEEDED'
            """)
results = dict()
for (fp,mj,mn,os,lt) in tqdm(sql.fetchall(),desc='Loading raw results'):
    if (fp,mj,mn,os) not in results.keys():
        results[(fp,mj,mn,os)] = list()
    results[(fp,mj,mn,os)].append(lt)


#TODO List Comprehensions. 
from numpy import percentile 
percentile99 = dict()
for (fp,mj,mn,os) in tqdm(results.keys(),desc='Calculating percentiles'):
    if len(results[(fp,mj,mn,os)]) < 1000:
        continue
    if (mj,mn,os) not in percentile99.keys():
        percentile99[(mj,mn,os)] = list()
    percentile99[(mj,mn,os)].append(percentile(results[(fp,mj,mn,os)],99))

majorVersionPercentiles = dict()
for (mj,mn,os) in percentile99.keys():
    if len(percentile99[(mj,mn,os)]) < 5:
        continue
    majorVersionPercentiles[(mj,mn,os)] = percentile99[(mj,mn,os)]

totalRelays = 0
for v in majorVersionPercentiles.values():
    totalRelays += len(v)

print("Loaded percentile data for " + \
    str(totalRelays) + \
    " relays across " + str(len(majorVersionPercentiles.keys())) + " minor versions")
#%%
#Example plotly call 
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go

init_notebook_mode(connected=True)         # initiate notebook for offline plot

h = list()
for (k,v) in majorVersionPercentiles.items():
    h.append(go.Histogram(x=v,name=str(k)))

layout = go.Layout(barmode='stack')
fig = go.Figure(data=h, layout=layout)

iplot(fig, filename='stacked histogram')

#%%
