# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 18:57:25 2023

@author: hp
"""

import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

# Function for reading NetCDF4 data 
def nc_read(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim):
   
    # Read RCP2.6 data
    ds_rcp26 = xr.open_dataset(file_rcp26, decode_times=False)
    da_rcp26 = ds_rcp26['exposure']
    
    # Read RCP8.5 data
    ds_rcp85 = xr.open_dataset(file_rcp85, decode_times=False)
    da_rcp85 = ds_rcp85['exposure']
    
    # Read global grid cell areas
    ds_grid_cell_areas = xr.open_dataset(file_grid_cell_areas, decode_times=False)
    grid_cell_areas = ds_grid_cell_areas['cell_area'] 
    
    # Read IPCC AR6 regions
    ds_ipcc_regions = xr.open_dataset(file_ipcc_regions, decode_times=False)
    ipcc_regions = ds_ipcc_regions['ids']  
    
    if time_dim:
# Manually decode times from integer to datetime series using the specified 'start_year'
        new_dates = pd.date_range(start=str(start_year)+'-1-1', periods=da_rcp26.sizes['time'], freq='YS')
        da_rcp26['time'] = new_dates
    # Update time for the first file
    if time_dim:
        new_dates1 = pd.date_range(start=str(start_year)+'-1-1', periods=da_rcp85.sizes['time'], freq='YS')
        da_rcp85['time'] = new_dates1

    
    return  da_rcp26, da_rcp85, grid_cell_areas, ipcc_regions

def calculate_and_mask(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim):
    da_rcp26, da_rcp85, grid_cell_areas, ipcc_regions = nc_read(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim)
    
   # Initialize dictionaries to store masked arrays for each region and scenario
    masked_flooded_area_rcp26 = {}
    masked_flooded_area_rcp85 = {}

   # Loop through each IPCC AR6 region
    for region_id in range(1, 45):  # Assuming region IDs range from 1 to 44...if IPCC regions are different i might need to adjust
       # Create a boolean mask for the current region
       region_mask = (ipcc_regions == region_id)

       # Apply the mask to the flooded area for both scenarios
       region_flooded_area_rcp26 = da_rcp26.where(region_mask, other=0.0)
       region_flooded_area_rcp85 = da_rcp85.where(region_mask, other=0.0)

       # Store the masked arrays in dictionaries
       masked_flooded_area_rcp26[region_id] = region_flooded_area_rcp26
       masked_flooded_area_rcp85[region_id] = region_flooded_area_rcp85
 
    # Calculate flooded area (Km2)
    flooded_area_rcp26 = da_rcp26 * grid_cell_areas*10**-6
    flooded_area_rcp85 = da_rcp85 * grid_cell_areas*10**-6
  
    return masked_flooded_area_rcp26, masked_flooded_area_rcp85, flooded_area_rcp26, flooded_area_rcp85

new = calculate_and_mask('orchidee_ipsl_rcp26_floodedarea_2006_2099.nc4','orchidee_ipsl_rcp85_floodedarea_2006_2099.nc4','globe_grid_cell_areas.nc', 'ipcc_regions_regions_1_44.nc', 2006,94)
         
    

