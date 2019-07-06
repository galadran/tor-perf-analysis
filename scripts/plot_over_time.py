import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from random import sample

import numpy as np
import pandas as pd
from glob import glob 

csvs = glob('*_weak_congestion.csv')

csvs = sample(csvs,1)
print(csvs)
t = pd.read_csv(csvs[0])
p1 = lambda t: go.Scatter(x=t['date'],y=t['congestion'],mode='lines+markers',name='congestion')
p2 = lambda t: go.Scatter(x=t['date'],y=t['median'],mode='lines+markers',name='median')
p3 = lambda t: go.Scatter(x=t['date'],y=t['1st percentile'],mode='lines+markers',name='percentile')
lines = [p1(t), p2(t), p3(t)]

layout = go.Layout(title='congestion by node over time')
fig = go.Figure(data=lines,layout=layout)

plot(fig,filename='congestion_over_time.html')