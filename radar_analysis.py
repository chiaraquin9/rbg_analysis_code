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

 
#get shapefiles
shapefiles = sorted(glob.glob(dirpath + '/raw_data/site1/raw_shpfiles/projected/*.shp'))

output=[]

#loop for each year for all the HV and hh (years after 2015 are from ALOS Palsar2):
for folder in os.listdir(dirpath + '/radar/ALOS_PALSAR/'):
    yr = folder[8:-4]
    if yr == '17' or yr == '16' or yr == '15':
        f_HV = dirpath + '/radar/ALOS_PALSAR/N03E016_'+ yr + '_MOS/N03E016_' + yr + '_sl_HV_F02DAR'
        f_HH = dirpath + '/radar/ALOS_PALSAR/N03E016_'+ yr + '_MOS/N03E016_' + yr + '_sl_HH_F02DAR'
    else:
        f_HV = dirpath + '/radar/ALOS_PALSAR/N03E016_'+ yr + '_MOS/N03E016_' + yr + '_sl_HV'
        f_HH = dirpath + '/radar/ALOS_PALSAR/N03E016_'+ yr + '_MOS/N03E016_' + yr + '_sl_HH'
    
    #crop shapefiles
    for shp in shapefiles:
        base = re.findall('\d+',shp) # get plot number
        index = int(base[2])
        
        crop_fname= dirpath + '/outputs/site1/radar/ALOS_PALSAR/temp.tif'
        
        #get HV stats
        os.system('gdalwarp -overwrite -cutline ' + shp.replace(' ', '\ ') + ' -crop_to_cutline ' + f_HV + ' ' + crop_fname)
        gHV =gdal.Open(crop_fname)    
        data_HV = gdal_array.DatasetReadAsArray(gHV)
        mean_HV = np.mean(data_HV)
        std_HV = np.std(data_HV)
        
#        filtHV = f.reject_outliers(data_HV) # remove outliers   
#        mean_HV = np.mean(filtHV)
#        std_HV = np.std(filtHV)
    
        #get HH stats
        os.system('gdalwarp -overwrite -cutline ' + shp.replace(' ', '\ ') + ' -crop_to_cutline ' + f_HH + ' ' + crop_fname)
        gHH =gdal.Open(crop_fname)
        data_HH = gdal_array.DatasetReadAsArray(gHH)                
        mean_HH = np.mean(data_HH)
        std_HH = np.std(data_HH)
#         
#        filtHH = f.reject_outliers(data_HH) #remove outliers     
#        mean_HH = np.mean(filtHH)
#        std_HH = np.std(filtHH)
        
        #convert in db
        HV = convert(mean_HV)
        dHV = std(mean_HV,std_HV)
        HH = convert(mean_HH)
        dHH = std(mean_HH,std_HH)
        
        #get HV/HH stats (this ratio is not reported in db)
        HV_HH = mean_HV/mean_HH
        d_HV_HH = propagation(mean_HV,std_HV,mean_HH,std_HH,HV_HH)
        
        #save to array
        output.append([index,HV,dHV,HH,dHH,HV_HH,d_HV_HH])
        output.sort(key=lambda x: x[0])
        
    #export to csv    
    with open(dirpath + '/outputs/site1/radar/ALOS_PALSAR/stats_'+ yr +'.csv', "w") as myfile:
        writer = csv.writer(myfile, lineterminator='\n')
        writer.writerow(('Plot','HV','d_HV','HH','d_HH','HV/HH','d_HV/HH'))
        writer.writerows(output)
        myfile.close()
    
    print("...Exported")
    del output[:]
    
    





