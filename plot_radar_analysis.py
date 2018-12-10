# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 10:37:17 2018

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

#import csv file for AGB data
AGB = pd.read_csv( dirpath + '/outputs/site1/AGB/AGB.csv')

###### ALOS PALSAR #####

##import csv file containing ALOS PALSAR backscatter data for all years
all_files = glob.glob(dirpath + "/outputs/site1/radar/ALOS_PALSAR/*.csv")
bsc = pd.concat((pd.read_csv(f) for f in all_files))

#filter data for years > 1996
alos = bsc[bsc['Year']>1996]

#filter data for logged and unlogged plots and take averages

l = alos.drop(alos[alos.Plot < 12].index)      # remove data of unlogged plots
logged = l.groupby(['Year']).mean()          # calculate averages for each year

unl = alos.drop(alos[alos.Plot > 11].index)    # remove data of logged plots
unlogged = unl.groupby(['Year']).mean()      # calculate averages for each year


####### Sentinel-1 ######

#import csv file containing S1 backscatter data for 1 year
s1 = pd.read_csv( dirpath + '/outputs/site1/radar/S1/2016_stats_allyear.csv')

ls1 = s1.drop(s1[s1.Plot < 12].index)      # remove data of unlogged plots
s1logged = ls1.mean()
unls1 = s1.drop(s1[s1.Plot > 11].index)      # remove data of unlogged plots
s1unlogged = unls1.mean()

s1_data = ['VV', 'VH', 'VH/VV']
alos_data = ['HH', 'HV', 'HV/HH']



################################################################################
######################### BACKSCATTER PLOTS #############################
################################################################################


#S1: VV vs AGB

s1 = s1.astype({"Plot": int})
colors = ['red' if i>11 else 'green' for i in s1['Plot']]
lines = [Line2D([0], [0], marker='o', color='r', lw=3, label='Logged Plots'),
                   Line2D([0], [0], marker='o', color='g', lw=3, label='Unlogged Plots')]

labels = ['plot{0}'.format(i) for i in s1['Plot']]

fig = plt.figure(3, figsize=(12,8))
ax0 = fig.add_subplot(121)

#for pos,y,err,color in zip(AGB['AGB (Mg/ha)'],s1['VV'],s1['d_VV'],colors):
for pos,y,err,color in zip(s1['Plot'],s1['VV'],s1['d_VV'],colors):
    ax0.errorbar(pos,y,err,lw=2,capsize=5,fmt='o',capthick=2,color=color)
    plt.title('Sentinel-1 VV vs AGB')
    #plt.xlabel('AGB [Mg/ha]')
    plt.xlabel('Plot no.')
    plt.ylabel('VV [db]')
    plt.ylim(-12,-2)
    
#for label, x, y in zip(labels, AGB['AGB (Mg/ha)'], s1['VV']):
#    plt.annotate(
#        label,
#        xy=(x, y), xytext=(-20, 20),
#        textcoords='offset points', ha='right', va='bottom',
#        bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.5),
#        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))


#ALOS-PALSAR: HH vs AGB

#choose one year
alos_2016 = bsc[bsc['Year']==2016]

ax01 = fig.add_subplot(122)

#for pos,y,err,color in zip(AGB['AGB (Mg/ha)'],alos_2016['HH'],alos_2016['d_HH'],colors):
for pos,y,err,color in zip(alos_2016['Plot'],alos_2016['HH'],alos_2016['d_HH'],colors):
    ax01.errorbar(pos,y,err,lw=2,capsize=5,fmt='o',capthick=2,color=color)
    plt.title('ALOS-PALSAR HH vs AGB')
    #plt.xlabel('AGB [Mg/ha]')
    plt.xlabel('Plot no.')
    plt.ylabel('HH [db]')
    plt.ylim(-12,-2)

plt.figlegend(handles=lines,loc='lower left')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.suptitle('ALOS-PALSAR and SENTINEL-1 Backscatter vs AGB per plot for year 2016',fontsize=18)
plt.show()
#fig.savefig(dirpath + '/outputs/site1/radar/ALOS_PALSAR/sigma0_AGB_07.pdf', bbox_inches='tight')



