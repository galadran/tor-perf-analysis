from draw_scatter_dataset import draw_graph
from fetch_latencies import fetchTorPerf, fetchDNSData

def torPerfAnalysis(s,f,l,u,sources,img,prefix='../images/',m=False):
    xD, yD = fetchTorPerf(s,f,l,u,sources)
    draw_graph('TorPerf dataset',l,u,xD,yD,prefix+img,months=m)

def DNSAnalysis(s,f,l,u,img,prefix='../images/',m=False):
    (xD,yD) = fetchDNSData(s,f,l,u)
    draw_graph('DNS Dataset',l,u,xD,yD,prefix+img,months=m)

print("Warning: After graphing finishes, there may be a long (silent) pause for rendering to png")

torPerfAnalysis("2010","2020",'2.0','10.0',[],'torperf_slow.png')
torPerfAnalysis("2017-05-01","2020",'0.0','10.0',[],'torperf_latest.png',m=True)
torPerfAnalysis("2010","2020",'0.0','10.0',[],'torperf_all.png')
torPerfAnalysis("2010","2020",'0.0','10.0',['torperf','moria','siv'],'torperf_big_three.png')
torPerfAnalysis("2014-06-01","2015-06-01",'0.0','10.0',[],'torperf_2015.png',m=True)
torPerfAnalysis("2010","2015-01-01",'0.0','10.0',[],'torperf_early.png',m=True)
torPerfAnalysis("2015","2020",'0.0','10.0',[],'torperf_late.png',m=True)
torPerfAnalysis("2010","2020",'0.0','2.0',[],'torperf_fast.png')


DNSAnalysis("2010","2020","0.0","10.0",'dns_all.png',m=True)
DNSAnalysis("2010","2020","0.0","2.0",'dns_fast.png',m=True)
DNSAnalysis("2010","2020","2.0","10.0",'dns_slow.png',m=True)
