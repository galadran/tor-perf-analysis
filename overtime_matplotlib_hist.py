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
from scipy.interpolate import interpn
import matplotlib.dates as mdates

#https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density-in-matplotlib
def density_scatter( x , y, ax = None, sort = True, bins = 20, **kwargs )   :
    """
    Scatter plot colored by 2d histogram
    """
    if ax is None :
        fig , ax = plt.subplots()
    data , x_e, y_e = np.histogram2d( x, y, bins = bins)
    z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([x,y]).T , method = "splinef2d", bounds_error = False )

    # Sort the points by density, so that the densest points are plotted last
    if sort :
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

    ax.scatter( x, y, c=z, **kwargs )
    return ax


db = sqlite3.connect("output.sqlite")
sql = db.cursor() 

#fingerprint = '77B829E5628712BD3D639242B9A0B40DDCB6B871'

sql.execute("""
                SELECT source,datarequest,dataresponse 
                FROM torperf 
                WHERE didtimeout == '0'
                AND dataresponse-datarequest > 0
                AND dataresponse-datarequest < 10
                AND (source ='torperf' OR source = 'moria' or source='siv')
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
    #Linux Time to datetime
    #datetime to 
    t = time.ctime(int(s.split('.')[0]))
    dt = datetime.datetime.strptime(t, "%a %b %d %H:%M:%S %Y")
    if str(dt )< "2014-06-01" or str(dt) > "2015-06-01":
        continue
    xD[source].append(mdates.date2num(dt)) 
    yD[source].append(float(f)-float(s))

#plt.figure(figsize=(24,24))
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')

fig, ax = plt.subplots(len(xD.keys()),1,figsize=(24,24),sharex=True)
ax[0].xaxis.set_major_locator(years)
ax[0].xaxis.set_major_formatter(years_fmt)
ax[0].xaxis.set_minor_locator(months)

i = 0
for source in tqdm(yD.keys()):
    x = np.array(xD[source])
    y = np.array(yD[source])
    density_scatter(x,y,bins=256,ax=ax[i],cmap=plt.get_cmap('hot'))
    #ax[i].hist2d(x, y, (50,50),cmap=plt.cm.jet)
    ax[i].set_title(source)
    i +=1



#plt.colorbar()
plt.tight_layout()
plt.savefig('foo.png')
#plt.show()