#%%
import numpy as np
import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats
from tqdm import tqdm
import matplotlib.pyplot as plt
import sqlite3
import datetime

#   Get latency by day
#   Bootstrap confidence values for 1/50/99
#   Plot

#%%
dbpath = '../data/output.sqlite'
latencyLB = '0.0'
latencyUB = '30.0'

db = sqlite3.connect(dbpath)
sql = db.cursor()
query = """SELECT datarequest,dataresponse 
                FROM torperf 
                WHERE didtimeout == '0'
                AND dataresponse-datarequest > """ + latencyLB + """
                AND dataresponse-datarequest < """ + latencyUB
                
sql.execute(query)

tFormat = "%Y-%m-%d %H:%M:%S.%f"

import time 
dayArrays = dict()
for (s,f) in tqdm(sql.fetchall(),desc='Processing entries'):
    t = time.ctime(int(s.split('.')[0]))
    dt = datetime.datetime.strptime(t, "%a %b %d %H:%M:%S %Y")
    day = dt.date()
    if day not in dayArrays.keys():
        dayArrays[day] = list()
    dayArrays[day].append(float(f)-float(s))

#%%
xvalues = list()
yvalues = list()
lowers = list()
uppers = list() 
for k in tqdm(dayArrays,desc='Bootstrapping each day'):
    vals = np.array(dayArrays[k])
    r = bs.bootstrap(vals, stat_func=bs_stats.median,num_threads=12)
    xvalues.append(k)
    yvalues.append(r.value)
    lowers.append(r.lower_bound)
    uppers.append(r.upper_bound)

errors = [lowers,uppers]
#%%

plt.figure()
plt.errorbar(xvalues, yvalues, yerr=errors,fmt='o')

plt.show()
