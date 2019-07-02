import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from random import sample

import numpy as np
import pandas as pd
from glob import glob 

csv = 'daybyday.csv'

table = pd.read_csv(csv)
p1 = lambda t: go.Scatter(x=t['date'],y=t['1st percentile'],mode='lines+markers',name='1st percentile')
p2 = lambda t: go.Scatter(x=t['date'],y=t['median'],mode='lines+markers',name='median')
p3 = lambda t: go.Scatter(x=t['date'],y=t['99th percentile'],mode='lines+markers',name='99th percentile')

lines = [p1(table),p2(table),p3(table)]

layout = go.Layout(title='Global Daily Latency over time')
fig = go.Figure(data=list(lines),layout=layout)

plot(fig,filename='day_by_day.html')