# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 15:39:36 2023

@author: dmuheki
"""


import xarray as xr
import pandas as pd
import numpy as np
import os

current_directory = os.getcwd()

#%% Function for reading NetCDF4 data 
def nc_read(file, start_year, time_dim):
    
    """ Reading netcdfs based on occurrence variable: here 'exposure'
    
    Parameters
    ----------
    file : files in data directory (string)
    start_year: (int)
    
    Returns
    ------- 
    Xarray data array
    """
    # initiate as xarray dataset 
    ds = xr.open_dataset(file,decode_times=False)
    
    # convert to xarray data array for target variable
    da = ds['exposure']
   
    if time_dim:
        # manually decode times from integer to datetime series using the 'Start year' derived from the function read_start_year above
        new_dates = pd.date_range(start=str(start_year)+'-1-1', periods=da.sizes['time'], freq='YS')
        da['time'] = new_dates
    
    return da

#df= pd.DataFrame(da)

def nc_read2(file,start_year):
    
    """ Reading netcdfs based on occurrence variable: here 'ids'
    
    """
    # initiate as xarray dataset 
    ds = xr.open_dataset(file,decode_times=False)
    
    # convert to xarray data array for target variable
    
    da = ds['ids']
   
      
    return da

def nc_read3(file,start_year):
    
    """ Reading netcdfs based on occurrence variable: here 'ids'
    
    """
    # initiate as xarray dataset 
    ds = xr.open_dataset(file,decode_times=False)
    
    # convert to xarray data array for target variable
    
    da = ds['cell_area']
   
      
    return da















