from draw_scatter_dataset import draw_graph
from fetch_latencies import fetchTorPerf, fetchDNSData

def torPerfAnalysis(s,f,l,u,sources,img):
    xD, yD = fetchTorPerf(s,f,l,u,sources)
    draw_graph('TorPerf dataset',l,u,xD,yD,img)

def DNSAnalysis(s,f,l,u,img):
    (xD,yD) = fetchDNSData(s,f,l,u)
    draw_graph('DNS Dataset',l,u,xD,yD,img)

torPerfAnalysis("2010","2020",'0.0','10.0',[],'torperf_all.png')
torPerfAnalysis("2010","2020",'0.0','10.0',['torperf','moria','siv'],'torperf_big_three.png')
torPerfAnalysis("2014-06-01","2015-06-01",'0.0','10.0',[],'torperf_2015.png')
torPerfAnalysis("2010","2015-01-01",'0.0','10.0',[],'torperf_early.png')
torPerfAnalysis("2015","2020",'0.0','10.0',[],'torperf_late.png')
torPerfAnalysis("2017-01-01","2020",'0.0','10.0',[],'torperf_latest.png')
torPerfAnalysis("2010","2020",'0.0','2.0',[],'torperf_fast.png')
torPerfAnalysis("2010","2020",'2.0','10.0',[],'torperf_slow.png')

DNSAnalysis("2010","2020","0.0","10.0",'dns_all.png')
DNSAnalysis("2010","2020","0.0","2.0",'dns_fast.png')
DNSAnalysis("2010","2020","2.0","10.0",'dns_slow.png')
