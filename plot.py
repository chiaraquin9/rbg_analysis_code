#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 14:54:48 2018

@author: s1326314
"""

#plotting HV vs AGB

import csv
import glob
import matplotlib.pyplot as plt
import numpy as np

dirpath = '/exports/csce/datastore/geos/users/s1326314/rbg_analysis'

#import AGB data
AGB_data = []
with open(dirpath + '/outputs/site1/AGB/AGB.csv', 'rb') as f:
    next(f)
    reader = csv.reader(f)
    for row in reader:
        AGB_data.append(row)


#import radar data for one year
radar_data = []
with open(dirpath + '/outputs/site1/radar/stats_17.csv', 'rb') as f:
    next(f)
    reader = csv.reader(f)
    for row in reader:
        radar_data.append(row)

#match AGB and radar data for the same plots
matches = [[i[0],i[1],j[1],j[2],j[3],j[4],j[5],j[6]] for i in AGB_data for j in radar_data if i[0] == j[0]]
matches.sort(key=lambda x: float(x[0]))

#get values for AGB, HV, dHV, HH, dHH,HH/HV, dHH/HV
plot = [float(i) for i in [x[0] for x in matches]]
AGB = [float(i) for i in [x[1] for x in matches]]
HV = [float(i) for i in [x[2] for x in matches]]
dHV = [float(i) for i in [x[3] for x in matches]]
HH = [float(i) for i in [x[4] for x in matches]]
dHH = [float(i) for i in [x[5] for x in matches]]
HH_HV = [float(i) for i in [x[6] for x in matches]]
dHH_HV = [float(i) for i in [x[7] for x in matches]]


col = ['r' if i > 11 else 'g' for i in plot]
leg = ['logged'if i > 11 else 'unlogged' for i in plot]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(AGB,HV,marker='^',label=leg,color=col)
ax.scatter(AGB,HH,marker='^',label=leg,color=col)
#ax.errorbar(AGB,HH,yerr= dHV,fmt='^',color=['r' if i > 11 else 'g' for i in AGB],ls='none')

#x.errorbar(AGB,HH,yerr= dHH,fmt='o',label=leg,color=col)
plt.ylim([-14, -5])
plt.xlabel('AGB [Mg]')
plt.ylabel('sigma_0 [db]')
plt.title('ALOS/PALSAR Backscatter vs AGB per plot for year 2017')
#plt.legend(loc='best')
plt.show()

fig.savefig(dirpath + "/outputs/site1/radar/sigma0_AGB_17.pdf", bbox_inches='tight')

















##import radar data for each year
#radar = []
#
#files = glob.glob(dirpath + '/outputs/site1/radar/*.csv')
#for fle in files:
#   # open the file and then call .read() to get the text
#   with open(fle) as f, open("{}.csv".format(fle.rsplit(".", 1)[1]),"w") as out:
#       next(f)
#       reader = csv.reader(f)
#       for row in reader:
#           radar.append(row)
#print(radar) 
