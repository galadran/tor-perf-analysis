import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from random import sample

import numpy as np
import pandas as pd
from glob import glob 

csvs = glob('*_precise_latency.csv')

csvs= ['460F2EB956C09933A7E495C800786F11FD6D6336_precise_latency.csv', '5D3A57F494FD0782762C508A6695F4FCFF161FA4_precise_latency.csv']
#csvs = sample(csvs,2)
print(csvs)
tables = map(pd.read_csv,csvs)

results = []
# Find minimum value (over all time)
for t in tables:
    m = min(t['latency'])
    f = lambda x : x - m
    data = list(map(f,t['latency']))
    results.append(data)
# Plot histogram
plotter = lambda data : go.Histogram(x=data,xbins=dict(end=2,size=0.02),histnorm='probability',cumulative=dict(enabled=True))
h = list(map(plotter, results))

layout = go.Layout(barmode='overlay')
fig = go.Figure(data=h, layout=layout)

plot(fig,filename='distribution.html')
