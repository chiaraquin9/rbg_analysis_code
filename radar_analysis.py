### processing radar images

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 10:23:04 2018

@author: s1326314
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 10:03:20 2018

@author: imcnicol
"""

## Load necessary libraries
from osgeo import gdal, gdal_array
import numpy as np
import glob
import os, os.path
import osgeo.ogr
import csv
import re


# Where is your data?
dirpath = '/exports/csce/datastore/geos/users/s1326314/rbg_analysis'
 
#get shapefiles
shapefiles = sorted(glob.glob(dirpath + '/raw_data/site1/raw_shpfiles/projected/*.shp'))


# HV data
HV=[]
HH=[]
HH_HV_ratio=[]

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
        base = re.findall('\d+',shp)
        crop_fname_HV = dirpath + '/outputs/radar/site1/temp_HV.tif'
        crop_fname_HH = dirpath + '/outputs/radar/site1/temp_HH.tif'
        
        #get HV stats
        os.system('gdalwarp -overwrite -cutline ' + shp.replace(' ', '\ ') + ' -crop_to_cutline ' + f_HV + ' ' + crop_fname_HV)
        gHV =gdal.Open(crop_fname_HV)    
        data_HV = gdal_array.DatasetReadAsArray(gHV)
        mean_HV = round(np.mean(data_HV),2)
        std_HV = round(np.std(data_HV),2)
        HV.append([base[2],mean_HV,std_HV]) #for each plot, save label, mean, std   
        
        #get HH stats
        os.system('gdalwarp -overwrite -cutline ' + shp.replace(' ', '\ ') + ' -crop_to_cutline ' + f_HH + ' ' + crop_fname_HH)
        gHH =gdal.Open(crop_fname_HH)    
        data_HH = gdal_array.DatasetReadAsArray(gHH)
        mean_HH = round(np.mean(data_HH),2)
        std_HH = round(np.std(data_HH),2)
        HH.append([base[2],mean_HH,std_HH]) #for each plot, save label, mean, std 
    
    #export HV to csv    
    with open(dirpath + '/outputs/radar/site1/HV_'+ yr +'.csv', "w") as myfile:
        writer = csv.writer(myfile, lineterminator='\n')
        writer.writerow(('Plot','Mean','Std'))
        writer.writerows(HV)
    myfile.close()
    
    #export HH to csv 
    with open(dirpath + '/outputs/radar/site1/HH_'+ yr +'.csv', "w") as myfile:
        writer = csv.writer(myfile, lineterminator='\n')
        writer.writerow(('Plot','Mean','Std'))
        writer.writerows(HH)
    myfile.close()
    
    print("Saved")
    del HV[:]
    del HH[:]
    






