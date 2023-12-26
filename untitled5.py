# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 14:04:22 2023

@author: Njesh
"""

import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import os


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

def calculate_and_mask(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim):
    da_rcp26, da_rcp85, grid_cell_areas, ipcc_regions = nc_read(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim)
    
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
       region_flooded_area_rcp26 = da_rcp26.where(region_mask, other=0.0)
       region_flooded_area_rcp85 = da_rcp85.where(region_mask, other=0.0)

       #region_flooded_area_value26 = flooded_area_
       # Store the masked arrays in dictionaries
       masked_flooded_area_rcp26[region_id] = region_flooded_area_rcp26
       masked_flooded_area_rcp85[region_id] = region_flooded_area_rcp85
 
    # Calculate flooded area (Km2)
       region_area={}
      #create a loop
       for key, floodarea_data in masked_flooded_area_rcp26.items():
           mask = floodarea_data == key
           
           C = xr.where(mask, region_flooded_area_rcp26, 0)
           region_area[key] = C
          
    
    
       return region_area, masked_flooded_area_rcp26, masked_flooded_area_rcp85, flooded_area_rcp26, flooded_area_rcp85

"""
def total_flooded_area(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim):
    #calculate_and_mask('orchidee_ipsl_rcp26_floodedarea_2006_2099.nc4','orchidee_ipsl_rcp85_floodedarea_2006_2099.nc4','globe_grid_cell_areas.nc', 'ipcc_regions_1_44.nc', 2006,94)
    masked_flooded_area_rcp26, masked_flooded_area_rcp85, flooded_area_rcp26, flooded_area_rcp85 = calculate_and_mask(file_rcp26, file_rcp85, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim)

    mask26 = pd.DataFrame.from_dict(masked_flooded_area_rcp26)
    mask85 = pd.DataFrame.from_dict(masked_flooded_area_rcp85)
    maskarea = [mask26,mask85]
   
    # Convert xarray dataset to pandas DataFrame
    flood_area26 = flooded_area_rcp26.to_dataframe().reset_index()
    flood_area85 = flooded_area_rcp85.to_dataframe().reset_index()
    data_df = [data1, data2] 
    # Create Excel writer object
    excel_writer = pd.ExcelWriter('flooded_area_results.xlsx', engine='openpyxl')
    
    # Iterate over RCP scenarios
    for rcp_scenario in maskarea.unique():
        rcp_data = data_df[data_df['RCP'] == rcp_scenario]
    
        # Create a pivot table to get the total flooded area per region per year
        pivot_table = pd.pivot_table(rcp_data, values='FloodedArea', index='Year', columns='Region', aggfunc='sum', fill_value=0)
    
        # Write the pivot table to Excel sheet
        pivot_table.to_excel(excel_writer, sheet_name=f'Sheet_{rcp_scenario}', index=True)
    
    # Save the Excel file
    excel_writer.save()
    df = pd.read_excel('flooded_area_results.xlsx', sheet_name='Sheet_RCP2.6')
    print(df)
    return df
"""   
reg_area,masked_rcp26, masked_rcp85, flood_area_rcp26, flood_area_rcp85 = calculate_and_mask('orchidee_ipsl_rcp26_floodedarea_2006_2099.nc4','orchidee_ipsl_rcp85_floodedarea_2006_2099.nc4','globe_grid_cell_areas.nc', 'ipcc_regions_1_44.nc', 2006,94)

#mask26 = pd.DataFrame.from_dict(masked_rcp26, index = 'False', columns = ) 
#print(type(mask26))
#flood_area26 = flooded_area_rcp26.to_dataframe()

#new = flood_area_rcp26.to_dataframe()
#print(new)      

