
#Glob files 
#Filter only for results containing circuit info 
#Parse out all relevant results into table 

# BUILDTIMES=0.193307876587,0.427851915359,0.932479858398 CIRC_ID=5956 
# CONNECT=1304465521.39 DATACOMPLETE=1304465531.85 DATAREQUEST=1304465521.92 
# DATARESPONSE=1304465522.44 DIDTIMEOUT=0 FILESIZE=1048576 LAUNCH=1304464374.77 
# NEGOTIATE=1304465521.39 
# PATH=$35BDC6486420EFD442C985D8D3C074988BFE544B,$073D54FE18CB605BB87EEB9F8C95EE551A92986C,$775DF6B8CF3FB0150A594F6E2B5CB1E0AC45D09B 
# QUANTILE=0.800000 READBYTES=1048825 REQUEST=1304465521.39 RESPONSE=1304465521.92 SOCKET=1304465521.39 
# SOURCE=moria START=1304465521.39 TIMEOUT=4594 USED_AT=1304465531.86 USED_BY=14958 WRITEBYTES=83


# Request data:
# SOURCE=moria
# WRITEBYTES=83
# FILESIZE=1048576
# READBYTES=1048825
# Circuit data: 
# BUILDTIMES=0.193307876587,0.427851915359,0.932479858398
# PATH=$35BDC6486420EFD442C985D8D3C074988BFE544B,$073D54FE18CB605BB87EEB9F8C95EE551A92986C,$775DF6B8CF3FB0150A594F6E2B5CB1E0AC45D09B 
# LAUNCH=1304464374.77 
# Timings
# START=1304465521.39 
# SOCKET=1304465521.39 
# CONNECT=1304465521.39 
# NEGOTIATE=1304465521.39 
# REQUEST=1304465521.39
# RESPONSE=1304465521.92 
# DATAREQUEST=1304465521.92 
# DATARESPONSE=1304465522.44
# DATACOMPLETE=1304465531.85 
# DIDTIMEOUT=0  
# QUANTILE=0.800000   

#How do we distinguish hidden service searches?
#Will version 1.1 and have more entries in path!
#parse strategy is split on ' ' then '=' then ','. Place into dictionary. 
# Extract relevant entries. 
#Dump into SQL

from glob import glob 
from tqdm import tqdm
import sqlite3


def convert(row):
    result = dict()
    keyvalues = row.split(' ')
    for kv in keyvalues:
        (k,v) = kv.split('=')
        if ',' in v:
            v = v.split(',')
        if k == 'PATH':
            if len(v) == 3:
                result['guard'] = v[0]
                result['middle'] = v[1]
                result['exit'] = v[2]
            elif len(v) == 2:
                result['guard'] = v[0]
                result['middle'] = 'NONE'
                result['exit'] = v[1]
            continue
        if k == 'BUILDTIMES':
            if len(v) == 3:
                result['guard_latency'] = v[0]
                result['middle_latency'] = v[1]
                result['exit_latency'] = v[2]
            elif len(v) == 2:
                result['guard_latency'] = v[0]
                result['middle_latency'] = 'NONE'
                result['exit_latency'] = v[1]
            continue
        result[k.lower()] = v
    if 'didtimeout' not in result.keys():
        result['didtimeout'] = '?'
    return result 

def getTuple(r):
    keys = [
        'SOURCE',
        'WRITEBYTES',
        'FILESIZE',
        'READBYTES',
        'guard',
        'middle',
        'exit',
        'guard_latency',
        'middle_latency',
        'exit_latency',
        'LAUNCH',
        'START',
        'SOCKET',
        'CONNECT',
        'NEGOTIATE',
        'REQUEST',
        'RESPONSE',
        'DATAREQUEST',
        'DATARESPONSE',
        'DATACOMPLETE',
        'DIDTIMEOUT'
    ]
    values = list()
    for k in keys: 
        v = r[k.lower()]
        v = v.replace('\n','')
        v = v.replace('$','')
        values.append(v)
    return tuple(values)

db = sqlite3.connect("output.sqlite")
sql = db.cursor() 

sql.execute('DROP TABLE IF EXISTS torperf')
sql.execute("""CREATE TABLE torperf
            ( 
        'source',
        'writebytes',
        'filesize',
        'readbytes',
        'guard',
        'middle',
        'exit',
        'guard_latency',
        'middle_latency',
        'exit_latency',
        'launch',
        'start',
        'socket',
        'connect',
        'negotiate',
        'request',
        'response',
        'datarequest',
        'dataresponse',
        'datacomplete',
        'didtimeout'
            )
            """)

dropped_guard = 0
dropped_middle = 0 
dropped_timeout = 0
added_records = 0
total_records = 0
for p in tqdm(glob("torperf/**/*.tpf",recursive=True)):
    f = open(p,'r')
    for row in f.readlines():
        if row == '':
            continue
        if '@' in row:
            continue
        result = convert(row)
        total_records += 1
        if 'guard' not in result.keys():
            dropped_guard += 1
            continue
        if result['middle'] == 'NONE':
            dropped_middle += 1
            continue
        if result['didtimeout'] == '?':
            dropped_timeout += 1
            continue
        added_records += 1 
        sql.execute('INSERT INTO torperf VALUES ' + str(getTuple(result)))
print("Total Records: "+ str(total_records))
print("Dropped due to missing circuit info: " + str(dropped_guard))
print("Dropped due to only 2-hop circuit: " + str(dropped_middle))
print("Dropped due to missing timeout info: " + str(dropped_timeout))
print("Added Records: "+str(added_records))
db.commit()
db.close()