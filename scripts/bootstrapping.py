#%%
import numpy as np
import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats
from tqdm import tqdm
import matplotlib.pyplot as plt
import sqlite3
import datetime

#   Get latency by day
#   Bootstrap confidence values for 1/50/99
#   Plot

#%%
dbpath = '../data/output.sqlite'

db = sqlite3.connect(dbpath)
sql = db.cursor() 
sql.execute("""
    SELECT timestamp,latency FROM output WHERE state = 'SUCCEEDED'
            """)

tFormat = "%Y-%m-%d %H:%M:%S.%f"


dayArrays = dict()
for (t,l) in tqdm(sql.fetchall(),desc='Processing entries'):
    try:
        day = datetime.datetime.strptime(t,tFormat).date()
    except:
        day = datetime.datetime.strptime(t,"%Y-%m-%d %H:%M:%S").date()
    if day not in dayArrays.keys():
        dayArrays[day] = list()
    dayArrays[day].append(float(l))

#%%
xvalues = list()
yvalues = list()
lowers = list()
uppers = list()
dates = sorted(dayArrays.keys()) 

for k in tqdm(dates,desc='Bootstrapping each day'):
    vals = np.array(dayArrays[k])
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