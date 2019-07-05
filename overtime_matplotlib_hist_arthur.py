

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
from density_plot import density_scatter

lower = "0.0"
higher = "10.0"

### Fetch results 
db = sqlite3.connect("output.sqlite")
sql = db.cursor() 
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

### General style options
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

### Setup graph
fig, ax = plt.subplots(1,1,figsize=(24,24),sharex=True)
ax.set_title('All successful measurements between ' + lower +  ' and ' +higher+ ' seconds')
ax.set_xlabel("Date (Years, Months)")
ax.set_ylabel("Latency, excluding circuit construction (seconds)")

### Setup axes 
years = mdates.YearLocator()   
months = mdates.MonthLocator()  

years_fmt = mdates.DateFormatter('%Y')
month_fmt = mdates.DateFormatter('%B')

ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt,)
ax.xaxis.set_minor_locator(months)
#ax.xaxis.set_minor_formatter(month_fmt)

ax.set_xlim([min(xD),max(xD)])
ax.set_ylim([float(lower),float(higher)])

if len(xD) > 10000000:
    print("WARNING: Graph may take 20+ minutes to draw and save")
elif len(xD) > 1000000:
    print("WARNING: Graph will take up to 20 minutes to draw and save")

### Draw Graph
x = np.array(xD)
y = np.array(yD)
density_scatter(x,y,bins=1024,ax=ax,s=200,cmap=plt.get_cmap('magma',1024))
plt.tight_layout()

### Output
plt.savefig('foo.png')