from draw_scatter_dataset import draw_graph
from fetch_latencies import fetchTorPerf, fetchDNSData

before = "2014-06-01"
after = "2015-06-01"
xD, yD = fetchTorPerf(before,after,'0.0','10.0',['torperf','moria','siv'])
draw_graph('Historical Analysis','0.0','10.0',xD,yD,'bar.png')

a = "5.0"
b = "7.0"
(xD,yD) = fetchDNSData("2020","2016",a,b)
title = 'DNS Data'
draw_graph(title,a,b,xD,yD,'foo.png')