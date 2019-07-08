from draw_scatter_dataset import draw_graph
from fetch_latencies import fetchTorPerf, fetchDNSData, fetchDNSVersionData
from tqdm import tqdm
import sqlite3

def torPerfAnalysis(s,f,l,u,sources,img,prefix='../images/',m=False):
    xD, yD = fetchTorPerf(s,f,l,u,sources)
    draw_graph('TorPerf dataset',l,u,xD,yD,prefix+img,months=m)

def DNSAnalysis(s,f,l,u,img,prefix='../images/',m=False):
    (xD,yD) = fetchDNSData(s,f,l,u)
    draw_graph('DNS Dataset',l,u,xD,yD,prefix+img,months=m)

def DNSVersion(versions,img,prefix='../images/'):
    (xD,yD) = fetchDNSVersionData(versions)
    draw_graph('DNS Version Dataset','0.0','10.0',xD,yD,prefix+img)

def getVersions(db='../data/output.sqlite'):
    db = sqlite3.connect(db)
    sql = db.cursor() 
    sql.execute('SELECT os,major FROM detailed_output GROUP BY os,major')
    windows = list()
    bsd = list()
    for os,major in tqdm(sql.fetchall()):
        if 'windows' in os.lower() or  'cygwin' in os.lower():
            windows.append((str(major),os))
        if 'bsd' in os.lower() or 'dragonfly' in os.lower():
            bsd.append((str(major),os))
    return (windows,bsd)

print("Warning: After graphing finishes, there may be a long (silent) pause for rendering to png")
torPerfAnalysis("2010","2014-01-01",'0.0','10.0',[],'torperf_early.png',m=True)
DNSVersion([('2','Linux'),('3','Linux'),('4','Linux')],'dns_all_linux.png')

windows,bsd = getVersions()
DNSVersion(windows,'dns_Windows.png')
DNSVersion(bsd,'dns_BSD.png')
DNSVersion([('2','Linux')],'dns_2_linux.png')
DNSVersion([('3','Linux')],'dns_3_linux.png')
DNSVersion([('4','Linux')],'dns_4_linux.png')

torPerfAnalysis("2010","2020",'2.0','10.0',[],'torperf_slow.png')
torPerfAnalysis("2017-05-01","2020",'0.0','10.0',[],'torperf_latest.png',m=True)
torPerfAnalysis("2010","2020",'0.0','10.0',[],'torperf_all.png')
torPerfAnalysis("2010","2020",'0.0','10.0',['torperf','moria','siv'],'torperf_big_three.png')
torPerfAnalysis("2014-06-01","2015-06-01",'0.0','10.0',[],'torperf_2015.png',m=True)

torPerfAnalysis("2015","2020",'0.0','10.0',[],'torperf_late.png',m=True)
torPerfAnalysis("2010","2020",'0.0','2.0',[],'torperf_fast.png')

#Breakdown by version

DNSAnalysis("2010","2020","0.0","10.0",'dns_all.png',m=True)
DNSAnalysis("2010","2020","0.0","2.0",'dns_fast.png',m=True)
DNSAnalysis("2010","2020","2.0","10.0",'dns_slow.png',m=True)
