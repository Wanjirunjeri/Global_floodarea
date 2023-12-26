# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 13:41:51 2023

@author: Njesh
"""


import xarray as xr
import pandas as pd
import numpy as np

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



def nc_read2(file):
    
    ds = xr.open_dataset(file,decode_times=False)
    return ds

ds = nc_read('orchidee_ipsl_rcp26_floodedarea_2006_2099.nc4',2006,94)
print(ds)

def calculate_and_mask(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim):
    da_rcp26, da_rcp85, grid_cell_areas, ipcc_regions = nc_read(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim)
    # Initialize dictionaries to store masked arrays for each region and scenario
     
    masked_flooded_area_rcp26 = {}
     
    masked_flooded_area_rcp85 = {}
     
     # Loop through each IPCC AR6 region
    for region_id in range(1, 45):  # Assuming region IDs range from 1 to 44...if IPCC regions are different i might need to adjust
        # Create a boolean mask for the current region
        region_mask = (ipcc_regions == region_id)
        
        region_flooded_area_rcp26 = da_rcp26.where(region_mask, other=0.0)
        region_flooded_area_rcp85 = da_rcp85.where(region_mask, other=0.0)

        # Store the masked arrays in dictionaries
        masked_flooded_area_rcp26[region_id] = region_flooded_area_rcp26
        masked_flooded_area_rcp85[region_id] = region_flooded_area_rcp85
  
     # Calculate flooded area (Km2)
    flooded_area_rcp26 = da_rcp26 * grid_cell_areas*10**-6
    flooded_area_rcp85 = da_rcp85 * grid_cell_areas*10**-6
   
    return masked_flooded_area_rcp26, masked_flooded_area_rcp85, flooded_area_rcp26, flooded_area_rcp85

def total_flooded_area(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim):
    masked_flooded_area_rcp26, masked_flooded_area_rcp85, flooded_area_rcp26, flooded_area_rcp85 = calculate_and_mask(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim)
    
    
    
Masked = calculate_and_mask('orchidee_ipsl_rcp26_floodedarea_2006_2099.nc4','orchidee_ipsl_rcp85_floodedarea_2006_2099.nc4','globe_grid_cell_areas.nc', 'ipcc_regions_regions_1_44.nc', 2006,94)
#print( ds)        
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     