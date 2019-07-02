from scipy import signal
import matplotlib.pyplot as plt
from random import sample

import numpy as np
import pandas as pd
from glob import glob 

csvs = glob('*_weak_congestion.csv')

csvs = sample(csvs,1)
print(csvs)
t = pd.read_csv(csvs[0])

f, Pxx_den =signal.periodogram(t['congestion'])

plt.semilogy(f,Pxx_den)
plt.show()