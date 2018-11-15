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
from itertools import groupby

#dirpath = '/exports/csce/datastore/geos/users/s1326314/rbg_analysis'
dirpath = 'R:/rbg_analysis'

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


## select red for logged and green for unlogged plots
#colors = ['red' if i > 11 else 'green' for i in plot_no]
#lines = [Line2D([0], [0], marker='o', color='r', lw=3, label='Logged Plots'),
#                   Line2D([0], [0], marker='o', color='g', lw=3, label='Unlogged Plots')]
#
#fig = plt.figure(1, figsize=(9,9))
#
#ax1 = fig.add_subplot(2,2,1)
#for pos,y,err,color in zip(AGB,HV,dHV,colors):
#    ax1.errorbar(pos,y,err,lw=2,capsize=5,fmt='o',capthick=2,color=color)
#    plt.title('HV vs AGB')
#    plt.xlabel('AGB [Mg/ha]')
#    plt.ylabel('HV [db]')
#    plt.ylim(-16,-9)
#    
#ax2 = fig.add_subplot(2,2,2)
#for pos,y,err,color in zip(AGB,HH,dHH,colors):
#    ax2.errorbar(pos,y,err,lw=2,capsize=5,fmt='o',capthick=2,color=color)
#    plt.title('HH vs AGB')
#    plt.xlabel('AGB [Mg/ha]')
#    plt.ylabel('HH [db]')
#    plt.ylim(-11,-3)
#    
#ax3 = fig.add_subplot(2,1,2)
#for pos,y,err,color in zip(AGB,HV_HH,dHV_HH,colors):
#    ax3.errorbar(pos,y,err,lw=2,capsize=5,fmt='o',capthick=2,color=color)
#    plt.title('HV/HH vs AGB')
#    plt.xlabel('AGB [Mg/ha]')
#    plt.ylabel('HV/HH')
#    plt.ylim(0,1)
#    
#
#plt.figlegend(handles=lines,loc='lower left')
#plt.tight_layout(rect=[0, 0.03, 1, 0.95])
#fig.suptitle('ALOS/PALSAR Backscatter vs AGB per plot for year 2007',fontsize=18)
#plt.show()
#fig.savefig(dirpath + '/outputs/site1/radar/ALOS_PALSAR/sigma0_AGB_07.pdf', bbox_inches='tight')

# plot temporal variation 

y2 = '17' #set year of choice

HV17 = [float(i[3]) for i in matches if i[0] == y2]

#dHV17 = [float(i[4]) for i in matches if i[0] == y2]
#HH17 = [float(i[5]) for i in matches if i[0] == y2]
#dHH17 = [float(i[6]) for i in matches if i[0] == y2]
HV_HH17 = [float(i[7]) for i in matches if i[0] == y2]
dHV_HH17 = [float(i[8]) for i in matches if i[0] == y2]

#lines_time=[Line2D([0], [0], marker='o', color='r', mfc='white', lw=1, label='Logged Plots 2007'),
#            Line2D([0], [0], marker='o', color='g', mfc='white', lw=1, label='Unlogged Plots 2007'),
#            Line2D([0], [0], marker='o', color='r', lw=2, label='Logged Plots 2017'),
#                   Line2D([0], [0], marker='o', color='g', lw=2, label='Unlogged Plots 2017')]
#
#fig = plt.figure(2, figsize=(9,9))
#for pos,y,err,color in zip(AGB,HV_HH,dHV_HH,colors):
#    plt.errorbar(pos,y,err,lw=2,capsize=5,capthick=1,mfc='white', color=color,fmt='o')
#for pos,y,err,color in zip(AGB17,HV_HH17,dHV_HH17,colors):
#    plt.errorbar(pos,y,err,lw=2,capsize=5,capthick=2,color=color,fmt='o')
#    plt.ylim(0,1)
#    plt.xlabel('AGB [Mg/ha]')
#    plt.ylabel('HV/HH')
#    plt.title('ALOS/PALSAR temporal variation in HH/HV vs AGB per plot for years 2007 and 2017',fontsize=18, pad=30)
#    plt.figlegend(handles=lines_time,loc=(0.2,0.1))
#    fig.savefig(dirpath + '/outputs/site1/radar/ALOS_PALSAR/HH_HV_compare07_17.pdf', bbox_inches='tight')


