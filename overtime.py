from tqdm import tqdm


import sqlite3
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
import datetime
from plotly import tools

db = sqlite3.connect("output.sqlite")
sql = db.cursor() 

#fingerprint = '77B829E5628712BD3D639242B9A0B40DDCB6B871'

sql.execute("""
                SELECT source,datarequest,dataresponse 
                FROM torperf 
                WHERE didtimeout == '0'
                AND dataresponse-datarequest > 2
                AND dataresponse-datarequest < 10
                """)

x = dict()
y = dict()
for (source,s,f) in tqdm(sql.fetchall()):
    import time 
    t = datetime.datetime.strptime(time.ctime(int(s.split('.')[0])), "%a %b %d %H:%M:%S %Y")
    m = s.split('.')[1]
    m = datetime.datetime.strptime(m,'%f')
    if source not in y.keys():
        y[source] = list()
    if source not in x.keys():
        x[source] = list()
    x[source].append(t) #Omitted milliseconds
    y[source].append(float(f)-float(s))

scatters = list()
for source in y.keys():
    scatters.append(go.Scatter(x=x[source],y=y[source],mode='markers',name=source))

fig = tools.make_subplots(rows=len(scatters), cols=1, shared_xaxes=True)
i = 1
for s in scatters:
    fig.append_trace(s,i,1)
    i += 1

plot(fig,filename='scatters')
    