import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from random import sample

import numpy as np
import pandas as pd
from glob import glob 


csvs = glob('parsed_by_node/*_precise_latency.csv')
csvs = sample(csvs, 1)

tables = map(pd.read_csv,csvs)

lines = []
for t in tables:
    for g in set(t['guard']):
        x = t.query('guard=='+'"'+str(g)+'"')
        p1 = lambda t: go.Scatter(x=x['timestamp'],y=x['latency'],mode='lines+markers',name=g)
        lines.append(p1(x))

layout = go.Layout(title='Latency over time')
fig = go.Figure(data=list(lines),layout=layout)

plot(fig,filename='precise_latency.html')