################################################################################
############ PLOT AVERAGES FOR LOGGED/UNLOGGED PLOTS VS YEAR ###################
################################################################################
#
#
#fig = plt.figure(1, figsize=(9,13))
#fig.suptitle("ALOS PALSAR Averages for Backscatter Measurements", fontsize=18, y=1.03, ha='center', va='center')
#width = 0.2
#
## plot subfigure 1 with HV data
#ax = fig.add_subplot(311)
#
#unlogged.HV.plot(kind='bar', color='forestgreen', ax=ax, width=width, position=0, edgecolor='black')
#logged.HV.plot(kind='bar', color='tomato', ax=ax, width=width, position=1, edgecolor='black')
#
#ax.yaxis.grid(color='gray', linestyle='dashed')
#ax.set_ylabel('Backscatter coefficient [dB]')
#ax.set_xlabel('')
#ax.set_ylim(-14,0)
#ax.set_xlim(-1,8)
#ax.set_title('HV backscatter', pad=10)
#ax.legend(['Unlogged', 'Logged'], loc='lower right')
#
## plot subfigure 2 with HH data
#ax1 = fig.add_subplot(312)
#
#unlogged.HH.plot(kind='bar', color='forestgreen', ax=ax1, width=width, position=0, edgecolor='black')
#logged.HH.plot(kind='bar', color='tomato', ax=ax1, width=width, position=1, edgecolor='black')
#
#ax1.yaxis.grid(color='gray', linestyle='dashed')
#ax1.set_ylabel('Backscatter coefficient [dB]')
#ax1.set_xlabel('')
#ax1.set_ylim(-8,0)
#ax1.set_xlim(-1,8)
#ax1.set_title('HH backscatter', pad=10)
#ax1.legend(['Unlogged', 'Logged'], loc='lower right')
#
## plot subfigure 3 with HV/HH data
#ax2 = fig.add_subplot(313)
#
#unlogged.ratio.plot(kind='bar', color='forestgreen', ax=ax2, width=width, position=0, edgecolor='black')
#logged.ratio.plot(kind='bar', color='tomato', ax=ax2, width=width, position=1, edgecolor='black')
#
#ax2.yaxis.grid(color='gray', linestyle='dashed')
#ax2.set_ylabel('Backscatter coefficient [dB]')
#ax2.set_xlabel('')
#ax2.set_ylim(0,0.7)
#ax2.set_xlim(-1,8)
#ax2.set_title('HV/HH ratio', pad=10)
#ax2.legend(['Unlogged', 'Logged'], loc='lower right')
#
##plt.title('ALOS/PALSAR backscatter averages over time',fontsize=18,pad=45)
#plt.tight_layout()
#fig.savefig(dirpath + '/outputs/site1/radar/ALOS_PALSAR/ALOS_PALSAR_averages_over_time.pdf', bbox_inches='tight')
#plt.show()


################################################################################
#################### BACKSCATTER BOX AND WHISKER PLOT #########################
################################################################################


lpos = [1.2,3.2,5.2,7.2,9.2,11.2,13.2]
unlpos = [1.8,3.8,5.8,7.8,9.8,11.8,13.8]
green_patch = mpatches.Patch(color='green', label='Unlogged')
red_patch = mpatches.Patch(color='red', label='Logged')

fig = plt.figure(2, figsize=(12,10))


plotnum = 1

for alos in alos_data:
    ax = fig.add_subplot(2,2,plotnum)
    bx_l = l.boxplot(by='Year',column=[alos], ax=ax,positions=lpos, patch_artist = True, return_type='dict', grid= False)
    bx_unl = unl.boxplot(by='Year',column=[alos], ax=ax,positions=unlpos, patch_artist = True, return_type='dict', grid=False)
    
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
        
           
    ax.set_xlim(0,15)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    ax.set_ylabel('Backscatter coefficient [dB]')

    plt.legend(handles=[red_patch, green_patch], fontsize=16)
    plt.legend(handles=[red_patch, green_patch], fontsize=16)

# label adjustment
fig.suptitle("ALOS PALSAR Backscatter Boxplot", fontsize=18, y=1.03, ha='center', va='center')
plt.tight_layout()
fig.savefig(dirpath + '/outputs/site1/radar/ALOS_PALSAR/ALOS_PALSAR_HV_log_unlog_boxplot.pdf', 
            bbox_inches='tight')


###### box and whisker comparison ALOS Palsar and S1 for year 2016

lalos = l[l['Year']==2016]     
unlalos = unl[unl['Year']==2016]  

fig = plt.figure(4, figsize=(10,16))

plotnum = 1

for alos, s1 in zip(alos_data, s1_data):
    ax_alos = fig.add_subplot(3,2,plotnum)
    bx_lalos = lalos.boxplot(column=[alos], ax=ax_alos,positions=[1], patch_artist = True, return_type='dict')
    bx_unlalos = unlalos.boxplot(column=[alos], ax=ax_alos,positions=[1.2], patch_artist = True, return_type='dict')
    
    if plotnum == 1:
        ax_alos.set_title('ALOS PALSAR', fontsize=14)
    if plotnum == 5:
        ax_alos.set_ylabel('Ratio')
    else:
        ax_alos.set_ylabel('Backscatter coefficient [dB]')
    
    plotnum += 1
    
    ax_s1 = fig.add_subplot(3,2,plotnum)
    bx_ls1= ls1.boxplot(column=[s1], ax=ax_s1, positions=[1], patch_artist = True, return_type='dict')
    bx_unls1 = unls1.boxplot(column=[s1], ax=ax_s1, positions=[1.2], patch_artist = True, return_type='dict')
    
    if plotnum == 2:
        ax_s1.set_title('Sentinel-1', fontsize=14)

    plotnum += 1
    
    [item.set_color('r') for item in bx_lalos['boxes']]
    [item.set_color('g') for item in bx_unlalos['boxes']]
    [item.set_color('r') for item in bx_ls1['boxes']]
    [item.set_color('g') for item in bx_unls1['boxes']]
    [item.set_color('y') for item in bx_lalos['medians']]
    [item.set_color('y') for item in bx_unlalos['medians']]
    [item.set_color('y') for item in bx_ls1['medians']]
    [item.set_color('y') for item in bx_unls1['medians']]
    
    
    plt.legend(handles=[red_patch, green_patch], fontsize=16, loc="upper right")
    plt.legend(handles=[red_patch, green_patch], fontsize=16, loc="upper right")
    


fig.suptitle("ALOS PALSAR and Sentinel-1 Backscatter Box and Whisker Plots for Year 2016", fontsize=18, y=1.03, ha='center', va='center')
plt.tight_layout()

fig.savefig(dirpath + '/outputs/site1/radar/ALOS_vs_S1.pdf', 
        bbox_inches='tight')





