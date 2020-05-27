# -*- coding: utf-8 -*-
"""
Created on Wed May 27 09:04:59 2020

OBJ: PARAMETER CALCULATION FOR GRASS-GROW MODEL (annual)
@author: ICJRC
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from osgeo import gdal

# INPUT FILE DATA
work_path = 'C:/Users/57314/Google Drive/EPM_PUJ/Ejecucion/GIS/RAS'
raster_01 = 'cobertura_tierra_2000_2002_TRIM_3115.tif'
raster_02 = 'cobertura_tierra_2005_2009_TRIM_3115.tif'
timer_001 = 2002 # YEAR
timer_002 = 2005 # YEAR

# INPUT ARRAY DATA ID
id_for = 1
id_har = 2
id_gra = 4
id_wat = 5
id_oth = 3

# INPUT DEBUG MODE
bug = 0

# AUXILIAR FUNCTIONS
def dem_extract (DEM):
    # Raster 2 array
    db_DEM = DEM.GetRasterBand(1).ReadAsArray()
    na_val = DEM.GetRasterBand(1).GetNoDataValue()
    db_DEM = np.array(db_DEM)
    db_DEM [db_DEM == na_val] = float('nan')
    return(db_DEM)

def comparison (id_ini, id_fin, mat_t0, mat_t1, i):
    dummy = np.copy(mat_t0)
    dummy[dummy != id_ini] = 0
    dummy[dummy == id_ini] = 1
    
    dummy1 = np.copy(mat_t1)
    dummy1[dummy != 1] = 0 
    
    dummy1[dummy1 != id_fin] = 0
    dummy1[dummy1 == id_fin] = 1
    if i == 1:
        print('Debug mode ON')
        print(str(id_ini) + ' to ' + str(id_fin))
        print(np.sum(dummy1))
        plt.imshow(dummy1)
        plt.show()
    return(np.sum(dummy1))

def main_extractor(id_for, id_gra, id_har, id_wat, id_oth, vec_t, vec_t1, dt, bug):      
    # ------------------------------------------------------------
    # ----------- FOREST -----------------------------------------
    # ------------------------------------------------------------
    # Forest to grass analysis
    hf2g = comparison (id_for, id_gra, vec_t, vec_t1, bug)
    # Grass to forest analysis
    hg2f = comparison (id_gra, id_for, vec_t, vec_t1, bug)
    
    # ------------------------------------------------------------
    # ----------- HARVEST ----------------------------------------
    # ------------------------------------------------------------
    # Harvest to grass
    hh2g = comparison (id_har, id_gra, vec_t, vec_t1, bug)
    # Grass to harvest
    hg2h = comparison (id_gra, id_har, vec_t, vec_t1, bug)
    
    # ------------------------------------------------------------
    # ------------ OTHER -----------------------------------------
    # ------------------------------------------------------------
    # OTHER to grass
    ho2g = comparison (id_oth, id_gra, vec_t, vec_t1, bug)
    # Grass to OTHER
    hg2o = comparison (id_gra, id_oth, vec_t, vec_t1, bug)
    
    # ------------------------------------------------------------
    # ------------ WATER -----------------------------------------
    # ------------------------------------------------------------
    # WATER to grass
    hw2g = comparison (id_wat, id_gra, vec_t, vec_t1, bug)
    # Grass to WATER
    hg2w = comparison (id_gra, id_wat, vec_t, vec_t1, bug)

    # ----------- Parameters -------------------------------------
    hept0 = np.sum([vec_t == id_gra])
    
    hf2g = hf2g / (hept0 * dt)
    hh2g = hh2g / (hept0 * dt)
    hw2g = hw2g / (hept0 * dt)
    ho2g = ho2g / (hept0 * dt)
    
    hg2f = hg2f / (hept0 * dt)
    hg2h = hg2h / (hept0 * dt)
    hg2w = hg2w / (hept0 * dt)
    hg2o = hg2o / (hept0 * dt)
    
    return (hept0, hf2g, hh2g, hw2g, ho2g, hg2f, hg2h, hg2w, hg2o)

# MAIN
# Extraction raster data
os.chdir(work_path)
DEM = gdal.Open(raster_01)
db_DEM_1 = dem_extract (DEM)

DEM = gdal.Open(raster_02)
db_DEM_2 = dem_extract(DEM)
dt = timer_002 - timer_001

# Extraction parameters
hept0, hf2g, hh2g, hw2g, ho2g, hg2f, hg2h, hg2w, hg2o = main_extractor(id_for, id_gra, id_har, id_wat, id_oth, db_DEM_1, db_DEM_2, dt, bug)

if bug == 1:
    plt.imshow(db_DEM_1, origin="lower", cmap='Set1', interpolation='nearest')
    plt.gca().invert_yaxis()
    plt.colorbar()
    plt.show()
    
    plt.imshow(db_DEM_2, origin="lower", cmap='Set1', interpolation='nearest')
    plt.gca().invert_yaxis()
    plt.colorbar()
    plt.show()

print('Grass initial area : ' + str(hept0 * 5 * 5 * ((1 / 1000) ** 2) ))
print('-----------------------------------')
print('Parameter forest  to grass : ', str(hf2g))
print('Parameter harvest to grass : ', str(hh2g))
print('Parameter water   to grass : ', str(hw2g))
print('Parameter other   to grass : ', str(ho2g))
print('-----------------------------------')
print('Parameter grass to  forest : ', str(hg2f))
print('Parameter grass to harvest : ', str(hg2h))
print('Parameter grass to   water : ', str(hg2w))
print('Parameter grass to   other : ', str(hg2o))

