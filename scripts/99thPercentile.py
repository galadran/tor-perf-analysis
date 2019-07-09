#%%
import numpy as np
import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats
from tqdm import tqdm
import sqlite3
import datetime

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.io as pio

#   Get latency by day
#   Bootstrap confidence values for 1/50/99
#   Plot

#%%
dbpath = '../data/output.sqlite'
latencyLB = '0.0'
latencyUB = '30.0'
db = sqlite3.connect(dbpath)
sql = db.cursor()

def drawMedianGraph(source):
    query = """SELECT datarequest,dataresponse 
                    FROM torperf 
                    WHERE didtimeout == '0'
                    AND dataresponse-datarequest > """ + latencyLB + """
                    AND dataresponse-datarequest < """ + latencyUB + """
                    AND source = '""" + source + """'"""

    sql.execute(query)

    tFormat = "%Y-%m-%d %H:%M:%S.%f" 

    import time 
    dayArrays = dict()
    for (s,f) in tqdm(sql.fetchall(),desc='Processing entries'):
        t = time.ctime(int(s.split('.')[0]))
        dt = datetime.datetime.strptime(t, "%a %b %d %H:%M:%S %Y")
        day = dt.date()
        #day = datetime.datetime(dt.year,dt.month,1)
        if day not in dayArrays.keys():
            dayArrays[day] = list()
        dayArrays[day].append(float(f)-float(s))

    #%%
    xvalues = list()
    yvalues = list()
    lowers = list()
    uppers = list() 
    dates = sorted(dayArrays.keys())

    for k in tqdm(dates,desc='Bootstrapping each day'):
        vals = np.array(dayArrays[k])
        #r = bs.bootstrap(vals, stat_func=percentile,num_threads=12)
        #r = bs.bootstrap(vals, stat_func=bs_stats.median,num_threads=12)
        xvalues.append(k)
        yvalues.append(np.percentile(vals,99))

    trace = go.Scatter(
        name=source,
        x=xvalues,
        y=yvalues,
        mode='lines')
        #line=dict(color='rgb(31, 119, 180)'),
        #fillcolor='rgba(255, 0, 0, 0.3)',
        #fill='tonexty')

    return [trace]


layout = go.Layout(
        yaxis=dict(title='Latency(s)'),
        title='TorPerf - Median Monthly Latency',
        showlegend = True)
data = list()
sql.execute("SELECT DISTINCT source FROM torperf")
for (s,) in sql.fetchall():
    if 'op' not in s:
        continue
    data.extend(drawMedianGraph(s))
fig = go.Figure(data=data, layout=layout)
pio.write_image(fig, '../images/torperf_median_monthly_source_ci.png',scale=4)
