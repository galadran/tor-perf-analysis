

#%%
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

#%%

db = sqlite3.connect("output.sqlite")
sql = db.cursor() 

#fingerprint = '77B829E5628712BD3D639242B9A0B40DDCB6B871'

lower = "0.0"
higher = "10.0"

sql.execute("""
                SELECT timestamp,latency
                FROM output
                WHERE state == 'SUCCEEDED'
                AND latency > """+ lower + """
                AND latency < """ + higher + """
                """)

xD = list()
yD = list()
for (t,l) in tqdm(sql.fetchall()):
    if "." not in t:
        t = t + ".000"
    dt = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
    xD.append(mdates.date2num(dt)) 
    yD.append(float(l))

#%%
import matplotlib
#matplotlib.use('Cairo')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] = 24
plt.rcParams['axes.labelsize'] = 24
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titlesize'] = 24
plt.rcParams['xtick.major.size'] = 15
plt.rcParams['xtick.minor.size'] = 7.5
plt.rcParams['xtick.labelsize'] = 24
plt.rcParams['xtick.labelsize'] = 24
plt.rcParams['ytick.labelsize'] = 24
plt.rcParams['legend.fontsize'] = 24
plt.rcParams['figure.titlesize'] = 24
#plt.figure(figsize=(24,24))


years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')
month_fmt = mdates.DateFormatter('%B')
fig, ax = plt.subplots(1,1,figsize=(24,24),sharex=True)
ax.set_title('All successful measurements between ' + lower +  ' and ' +higher+ ' seconds')
ax.set_xlabel("Date (Years, Months)")
ax.set_ylabel("Latency, excluding circuit construction (seconds)")
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt,)
#ax.xaxis.set_minor_formatter(month_fmt)
ax.xaxis.set_minor_locator(months)

ax.set_xlim([min(xD),max(xD)])
ax.set_ylim([float(lower),float(higher)])

x = np.array(xD)
y = np.array(yD)

density_scatter(x,y,bins=1024,ax=ax,s=200,cmap=plt.get_cmap('magma',1024))
#plt.colorbar()
#plt.tight_layout()
plt.savefig('foo.png')
#plt.show()