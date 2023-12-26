# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 15:05:42 2023

@author: Njesh
"""

import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime as datetime


# Get the current working directory
current_directory = os.getcwd()

# Print the current working directory
print("Current Working Directory:", current_directory)

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

Sheet_name = input('Please input the RCP scenario: ')

def calculate_and_mask(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim):
    da_rcp26, da_rcp85, grid_cell_areas, ipcc_regions = nc_read(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim)
    
    #pdb.set_trace()  # Add this line for debugging
    
    flooded_area_rcp26 = da_rcp26 * grid_cell_areas*10**-6
    flooded_area_rcp85 = da_rcp85 * grid_cell_areas*10**-6
    
   # Initialize dictionaries to store masked arrays for each region and scenario
    masked_flooded_area_rcp26 = {}
    masked_flooded_area_rcp85 = {}

   # Loop through each IPCC AR6 region
    for region_id in range(1, 45):  # Assuming region IDs range from 1 to 44...if IPCC regions are different i might need to adjust
       # Create a boolean mask for the current region
       region_mask = (ipcc_regions == region_id)

       # Apply the mask to the flooded area for both scenarios
       region_flooded_area_rcp26 = da_rcp26.where(region_mask, 0.0)
       region_flooded_area_rcp85 = da_rcp85.where(region_mask, 0.0)

       #region_flooded_area_value26 = flooded_area_
       # Store the masked arrays in dictionaries
       masked_flooded_area_rcp26[region_id] = region_flooded_area_rcp26
       masked_flooded_area_rcp85[region_id] = region_flooded_area_rcp85
       
    region_area={}
    
    for key, floodarea_data in masked_flooded_area_rcp85.items():
        #floodarea_data = flooded.groupby('time')
        mask = (floodarea_data == key)
           
        C = xr.where(mask, flooded_area_rcp85, 0) #this line is edited
        region_area[key] = C
    #create a dictionary to store the summed area values #for every value per key sum up all the flooded area    
    sum_area = {}
    sum_area['year']= flooded_area_rcp85['time'].dt.year
    for key, sumarea_data in region_area.items():
           #for time in sumarea_data:
               # Sum the data values along the time dimension
        summed_values = sumarea_data.groupby('time').sum(dim=['lat', 'lon'])
        new_data_array = xr.DataArray(summed_values, dims=['time'], coords={'time':sumarea_data['time']})
        sum_area[key]= new_data_array
    
    sum_df = pd.DataFrame(sum_area) 
    print(sum_df)
    # Create a Pandas Excel writer using XlsxWriter as the engine
    #writer = pd.ExcelWriter('flooded_area_results.xlxs')
    excel = sum_df.append_to_excel('flooded_area_results.xlsx',sheet_name = Sheet_name ,index = True) 
    #excel.loc[0, 'Index'] = 'New Value'
    #,engine = 'openpyxl' ,sheet_name= 'RCP2.6'
    # Convert the dataframe to an XlsxWriter Excel object
    #excel = sum_df.to_excel(writer, sheet_name='Sheet1')
    # Save the Excel file
    #excel.save()
    return sum_area



Masked = calculate_and_mask('orchidee_ipsl_rcp26_floodedarea_2006_2099.nc4','orchidee_ipsl_rcp85_floodedarea_2006_2099.nc4','globe_grid_cell_areas.nc', 'ipcc_regions_1_44.nc', 2006,94)



