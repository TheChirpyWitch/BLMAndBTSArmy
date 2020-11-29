import numpy as np
import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import os


#_id,id,follower_list
df = pd.read_csv('follower_data.csv')
# 1st 100 uniq users & their followers
"""
uList=df['id'][:100]
fList=df['follower_list'][:100]
f = open("follower_edges_100.csv", 'w')
"""

# 2nd 100 uniq users & their followers
uList=df['id'][100:200]
fList=df['follower_list'][100:200]
f = open("follower_edges_100_2nd.csv", 'w')

f.write("source,target\n")
for source, target_list in zip(uList, fList):
    target_list = target_list.strip("[")
    target_list = target_list.strip("]")
    for target in target_list.split(','):
        f.write(f"{source},{target.strip()}\n")
f.close()
    
