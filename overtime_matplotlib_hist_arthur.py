from tqdm import tqdm
import sqlite3
import datetime
from draw_scatter_dataset import draw_graph
import matplotlib.dates as mdates

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

title = 'All successful measurements between ' + lower +  ' and ' +higher+ ' seconds'
draw_graph(title,lower,higher,xD,yD,'foo.png')