# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 15:52:21 2023

@author: Njesh
"""
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime as datetime
import openpyxl


# Get the current working directory
current_directory = os.getcwd()

# Print the current working directory
print("Current Working Directory:", current_directory)

# Function for reading NetCDF4 data 
def nc_read(file_rcp26, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim):
   
    # Read RCP2.6 data
    ds_rcp26 = xr.open_dataset(file_rcp26, decode_times=False)
    da_rcp26 = ds_rcp26['exposure']
    
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
    
    return  da_rcp26, grid_cell_areas, ipcc_regions

def calculate_and_mask(file_rcp26, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim):
    da_rcp26, grid_cell_areas, ipcc_regions = nc_read(file_rcp26,file_grid_cell_areas, file_ipcc_regions, start_year, time_dim)
    
    # Calculate flooded area (Km2)
    flooded_area_rcp26 = da_rcp26 * grid_cell_areas*10**-6

    
   # Initialize dictionaries to store masked arrays for each region and scenario
    masked_flooded_area_rcp26 = {}

   # Loop through each IPCC AR6 region
    for region_id in range(1, 45):  # Assuming region IDs range from 1 to 44...if IPCC regions are different i might need to adjust
       # Create a boolean mask for the current region
       region_mask = (ipcc_regions == region_id)

       # Apply the mask to the flooded area for both scenarios
       region_flooded_area_rcp26 = da_rcp26.where(region_mask, 0.0)

       #region_flooded_area_value26 = flooded_area_
       # Store the masked arrays in dictionaries
       masked_flooded_area_rcp26[region_id] = region_flooded_area_rcp26
       
       # Calculate flooded area (Km2)
    flooded_area_rcp26 = da_rcp26 * grid_cell_areas*10**-6
     
    return masked_flooded_area_rcp26, flooded_area_rcp26

Sheet_name = 'RCP8.5' #input('Please input the RCP scenario: ')


def total_flooded_area(file_rcp26, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim):
    masked_flooded_area_rcp26, flooded_area_rcp26 = calculate_and_mask(file_rcp26, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim)
    
    region_area={}
    
    for key, flooded in masked_flooded_area_rcp26.items():
        mask = (flooded == key)
           
        C = xr.where(mask, flooded_area_rcp26, 0)
        region_area[key] = C
    #create a dictionary to store the summed area values #for every value per key sum up all the flooded area    
    sum_area = {}
    sum_area['year']= flooded_area_rcp26['time'].dt.year
    for key, sumarea_data in region_area.items():
           #for time in sumarea_data:
               # Sum the data values along the time dimension
        summed_values = sumarea_data.groupby('time').sum(dim=['lat', 'lon'])
        new_data_array = xr.DataArray(summed_values, dims=['time'], coords={'time':sumarea_data['time']})
        sum_area[key]= new_data_array
    
    sum_df = pd.DataFrame(sum_area) 
    print(sum_df)
    
    return sum_df


def append_to_excel(dataframe, sheet_name, excel_file):
    ###dataframe = total_flooded_area(file_rcp26, file_grid_cell_areas, file_ipcc_regions, start_year, time_dim)
    # Open the Excel file in append mode
    ###excel_file = 'flooded_area_results.xlsx'
    with pd.ExcelWriter(excel_file, mode='a', engine='openpyxl') as writer:
        # Write the DataFrame to a new sheet
        dataframe.to_excel(writer, sheet_name, index=False)
 
def cumulative_area():
    file = 'flooded_area_results.xlsx'
    flooded_area26 = pd.read_excel(os.path.join(current_directory,file),sheet_name = 'RCP2.6')
    flooded_area85 = pd.read_excel(os.path.join(current_directory,file),sheet_name = 'RCP8.5')
    print(flooded_area85)
    excell = pd.ExcelFile(os.path.join(current_directory,file))
    print(excell)                      
    #create a list of the sheets
    flad = [flooded_area26,flooded_area85]
    
    with pd.ExcelWriter(os.path.join(current_directory, 'cumulative_flooded_area_.xlsx'), engine='openpyxl') as writer:
        pd.DataFrame().to_excel(writer, sheet_name='DummySheet', index=False)
        #loop over the sheets
        
        
        for i, data in enumerate(flad, start=1):
            sheet_name = f'Sheet{i}'  # Sheet names will be Sheet1, Sheet2, ...
            

        #for data in flad:
            i = 0
            sheet = excell.sheet_names[i]
            #If your column has a different name, replace 'Year' with the actual column name
            year_column = data['year'] 
            
                       
            # Create a new column 'Decade' representing the starting year of each decade
            data['Decade'] = ((year_column - 2010) // 10) * 10 + 2010
            
            # Exclude years before 2010
            dat = data[data['year'] > 2010]
            #dat['DecadeLabel'] = dat['Decade'].astype(str) + '-' + (dat['Decade'] + 9).astype(str)

            # Group by 'Decade' and sum the corresponding values in each column
            result_df = dat.groupby('Decade').sum()
            
            # Now, result_df contains the summed values for each column grouped by decades
            # You can save the result DataFrame back to Excel if needed
            #result_df.to_excel(os.path.join(current_directory, 'umulative_flooded_area_.xlsx'),sheet_name = sheet)
            #result_df[0] = dat['DecadeLabel'] 
            
            
            result_df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(result_df)
#cumulative_area()

def average_flooded_area():
    file = 'flooded_area_results.xlsx'
    flooded_area26 = pd.read_excel(os.path.join(current_directory,file),sheet_name = 'RCP2.6')
    flooded_area85 = pd.read_excel(os.path.join(current_directory,file),sheet_name = 'RCP8.5')
    
    # Filter data for the years 2070 to 2099
    df_filtered26 = flooded_area26[(flooded_area26['year'] >= 2070) & (flooded_area26['year'] <= 2099)]
    df_filtered85 = flooded_area85[(flooded_area85['year'] >= 2070) & (flooded_area85['year'] <= 2099)]
    
    # Identify the columns containing flooded area data (assuming they are numeric)
    flooded_area_columns26 = df_filtered26.columns[1:]  # Exclude the 'Year' column
    flooded_area_columns85 = df_filtered26.columns[1:]  # Exclude the 'Year' column

    
    
    # Calculate the average flooded area for each region (excluding non-numeric columns)
    average_per_region26 = df_filtered26[flooded_area_columns26].mean(numeric_only=True)
    average_per_region85 = df_filtered85[flooded_area_columns85].mean(numeric_only=True)

    
    # Create a new DataFrame with region names and mean values
    result_df26 = pd.DataFrame({'Region': average_per_region26.index, 'Mean_Flooded_Area': average_per_region26.values})
    result_df85 = pd.DataFrame({'Region': average_per_region85.index, 'Mean_Flooded_Area': average_per_region85.values})

    
    # Print or use the result DataFrame as needed
    print(result_df26)

#average_flooded_area()

def annual_flooded_area_timeseries_graph():
    file = 'flooded_area_results.xlsx'
    flooded_area26 = pd.read_excel(os.path.join(current_directory,file),sheet_name = 'RCP2.6')
    flooded_area85 = pd.read_excel(os.path.join(current_directory,file),sheet_name = 'RCP8.5')
    
    # Get user input for the desired region
    desired = input("Enter the desired region: ")
    desired_region = int(desired)
    # Plot timeseries of annual flooded area for the specified region
    plt.figure(figsize=(10, 6))
    
    # Plot for RCP2.6
    if desired_region in flooded_area26.columns:
        plt.plot(flooded_area26['year'], flooded_area26[desired_region], label=f'RCP2.6 - {desired_region}', linestyle='-', marker='o')
    else:
        print(f"The specified region '{desired_region}' is not found in RCP2.6 data.")
    
    # Plot for RCP8.5
    if desired_region in flooded_area85.columns:
        plt.plot(flooded_area85['year'], flooded_area85[desired_region], label=f'RCP8.5 - {desired_region}', linestyle='--', marker='o')
    else:
        print(f"The specified region '{desired_region}' is not found in RCP8.5 data.")
    
    plt.xlabel('Year')
    plt.ylabel('Annual Flooded Area (km2)')
    plt.title(f'Timeseries of Annual Flooded Area for {desired_region}')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(flooded_area26[3])
#annual_flooded_area_timeseries_graph()

def bargraph():
    # Load data from Excel file
    excel_file = 'cumulative_flooded_area_.xlsx'
    df = pd.read_excel(excel_file, sheet_name=None)
    print (df)
    desired_region = input("Enter the desired region: ")
    region = int(desired_region)
    # Create a bar graph for each sheet (RCP2.6 and RCP8.5)
    for sheet_name, data in df.items():
        # Group data by decade and sum the cumulative flooded area
        #grouped_data = data['year']
    
        # Plot the bar graph
        plt.bar(data['year'],data[region], label=sheet_name)
    
    # Customize the plot
    plt.xlabel('Decade')
    plt.ylabel('Cumulative Flooded Area')
    plt.title('Cumulative Flooded Area per Decade for RCP2.6 and RCP8.5')
    plt.legend()
    plt.grid(True)
    
    # Show the plot
    plt.show()

       
#Masked , floods = calculate_and_mask('orchidee_ipsl_rcp26_floodedarea_2006_2099.nc4','globe_grid_cell_areas.nc', 'ipcc_regions_1_44.nc', 2006,94)
#print( ds)    