#TODO - Histogram stacked by major version and OS
#One histogram for each major version and OS and one shared histogram? 

#TODO - Histogram stacked by weight
#One histogram for each weight quartile and one shared histogram? 

#%%
#grab candidates from sqlite file
#load in data for each relay 

from tqdm import tqdm


import sqlite3
db = sqlite3.connect("../data/output.sqlite")
sql = db.cursor() 

sql.execute("""
            SELECT fingerprint,Count(*) FROM detailed_output
            WHERE latency > 5 AND result == 'SUCCEEDED' GROUP BY fingerprint 
            """)
            #WHERE result == 'SUCCEEDED' AND latency > 5 GROUP BY fingerprint 
results = dict()
for (fp,ct) in tqdm(sql.fetchall(),desc='Loading raw results'):
    results[fp] = ct

#%%
#Example plotly call 
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
import plotly.io as pio

#init_notebook_mode(connected=True)         # initiate notebook for offline plot


h = go.Histogram(x=list(results.values()),xbins=dict(
        start=0.0,
        end=300.0))
layout = go.Layout()
fig = go.Figure(data=[h], layout=layout)
#iplot([h], filename='histogram')
pio.write_image(fig, '../images/dns_slow_requests_relays_histogram.png',scale=4)


#%%
candidates = [(k,v) for (k,v) in results.items() if v > 300]
#candidates = sorted(candidates,key=lambda x : int(x[1]),reverse=True)
candidates = candidates[0:20]

scatters = list()
for (k,v) in tqdm(candidates):
    print(k)
    print(v)
    #fetch full results 
    sql.execute("""
                SELECT timestamp,latency FROM detailed_output WHERE fingerprint == '""" + str(k) + """' AND result == 'SUCCEEDED'
                """)
    ts = list()
    lt = list()
    for (t,l) in sql.fetchall():
        ts.append(t)
        lt.append(l)
    if len(lt) < 3000:
        continue
    s = go.Scatter(x=ts,y=lt,mode='markers',name='latency')
    scatters.append(s)
    
    sql.execute("""
                SELECT timestamp,bandwidth,exit_prob FROM consensus WHERE fingerprint == '""" + str(k) + """'
                """)
    tsc = list()
    bdwth = list()
    exitProb = list()
    for (t,b,e) in sql.fetchall():
        tsc.append(t)
        bdwth.append(b)
        exitProb.append(e)
    
    b = go.Scatter(x=tsc,y=bdwth,mode='lines',name='Bandwidth',yaxis='y2')
    l = go.Layout(    title='Relay ID: '+str(k),
    yaxis=dict(
        title='Latency (s)',
        range=[0,10]
    ),
    yaxis2=dict(
        title='Exit Probability',
        titlefont=dict(
            color='rgb(148, 103, 189)'
        ),
        tickfont=dict(
            color='rgb(148, 103, 189)'
        ),
        overlaying='y',
        side='right'
    ))
    e = go.Scatter(x=tsc,y=exitProb,mode='lines',name='Exit Probability',yaxis='y2')
    #build scatter
    fig = go.Figure(data=[s,e],layout=l)
    pio.write_image(fig, '../images/TemporalAnalysis/random/'+str(k)+'.png',scale=4)


#%%
#from plotly import tools
#fig = tools.make_subplots(rows=len(scatters),cols=1)
#count = 1
#for s in scatters:
#    fig.append_trace(s,count,1)
#    count += 1

#iplot(fig,filename='scatters')

#%%
