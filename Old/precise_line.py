import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from random import sample

import numpy as np
import pandas as pd
from glob import glob 

csvs = glob('exits-json-raw/**/*_precise_latency.csv',recursive=True)

csvs = sample(csvs,2)
print(csvs)
tables = map(pd.read_csv,csvs)

p1 = lambda t: go.Scatter(x=t['timestamp'],y=t['latency'],mode='markers')

lines = map(p1, tables)

layout = go.Layout(title='Latency over time')
fig = go.Figure(data=list(lines),layout=layout)

plot(fig,filename='precise_latency.html')