import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from density_plot import density_scatter

def draw_graph(title,lower,higher,xD,yD,filename):

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
    ax.set_title(title)
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
    density_scatter(x,y,bins=1024,ax=ax,s=200,cmap=plt.get_cmap('viridis',1024))
    plt.tight_layout()

    ### Output
    plt.savefig(filename)