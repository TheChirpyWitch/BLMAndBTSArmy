import numpy as np
import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import os

#Id,Label,timeset,modularity_class,componentnumber,strongcompnum,indegree,outdegree,
#Degree,weighted indegree,weighted outdegree,Weighted Degree,Eccentricity,
#closnesscentrality,harmonicclosnesscentrality,betweenesscentrality,clustering,
#eigencentrality,nodecolor-multimode,Authority,Hub
"""
# cat ../gephi_statsitics.csv | cut -d, -f8| sort -n | uniq -c > retweet_outdegree.txt
df = pd.read_csv('retweet_outdegree.csv')
x=df['outdegree']
y=df['count']
plt.scatter(x, y, alpha=0.6)
plt.yscale("log") 
plt.ylabel('Count', labelpad=1)
plt.xlabel('OutDegree', labelpad=1)
plt.title('OutDegree distribution from retweet network')
plt.show()
"""


# cat ../gephi_statsitics.csv | cut -d, -f9| sort -n | uniq -c > retweet_outdegree.txt
df = pd.read_csv('retweet_Degree.csv')
x=df['Degree']
y=df['count']
plt.scatter(x, y, alpha=0.6)
plt.yscale("log") 
plt.ylabel('Count', labelpad=1)
plt.xlabel('Degree', labelpad=1)
plt.title('Degree distribution from retweet network')
plt.show()
