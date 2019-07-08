#For each day in consensus 
#Fetch counts of major version + os 
#Graph over time. 
import sqlite3
from tqdm import tqdm
from collections import Counter

dbpath = '../data/output.sqlite'

db = sqlite3.connect(dbpath)
sql = db.cursor() 
sql.execute("""
    SELECT timestamp,fingerprint,major,os FROM consensus 
            """)

def getVersionStr(m,os):
    chk = os.lower()
    if "windows" in chk or 'cygwin' in chk:
        return (m,'Windows')
    elif 'bsd' in chk or 'dragonfly' in chk:
        return (m,'BSD')
    else:
        return (m,os)

dates = dict()
versions = set()
relays = dict()
for (t,fp,m,os) in tqdm(sql.fetchall(),desc='Fetching records'):
    day = t 
    v = getVersionStr(m,os)
    versions.add(v)
    if day not in dates.keys():
        dates[day] = Counter()
        relays[day] = set()
    relays[day].add(fp)
    dates[day].update([v])

xvalues = sorted(list(dates.keys()))
yvalues = dict()
yvalues['Other'] = [0] * len(xvalues)
yvalues['totalCount'] = list()
for day in xvalues:
    yvalues['totalCount'].append(len(relays[day]))

for v in versions:
    yvalues[v] = list()
    for day in xvalues: 
        score = float(dates[day][v]) / float(len(relays[day])) 
        score = score * 100
        yvalues[v].append(score)
    if max(yvalues[v]) < 1:
        yvalues['Other'] = list(map(lambda x,y:x+y,yvalues['Other'],yvalues[v]))
        yvalues.pop(v)


import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def getColour(v):
    if v == 'Other':
        return dict(
            color='rgb(0,0,0)',
        )
    m, os = v
    m = int(m)
    if m < 0: 
        m = 1
    colour = (0,0,0)
    if os == 'Windows':
        colour = (60,0,0)
    elif os == 'BSD':
        colour = (0,60,0)
    elif os == 'Darwin':
        colour = (50,0,50)
    elif os == 'Linux':
        colour = (0,0,60)
    else:
        colour = (0,50,50)
    r,g,b = colour
    colour = (r*m,g*m,b*m)
    return dict(
            color='rgb'+str(colour),
        )
traces = list() 
series = sorted(yvalues.keys(),key=lambda x : (x[1],x[0]))
for k in series:
    if k == 'totalCount':
        continue
    traces.append(go.Scatter(
    x=xvalues,
    y=yvalues[k],
    stackgroup='one',
    name=str(k),
    line = getColour(k)
))

#Total Couunt not needed atm
traces.append(go.Scatter(x=xvalues,y=yvalues['totalCount'],name='TotalCount',yaxis='y2'))

layout = go.Layout(    
    title='Version Change in Exit Nodes Over Time (Unweighted)',
    showlegend=True,
    yaxis=dict(
        title='Percentage Share of Exit Nodes',
        range=[0,100]
    ),
    yaxis2=dict(
        title='Total Exit Nodes',
        titlefont=dict(
            color='rgb(148, 103, 189)'
        ),
        tickfont=dict(
            color='rgb(148, 103, 189)'
        ),
        overlaying='y',
        side='right'
    ))

fig = dict(data=traces, layout=layout)
plot(fig, filename='stacked-area-plot-norm')