## plot temporal variation
#
#lines = [Line2D([0], [1], color='r', lw=3, label='Logged Plots'),
#                   Line2D([0], [1], marker='o', color='g', lw=3, label='Unlogged Plots')]
#
#width = 0.3   # the width of the bars
#w = [i+width for i in plot_no]  # the position of the second bar     
#
#fig = plt.figure(3)
#ax = fig.add_subplot(111)
#ax.set_axisbelow(True)
#ax.yaxis.grid(color='gray', linestyle='dashed')
#rects1 = ax.bar(plot_no, HV_HH, width, color=['turquoise' if i < 12 else 'teal' for i in plot_no],edgecolor='black')
#rects2 = ax.bar(w, HV_HH17, width, color=['firebrick' if i < 12 else 'maroon' for i in plot_no],edgecolor='black')
## add some
#ax.set_ylabel('Backscatter coefficient [dB]')
##ax.set_ylim(-16,0)
#ax.set_ylim(0,0.7)
#ax.set_xlabel('Plot no.')
#ax.set_title('ALOS PALSAS HV/HH ratio backscatter measurements',fontsize=14, pad=15)
#ax.set_xticks([(x + y)/2 for x, y in zip(plot_no, w)])
#ax.set_xticklabels([i for i in range(1,17)])
#
#
##ax.annotate('', xy=(12, -15), xytext=(16.5, -15),
##            arrowprops={'arrowstyle': '<->'})
#ax.annotate('Logged', xy=(14,0.65), ha='center', va='center',fontsize=13, weight='bold')
##ax.annotate('', xy=(0.7, -15), xytext=(11.5, -15),
##            arrowprops={'arrowstyle': '<->'})
#ax.annotate('Unlogged', xy=(6,0.65), ha='center', va='center',fontsize=13,weight='bold')
#
#first = plt.legend((rects1[0], rects2[0]), ('2007', '2017'),
#          ncol=1,loc='lower left')
#ax = plt.gca().add_artist(first)
#plt.legend( (rects1[12], rects2[12]), ('2007', '2017'),
#          ncol=1,loc='lower right')
#fig.savefig(dirpath + '/outputs/site1/radar/ALOS_PALSAR/HV_HH_07_17.pdf', bbox_inches='tight')
#
#plt.show()

######################### PLOT AVERAGES FOR ALL YEARS ########################################


#match AGB and radar data for the same plots
matches2 = [[j[0],float(i[0]),  float(i[1]),float(j[2]),
            float(j[3]),float(j[4]),float(j[5]),float(j[6]),float(j[7])] for i in AGB_data for j in radar_data if i[0] == j[1]]
matches2.sort(key=lambda x: float(x[0]))

#Calculate average values for logged plots

#select HV, HH, HV/HH for logged plots (plot no smaller than 12)
logged_data = [[i[0],i[3],i[5],i[7]] for i in matches2 if i[1] > 11]
#group values for HV,HH and HV/HH ratio based on year
HV_data_log = [(n,[i[1] for i in g]) for n,g in groupby(logged_data, key = lambda x:x[0])]
HH_data_log = [(n,[i[2] for i in g]) for n,g in groupby(logged_data, key = lambda x:x[0])] 
HV_HH_data_log = [(n,[i[3] for i in g]) for n,g in groupby(logged_data, key = lambda x:x[0])]
#calculate averages for each year    
HV_log = [(i,float(sum(j))/float(len(j))) for i,j in HV_data_log]
HH_log = [(i,float(sum(j))/float(len(j))) for i,j in HH_data_log]
HV_HH_log = [(i,float(sum(j))/float(len(j))) for i,j in HV_HH_data_log]

#Calculate average values for unlogged plots

