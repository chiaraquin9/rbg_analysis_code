#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 14:54:48 2018

@author: s1326314
"""

#plotting HV vs AGB

import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import os, os.path

dirpath = '/exports/csce/datastore/geos/users/s1326314/rbg_analysis'
#dirpath = 'R:/rbg_analysis'

#plotting parameters
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
plt.rcParams.update(params)


#import AGB data
AGB_data = []
with open(dirpath + '/outputs/site1/AGB/AGB.csv', 'r') as f:
    next(f)
    reader = csv.reader(f)
    for row in reader:
        AGB_data.append(row)


#import radar data for all years
radar_data=[]
year = ['07','08','09','10','15','16','17','96']
for yr in year:
    with open(dirpath + '/outputs/site1/radar/ALOS_PALSAR/stats_'+ yr +'.csv', 'r') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            s = row.insert(0,yr) #append year
            radar_data.append(row)
            

#match AGB and radar data for the same plots
matches = [[j[0],i[0],i[1],j[2],j[3],j[4],j[5],j[6],j[7]] for i in AGB_data for j in radar_data if i[0] == j[1]]
matches.sort(key=lambda x: float(x[0]))

#get values for AGB, HV, dHV, HH, dHH,HH/HV, dHH/HV depending from year of choice

y = '07' #set year of choice

plot_no = [float(i[1]) for i in matches if i[0] == y]
AGB = [float(i[2]) for i in matches if i[0] == y]
HV = [float(i[3]) for i in matches if i[0] == y]
dHV = [float(i[4]) for i in matches if i[0] == y]
HH = [float(i[5]) for i in matches if i[0] == y]
dHH = [float(i[6]) for i in matches if i[0] == y]
HV_HH = [float(i[7]) for i in matches if i[0] == y]
dHV_HH = [float(i[8]) for i in matches if i[0] == y]


# select red for logged and green for unlogged plots
colors = ['red' if i > 11 else 'green' for i in plot_no]
lines = [Line2D([0], [0], marker='o', color='r', lw=3, label='Logged Plots'),
                   Line2D([0], [0], marker='o', color='g', lw=3, label='Unlogged Plots')]

fig = plt.figure(1, figsize=(9,9))

ax1 = fig.add_subplot(2,2,1)
for pos,y,err,color in zip(AGB,HV,dHV,colors):
    ax1.errorbar(pos,y,err,lw=2,capsize=5,fmt='o',capthick=2,color=color)
    plt.title('HV vs AGB')
    plt.xlabel('AGB [Mg/ha]')
    plt.ylabel('HV [db]')
    plt.ylim(-16,-9)
    
ax2 = fig.add_subplot(2,2,2)
for pos,y,err,color in zip(AGB,HH,dHH,colors):
    ax2.errorbar(pos,y,err,lw=2,capsize=5,fmt='o',capthick=2,color=color)
    plt.title('HH vs AGB')
    plt.xlabel('AGB [Mg/ha]')
    plt.ylabel('HH [db]')
    plt.ylim(-11,-3)
    
ax3 = fig.add_subplot(2,1,2)
for pos,y,err,color in zip(AGB,HV_HH,dHV_HH,colors):
    ax3.errorbar(pos,y,err,lw=2,capsize=5,fmt='o',capthick=2,color=color)
    plt.title('HV/HH vs AGB')
    plt.xlabel('AGB [Mg/ha]')
    plt.ylabel('HV/HH')
    plt.ylim(0,1)
    

plt.figlegend(handles=lines,loc='lower left')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.suptitle('ALOS/PALSAR Backscatter vs AGB per plot for year 2007',fontsize=18)
plt.show()
fig.savefig(dirpath + '/outputs/site1/radar/ALOS_PALSAR/sigma0_AGB_07.pdf', bbox_inches='tight')

# plot temporal variation 

y2 = '17' #set year of choice

#plot_no17 = [float(i[1]) for i in matches if i[0] == y2]
AGB17 = [float(i[2]) for i in matches if i[0] == y2]
#HV17 = [float(i[3]) for i in matches if i[0] == y2]
#dHV17 = [float(i[4]) for i in matches if i[0] == y2]
#HH17 = [float(i[5]) for i in matches if i[0] == y2]
#dHH17 = [float(i[6]) for i in matches if i[0] == y2]
HV_HH17 = [float(i[7]) for i in matches if i[0] == y2]
dHV_HH17 = [float(i[8]) for i in matches if i[0] == y2]

lines_time=[Line2D([0], [0], marker='o', color='r', mfc='white', lw=1, label='Logged Plots 2007'),
            Line2D([0], [0], marker='o', color='g', mfc='white', lw=1, label='Unlogged Plots 2007'),
            Line2D([0], [0], marker='o', color='r', lw=2, label='Logged Plots 2017'),
                   Line2D([0], [0], marker='o', color='g', lw=2, label='Unlogged Plots 2017')]

fig = plt.figure(2, figsize=(9,9))
for pos,y,err,color in zip(AGB,HV_HH,dHV_HH,colors):
    plt.errorbar(pos,y,err,lw=2,capsize=5,capthick=1,mfc='white', color=color,fmt='o')
for pos,y,err,color in zip(AGB17,HV_HH17,dHV_HH17,colors):
    plt.errorbar(pos,y,err,lw=2,capsize=5,capthick=2,color=color,fmt='o')
    plt.ylim(0,1)
    plt.xlabel('AGB [Mg/ha]')
    plt.ylabel('HV/HH')
    plt.title('ALOS/PALSAR temporal variation in HH/HV vs AGB per plot for years 2007 and 2017',fontsize=18, pad=30)
    plt.figlegend(handles=lines_time,loc=(0.2,0.1))
    fig.savefig(dirpath + '/outputs/site1/radar/ALOS_PALSAR/HH_HV_compare07_17.pdf', bbox_inches='tight')

