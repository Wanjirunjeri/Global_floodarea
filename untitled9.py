# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 14:03:35 2023

@author: Njesh
"""

# Convert xarray dataset to pandas DataFrame
data1 = masked_flooded_area_rcp26.to_dataframe().reset_index()
data2 = masked_flooded_area_rcp85.to_dataframe().reset_index()
data_df = [data1, data2] 
# Create Excel writer object
excel_writer = pd.ExcelWriter('P:\Environmental programming\Derrick\Topic6_Derrick_Global_Annual_River_Flooded_Area\Supporting_script\flooded_area_results.xlsx', engine='openpyxl')

# Iterate over RCP scenarios
for rcp_scenario in data_df.unique():
    rcp_data = data_df[data_df['RCP'] == rcp_scenario]

    # Create a pivot table to get the total flooded area per region per year
    pivot_table = pd.pivot_table(rcp_data, values='FloodedArea', index='Year', columns='Region', aggfunc='sum', fill_value=0)

    # Write the pivot table to Excel sheet
    pivot_table.to_excel(excel_writer, sheet_name=f'Sheet_{rcp_scenario}', index=True)

# Save the Excel file
excel_writer.save()
