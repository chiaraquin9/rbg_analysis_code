# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 16:17:09 2018

@author: s1326314
"""
### processing radar images: calculating mean and standard deviation for HH,HV and HV/HH ratio. 
### there's also an option to filter out outliers to reduce standard deviation.

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 10:23:04 2018

@author: s1326314
"""

## Load necessary libraries
from osgeo import gdal, gdal_array
import numpy as np
import glob
import os, os.path
import osgeo.ogr
import csv
import re
import matplotlib.pyplot as plt
import functions as f


#convert DN into backscatter
def convert(x):
    """
    convert Digital Numbers from radar raster into backscatter
    x = DN
    """
    s = 10*np.log10(x**2)-83.0
    return s

#convert std into backscatter (error propagation)
def std(x,dx):
    """
    convert Digital Numbers from radar raster into backscatter (for standard deviation)
    x = DN
    dx = error on DN
    """
    ds = (20/(x*np.log(10)))*dx
    return ds

#propagation of errors 
def propagation(x,dx,y,dy,q):
    """
    propagate uncertainties in the ratio
    """
    dq = q*np.sqrt((dx/x)**2 + (dy/y)**2)
    return dq

# Where is your data?
dirpath = '/exports/csce/datastore/geos/users/s1326314/rbg_analysis'
#dirpath = 'R:/rbg_analysis'

 
#get shapefiles
shapefiles = sorted(glob.glob(dirpath + '/raw_data/site1/raw_shpfiles/projected/*.shp'))

output=[]

#VH compares to HH while VV compares to HV

#year data

f_VV = dirpath + '/radar/S1/S1_VV_Mean_2016_20m.tif'
f_VH = dirpath + '/radar/S1/S1_VH_Mean_2016_20m.tif'

for shp in shapefiles:
    base = re.findall('\d+',shp) # get plot number
    index = int(base[2])
    
    crop_fname= dirpath + '/outputs/site1/radar/ALOS_PALSAR/temp.tif'
    
    #get VH stats
    os.system('gdalwarp -overwrite -cutline ' + shp.replace(' ', '\ ') + ' -crop_to_cutline ' + f_VH + ' ' + crop_fname)
    gVH =gdal.Open(crop_fname)    
    data_VH = gdal_array.DatasetReadAsArray(gVH)
    mean_VH = np.mean(data_VH)
    std_VH = np.std(data_VH)
            

    #get VV statsdA
    os.system('gdalwarp -overwrite -cutline ' + shp.replace(' ', '\ ') + ' -crop_to_cutline ' + f_VV + ' ' + crop_fname)
    gVV =gdal.Open(crop_fname)
    data_VV = gdal_array.DatasetReadAsArray(gVV)                
    mean_VV = np.mean(data_VV)
    std_VV = np.std(data_VV)
    
    #get HV/HH stats (this ratio is not reported in db)
    VH_VV = mean_VH/mean_VV
    d_VH_VV = propagation(mean_VH,std_VH,mean_VV,std_VV,VH_VV)
    
    #save to array
    output.append([index,mean_VH,std_VH,mean_VV,std_VV,VH_VV,d_VH_VV])
    output.sort(key=lambda x: x[0])
    
#export to csv    
with open(dirpath + '/outputs/site1/radar/S1/2016_stats_allyear.csv', "w") as myfile:
    writer = csv.writer(myfile, lineterminator='\n')
    writer.writerow(('Plot','VH','d_VH','VV','d_VV','VH/VV','dVH/VV'))
    writer.writerows(output)
    myfile.close()

print("...Exported")
del output[:]
    
    
    






