### processing radar images

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
    ds = (2/(x*np.log(10)))*dx
    return ds


# Where is your data?
dirpath = '/exports/csce/datastore/geos/users/s1326314/rbg_analysis'
 
#get shapefiles
shapefiles = sorted(glob.glob(dirpath + '/raw_data/site1/raw_shpfiles/projected/*.shp'))

output=[]
sigma=[]

#loop for each year for all the HV and hh (years after 2015 are from ALOS Palsar2):
for folder in os.listdir(dirpath + '/radar/'):
    yr = folder[8:-4]
    if yr == '17' or yr == '16' or yr == '15':
        f_HV = dirpath + '/radar/N03E016_'+ yr + '_MOS/N03E016_' + yr + '_sl_HV_F02DAR'
        f_HH = dirpath + '/radar/N03E016_'+ yr + '_MOS/N03E016_' + yr + '_sl_HH_F02DAR'
    else:
        f_HV = dirpath + '/radar/N03E016_'+ yr + '_MOS/N03E016_' + yr + '_sl_HV'
        f_HH = dirpath + '/radar/N03E016_'+ yr + '_MOS/N03E016_' + yr + '_sl_HH'
    
    #crop shapefiles
    for shp in shapefiles:
        base = re.findall('\d+',shp) # get plot number
        index = int(base[2])
        
        crop_fname= dirpath + '/outputs/site1/radar/temp.tif'
        
        #get HV stats
        os.system('gdalwarp -overwrite -cutline ' + shp.replace(' ', '\ ') + ' -crop_to_cutline ' + f_HV + ' ' + crop_fname)
        gHV =gdal.Open(crop_fname)    
        data_HV = gdal_array.DatasetReadAsArray(gHV)
        mean_HV = round(np.mean(data_HV),2)
        std_HV = round(np.std(data_HV),2)
    
        #get HH stats
        os.system('gdalwarp -overwrite -cutline ' + shp.replace(' ', '\ ') + ' -crop_to_cutline ' + f_HH + ' ' + crop_fname)
        gHH =gdal.Open(crop_fname)

        data_HH = gdal_array.DatasetReadAsArray(gHH)
        mean_HH = round(np.mean(data_HH),2)
        std_HH = round(np.std(data_HH),2)
        
        #get HH/HV stats
        mean_HH_HV = mean_HH/mean_HV
        std_HH_HV = std_HH/std_HV
        
        #save to array
        output.append([index,mean_HV,std_HV,mean_HH,std_HH,mean_HH_HV,std_HH_HV]) #for each plot, save label, mean, std            
        #convert from DN in sigma
        output_conv = [(i1, convert(i2),std(i2,i3),convert(i4),std(i4,i5),i6,i7) for i1,i2,i3,i4,i5,i6,i7 in output]
        output_conv.sort(key=lambda x: x[0])
        
    #export to csv    
    with open(dirpath + '/outputs/site1/radar/stats_'+ yr +'.csv', "w") as myfile:
        writer = csv.writer(myfile, lineterminator='\n')
        writer.writerow(('Plot','Mean_HV','Std_HV','Mean_HH','Std_HH','Mean_HH/HV','Std_HH/HV'))
        writer.writerows(output_conv)
        myfile.close()
    
    print("...Exported")
    del output[:]
    del output_conv[:]
    


    





