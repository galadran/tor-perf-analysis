from draw_scatter_dataset import draw_graph
from fetch_latencies import fetchTorPerf, fetchDNSData

def torPerfAnalysis(s,f,l,u,sources,img):
    xD, yD = fetchTorPerf(s,f,l,u,sources)
    draw_graph('TorPerf dataset',l,u,xD,yD,img)

def DNSAnalysis(s,f,l,u,img):
    (xD,yD) = fetchDNSData(s,f,l,u)
    draw_graph('DNS Dataset',l,u,xD,yD,img)

