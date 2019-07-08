#%%
import numpy as np
import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats
from tqdm import tqdm
import sqlite3
import datetime

#   Get latency by day
#   Bootstrap confidence values for 1/50/99
#   Plot

#%%
dbpath = '../data/output.sqlite'
latencyLB = '0.0'
latencyUB = '30.0'

db = sqlite3.connect(dbpath)
sql = db.cursor()
query = """SELECT datarequest,dataresponse 
                FROM torperf 
                WHERE didtimeout == '0'
                AND dataresponse-datarequest > """ + latencyLB + """
                AND dataresponse-datarequest < """ + latencyUB #+ """ LIMIT 10000 """ 
sql.execute(query)

tFormat = "%Y-%m-%d %H:%M:%S.%f" 

import time 
dayArrays = dict()
for (s,f) in tqdm(sql.fetchall(),desc='Processing entries'):
    t = time.ctime(int(s.split('.')[0]))
    dt = datetime.datetime.strptime(t, "%a %b %d %H:%M:%S %Y")
    day = dt.date()
    if day not in dayArrays.keys():
        dayArrays[day] = list()
    dayArrays[day].append(float(f)-float(s))

#%%
xvalues = list()
yvalues = list()
lowers = list()
uppers = list() 
dates = sorted(dayArrays.keys())

def percentile(val):
    return [np.percentile(val,50)]

for k in tqdm(dates,desc='Bootstrapping each day'):
    vals = np.array(dayArrays[k])
    #r = bs.bootstrap(vals, stat_func=percentile,num_threads=12)
    r = bs.bootstrap(vals, stat_func=bs_stats.std,num_threads=12)
    xvalues.append(k)
    yvalues.append(r.value)
    lowers.append(r.lower_bound)
    uppers.append(r.upper_bound)

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


upper_bound = go.Scatter(
    name='Upper Bound',
    x=xvalues,
    y=uppers,
    mode='lines',
    marker=dict(color="#444"),
    line=dict(width=0),
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty')

trace = go.Scatter(
    name='Measurement',
    x=xvalues,
    y=yvalues,
    mode='lines',
    line=dict(color='rgb(31, 119, 180)'),
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty')

lower_bound = go.Scatter(
    name='Lower Bound',
    x=xvalues,
    y=lowers,
    marker=dict(color="#444"),
    line=dict(width=0),
    mode='lines')

data = [lower_bound, trace, upper_bound]

layout = go.Layout(
    yaxis=dict(title='Latency(s)'),
    title='TorPerf Estimate of Median over time',
    showlegend = False)

fig = go.Figure(    data=data, layout=layout)
plot(fig, filename='pandas-continuous-error-bars.html')#,image='jpeg')#,imageheight=2160,image_width=4096)