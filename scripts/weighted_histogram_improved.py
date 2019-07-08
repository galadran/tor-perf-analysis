#TODO - Histogram stacked by weight
#One histogram for each weight quartile and one shared histogram? 

#%%
#grab candidates from sqlite file
#load in data for each relay 

from tqdm import tqdm

import sqlite3
db = sqlite3.connect("../data/output.sqlite")
sql = db.cursor() 

#Get weights of each relay
#Bin by quintile. 
#Swap out mk,os for quintile position. 

sql.execute("""
            SELECT exit_prob,latency FROM detailed_output
            WHERE result == 'SUCCEEDED' AND latency < 10
            """)

results = dict()
#Parse fingerprint and exit node weights from consensus data
for (ep,ln) in tqdm(sql.fetchall(),desc='Loading consensus data'):
    ep = float(ep)
    if ep not in results.keys():
        results[ep] = list()
    results[ep].append(float(ln))

import numpy as np
exit_probs = list(results.keys())
lower = np.percentile(exit_probs,25)
middle =  np.percentile(exit_probs,50)
upper =  np.percentile(exit_probs,75)

series = {
    '1st Quartile' : list(),
    '2nd Quartile' : list(),
    '3rd Quartile' : list(),
    '4th Quartile' : list()
}
for (ep,lt) in tqdm(results.items(),desc='Processing Quartiles'):
    if ep < lower:
        series['1st Quartile'].extend(lt)
    elif ep < middle: 
        series['2nd Quartile'].extend(lt)
    elif ep < upper:
        series['3rd Quartile'].extend(lt)
    else:
        series['4th Quartile'].extend(lt)


from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.io as pio
#init_notebook_mode(connected=True)         # initiate notebook for offline plot

data = list()
labels = list()
for (k,v) in series.items():
    #.append(go.Histogram(x=np.array(v),name=str(k),opacity=0))
    data.append(v)
    labels.append(k)
fig = ff.create_distplot(data, labels,show_hist=False,show_rug=False)


#layout = go.Layout(barmode='overlay')
pio.write_image(fig, '../images/dns_weighted_histogram.png',scale=4)#,width=4096, height=3012, scale=4)