#select HV, HH, HV/HH for unlogged plots (plot no bigger than 11)
unlogged_data = [[i[0],i[3],i[5],i[7]] for i in matches2 if i[1] < 12]
#group values for HV,HH and HV/HH ratio based on year
HV_data_unlog = [(n,[i[1] for i in g]) for n,g in groupby(unlogged_data, key = lambda x:x[0])]
HH_data_unlog = [(n,[i[2] for i in g]) for n,g in groupby(unlogged_data, key = lambda x:x[0])] 
HV_HH_data_unlog = [(n,[i[3] for i in g]) for n,g in groupby(unlogged_data, key = lambda x:x[0])]
#calculate averages for each year    
HV_unlog = [(i,float(sum(j))/float(len(j))) for i,j in HV_data_unlog]
HH_unlog = [(i,float(sum(j))/float(len(j))) for i,j in HH_data_unlog]
HV_HH_unlog = [(i,float(sum(j))/float(len(j))) for i,j in HV_HH_data_unlog]

#plot averages for all years 2007-2017. These are the averages over all the unlogged vs logged plots
w = 0.1   # the width of the bar

x = [2007,2008,2009,2010,2015,2016,2017]
y_log = [i[1] for i in HV_HH_log if i[0] != '96']
y_unlog = [i[1] for i in HV_HH_unlog if i[0] != '96']
y_logHV = [i[1] for i in HV_log if i[0] != '96']
y_unlogHV = [i[1] for i in HV_unlog if i[0] != '96']
y_logHH = [i[1] for i in HH_log if i[0] != '96']
y_unlogHH = [i[1] for i in HH_unlog if i[0] != '96']
idx = np.asarray([i for i in range(len(x))])


fig = plt.figure(4,figsize=(15,15))
ax = fig.add_subplot(311)
ax.yaxis.grid(color='gray', linestyle='dashed')
rects_unlog = ax.bar(idx+w, y_unlog, width=w , color='forestgreen',edgecolor='black',align='center')
rects_log = ax.bar(idx,y_log, width=w, color='tomato',edgecolor='black',align='center')
#rects_unlog1 = ax.bar(idx, y_unlogHV, width=w , color='green',edgecolor='black',align='center')
#rects_log1 = ax.bar(idx+(3*w),y_logHV, width=w, color='tomato',edgecolor='firebrick',align='center')
#rects_unlog2 = ax.bar(idx+(4*w), y_unlogHH, width=w , color='forestgreen',edgecolor='black',align='center')
#rects_log2 = ax.bar(idx+(5*w),y_logHH, width=w, color='tomato',edgecolor='black',align='center')
#ax.autoscale(tight=True)
ax.set_ylabel('Backscatter coefficient [dB]')
ax.set_xlim(-1,7)
ax.set_ylim(0,0.7)
ax.set_xticks(idx+(w/2))
ax.set_xticklabels(x, rotation=65)

#
#ax1 = fig.add_subplot(312)
#ax1.yaxis.grid(color='gray', linestyle='dashed')
#rects_unlog1 = ax1.bar(idx+w, y_unlogHV, width=w , color='forestgreen',edgecolor='darkgreen',align='center')
#rects_log1 = ax1.bar(idx,y_logHV, width=w, color='tomato',edgecolor='firebrick',align='center')
#ax1.set_xticks(idx+(w/2))
#ax1.set_xticklabels(x, rotation=65)
#ax1.set_ylabel('HV [dB]')
#ax1.set_ylim(-14,0)
#ax1.set_xlim(-1,7)
#
#ax2 = fig.add_subplot(313)
#ax2.yaxis.grid(color='gray', linestyle='dashed')
#rects_unlog2 = ax2.bar(idx+w, y_unlogHH, width=w , color='forestgreen',edgecolor='darkgreen',align='center')
#rects_log2 = ax2.bar(idx,y_logHH, width=w, color='tomato',edgecolor='firebrick',align='center')
#ax2.set_xticks(idx+(w/2))
#ax2.set_xticklabels(x, rotation=65)
#ax2.set_ylabel('HH [dB]')
#ax2.set_xlim(-1,7)
#ax2.set_ylim(-14,0)



plt.legend((rects_log[0], rects_unlog[0]), ('Logged', 'Unlogged'))
fig.suptitle('ALOS/PALSAR backscatter averages over time',fontsize=18,pad=15)
fig.savefig(dirpath + '/outputs/site1/radar/ALOS_PALSAR/ALOS_PALSAR_averages_over_time.pdf', bbox_inches='tight')
plt.show()

