# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 12:25:12 2018

@author: s1326314
"""

#stacked bar plot

import matplotlib.pyplot as plt
import numpy as np

# Define a function for a stacked bar plot
def stackedbarplot(x_data, y_data_list, y_data_names, colors, x_label, y_label, title,save):
    """
    source:https://www.datascience.com/blog/learn-data-science-intro-to-data-visualization-in-matplotlib
    """
    _, ax = plt.subplots()
    # Draw bars, one category at a time
    for i in range(0, len(y_data_list)):
        if i == 0:
            ax.bar(x_data, y_data_list[i], color = colors[i], align = 'center', label = y_data_names[i])
        else:
            # For each category after the first, the bottom of the
            # bar will be the top of the last category
            ax.bar(x_data, y_data_list[i], color = colors[i], bottom = y_data_list[i - 1], align = 'center', label = y_data_names[i])
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    ax.legend(loc = 'upper right')
    ax.savefig(save)

def proportion(x1,x2):
    total = x1 + x2
    x1_prop = x1 / total
    x2_prop = x2 / total
    return x1_prop,x2_prop
    


# plotting example

list07= [10,3,4]
list17= [2,6,75]

y_data = [proportion(a,b) for a,b in zip(list07,list17)]
y1 = [item[0] for item in y_data]
y2 = [item[1] for item in y_data]

x= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]


# Call stacked plot for showing temporal variation for each plot
stackedbarplot(x_data = x
               , y_data_list = [y1,y2]
               , y_data_names = ['2007', '2017']
               , colors = ['#539caf', '#7663b0']
               , x_label = 'Plot number'
               , y_label = 'HH/HV ratio [db]'
               , title = 'Temporal variation for logged and unlogged plots for years 2007 and 2017'
               , save = "R:/rbg_analysis/outputs/site1/radar/2007_2017_time_difference.pdf")


# plot histograms

plt.figure(1)
bn = int((np.amax(x)-np.amin(x))/np.sqrt(np.size(x)))   
hist, bins = np.histogram(x, bins=bn)
bin_centers = (bins[1:]+bins[:-1])*0.5
plt.plot(bin_centers, hist)
