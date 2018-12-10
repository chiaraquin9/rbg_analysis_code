# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 16:55:04 2018

@author: s1326314
"""
import numpy as np
import pandas as pd
import glob
import os, os.path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

#plotting parameters
params = {'legend.fontsize': 'large',
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
plt.rcParams.update(params)

#dirpath = '/exports/csce/datastore/geos/users/s1326314/rbg_analysis'
dirpath = 'R:/rbg_analysis'


#import csv file containing S1 montly backscatter data
all_files = glob.glob(dirpath + "/outputs/site1/radar/S1/2016/*.csv")
S1 = pd.concat((pd.read_csv(f) for f in all_files))

#filter data for logged and unlogged plots and take averages
#logged plots: 12-16
#unlogged plots: 1-11

l = S1.drop(S1[S1.Plot < 12].index)      # remove data of unlogged plots
l.sort_values(by=['Month'], inplace=True, ascending=True) # order by month
logged = l.groupby('Month', as_index=False)['VV','VH','VH/VV'].mean()          # calculate averages for each year

unl = S1.drop(S1[S1.Plot > 11].index)    # remove data of logged plots
unl.sort_values(by=['Month'], inplace=True, ascending=True) # order by month
unlogged = unl.groupby('Month', as_index=False)['VV','VH','VH/VV'].mean()        # calculate averages for each year


s1_data = ['VV', 'VH', 'VH/VV']
months= ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# plot features

lpos = [1.2,3.2,5.2,7.2,9.2,11.2,13.2,15.2,17.2,19.2,21.2,23.2]
unlpos = [1.8,3.8,5.8,7.8,9.8,11.8,13.8,15.8,17.8,19.8,21.8,23.8]
green_patch = mpatches.Patch(color='green', label='Unlogged')
red_patch = mpatches.Patch(color='red', label='Logged')
lines = [Line2D([0], [0], color='g', lw=2, label='Unlogged'),
                Line2D([0], [0], color='r', lw=2, label='Logged'),]

#BOX AND WHISKER PLOT FOR SEASONAL TIME SERIES

fig = plt.figure(1, figsize=(12,12))

plotnum = 1

for x in s1_data:
    ax = fig.add_subplot(3,1,plotnum)
    bx_l = l.boxplot(by='Month',column=[x], ax=ax,positions=lpos, patch_artist = True, return_type='dict', grid= False)
    bx_unl = unl.boxplot(by='Month',column=[x], ax=ax,positions=unlpos, patch_artist = True, return_type='dict', grid=False)
    
    plotnum += 1

    [[item.set_color('r') for item in bx_l[key]['boxes']] for key in bx_l.keys()]
    [[item.set_linewidth(0.8) for item in bx_l[key]['medians']] for key in bx_l.keys()]
    [[item.set_color('y') for item in bx_l[key]['medians']] for key in bx_l.keys()]
    [[item.set_color('k') for item in bx_l[key]['whiskers']] for key in bx_l.keys()]
    [[item.set_linestyle('--') for  item in bx_l[key]['whiskers']] for key in bx_l.keys()]
    [[item.set_color('g') for item in bx_unl[key]['boxes']] for key in bx_unl.keys()]
    [[item.set_linewidth(0.8) for item in bx_unl[key]['medians']] for key in bx_unl.keys()]
    [[item.set_color('y') for item in bx_unl[key]['medians']] for key in bx_unl.keys()]
    [[item.set_color('k') for item in bx_unl[key]['whiskers']] for key in bx_unl.keys()]
    [[item.set_linestyle('--') for item in bx_unl[key]['whiskers']] for key in bx_unl.keys()]
        
           
    ax.set_xlim(0,25)
    ax.tick_params(axis='x')
    ax.tick_params(axis='y', labelsize=14)
    ax.set_xticklabels(months, rotation=45, fontsize=14)
    ax.set_ylabel('Backscatter coefficient ' + x +  ' [dB]')
    ax.set_xlabel('')
    ax.set_title('')


    plt.legend(handles=[red_patch, green_patch], fontsize=14, loc='upper right')
    plt.legend(handles=[red_patch, green_patch], fontsize=14, loc='upper right')

# label adjustment

#plt.tight_layout()
fig.suptitle("Sentinel-1 Box and Whisker Monthly Time Series for Logged and Unlogged Plots", fontsize=18, y=0.95,ha='center', va='center')
fig.savefig(dirpath + '/outputs/site1/radar/S1/S1_monthly_boxplot_2016.pdf')
plt.show()
    

#TIMELINE FOR SEASONAL TIME SERIES (AVERAGES)

fig = plt.figure(2, figsize=(12,12))

plotnum = 1

for data in s1_data:
    ax = fig.add_subplot(3,1,plotnum)
    logged.plot(x='Month',y=data, ax=ax, label='Logged', color='r', grid=True, title=data)
    unlogged.plot(x='Month',y=data, ax=ax,label='Unlogged', color='g', grid=True, title=data)
    ax.set_xticks(logged.Month)
    ax.set_xticklabels(months, rotation=45, fontsize=14)
    ax.set_xlabel('')
    ax.legend(handles=lines,loc='upper right', fontsize=14)


    
    plotnum += 1
        
    ax.set_ylabel('Backscatter coefficient ' + data +  ' [dB]')
    ax.set_title('')

# label adjustment
fig.suptitle("Sentinel-1 Monthly Time Series for Averages of Logged and Unlogged Plots", fontsize=18, y=0.95, ha='center', va='center')
#plt.tight_layout()
fig.savefig(dirpath + '/outputs/site1/radar/S1/S1_monthly_averages_2016.pdf')
plt.show()
    
    
   
#TIMELINE FOR SEASONAL TIME SERIES (ALL PLOTS)


fig = plt.figure(3, figsize=(12,12))

plotnum = 1

for data in s1_data:
    ax = fig.add_subplot(3,1,plotnum)
    l.groupby('Plot').plot(kind='line', x = "Month", y = data, ax=ax,title=data, grid=True, legend=False, color='r')
    unl.groupby('Plot').plot(kind='line', x = "Month", y = data, ax=ax, title=data, grid=True, legend=False, color='g')
    ax.set_xticks(logged.Month)
    ax.set_xticklabels(months, rotation=45, fontsize=14)
    ax.set_xlabel('')
    ax.legend(handles=lines,loc='upper right', fontsize=14)

    
    plotnum += 1
        
          
    #ax.set_xlim(0,12)
    ax.set_ylabel('Backscatter coefficient ' + data +  ' [dB]')
    ax.set_title('')

# label adjustment
#plt.tight_layout()
fig.suptitle("Sentinel-1 Monthly Time Series for Logged and Unlogged Plots", fontsize=16, y=0.95, ha='center', va='center')
fig.savefig(dirpath + '/outputs/site1/radar/S1/S1_monthly_lineseries_2016.pdf')
plt.show()




