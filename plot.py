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

dirpath = '/exports/csce/datastore/geos/users/s1326314/rbg_analysis'

#import AGB data
AGB_list = []
with open(dirpath + '/outputs/site1/AGB/AGB.csv', 'rb') as f:
    next(f)
    reader = csv.reader(f)
    for row in reader:
        AGB_list.append(row)


#import radar data for one year
radar_list = []
with open(dirpath + '/outputs/site1/radar/stats_07.csv', 'rb') as f:
    next(f)
    reader = csv.reader(f)
    for row in reader:
        radar_list.append(row)

AGB = [l[1] for l in AGB_list]
HV = [l[1] for l in radar_list]
print(HV)
print(AGB)

plt.plot(AGB, HV, 'ro')
plt.show()



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
