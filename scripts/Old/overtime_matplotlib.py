from tqdm import tqdm


import sqlite3
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
import datetime
from plotly import tools
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from sklearn.neighbors import KernelDensity

db = sqlite3.connect("output.sqlite")
sql = db.cursor() 

#fingerprint = '77B829E5628712BD3D639242B9A0B40DDCB6B871'

sql.execute("""
                SELECT source,datarequest,dataresponse 
                FROM torperf 
                WHERE didtimeout == '0'
                AND dataresponse-datarequest > 0
                AND dataresponse-datarequest < 10
                """)

xD = dict()
yD = dict()
for (source,s,f) in tqdm(sql.fetchall()):
    import time 
    #t = datetime.datetime.strptime(time.ctime(int(s.split('.')[0])), "%a %b %d %H:%M:%S %Y")
    #m = s.split('.')[1]
    #m = datetime.datetime.strptime(m,'%f')
    if source not in yD.keys():
        yD[source] = list()
    if source not in xD.keys():
        xD[source] = list()
    xD[source].append(float(s)) 
    yD[source].append(float(f)-float(s))

#plt.figure(figsize=(24,24))
fig, ax = plt.subplots(len(xD.keys()),1,figsize=(24,24),sharex=True)
i = 0
for source in tqdm(yD.keys()):
    x = np.array(xD[source])
    y = np.array(yD[source])
    xy = np.vstack([x,y])
    
    kde = KernelDensity()
    #z = gaussian_kde(xy)(xy)
    kde.fit(list(zip(x,y)))
    z = kde.score_samples(xy)
    idx = z.argsort()
    x,y,z = x[idx], y[idx], z[idx]

    ax[i].scatter(x, y, c=z, s=1, edgecolor='')
    ax[i].set_title(source)
    i +=1

plt.tight_layout()
plt.show()