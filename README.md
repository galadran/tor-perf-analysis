# tor-perf-analysis

Instructions: 

Grab the sqlite file from [Drive](https://drive.google.com/file/d/1vclM-SFJYcyOtb2YydVYFRUpMHGQ3zhj/view?usp=sharing).
(or download the raw datasets and use the import scripts). 

Place the sqlite file in data/. 
Create a image/ directory. 
Scripts should be fairly self explanatory. 

# output.sqlite 

Contains four tables:
  - consensus - exit node consensus data
  - output - latency data from Arthur's dataset
  - detailed_output - latency data combined with consensus data. 
  - torperf - Torperf latency data. 
