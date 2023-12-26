# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 13:49:44 2023

@author: Njesh
"""

import xarray as xr
import pandas as pd
import numpy as np
import os
import supporting_scriptmodified as sp

current_directory = os.getcwd()

april = xr.open_dataset('orchidee_ipsl_rcp26_floodedarea_2006_2099.nc4')
may = sp.nc_read2('ipcc_regions_1_44.nc',2006)
june = sp.nc_read3('globe_grid_cell_areas.nc',2006)


summed_values = april['exposure'].groupby('time').sum(dim=['lon','lat'])
#sem = summed_values.to_pandas()#.resetindex()

#summ=summed_values.to_dataframe()
new_data_array = xr.DataArray(summed_values, dims=['time'], coords={'time':april['time']})
#sum_area[key]= new_data_array
summ=new_data_array.to_dataframe()
summ['time', 'exposure'] = summ['exposure'].astype(str).str.split('   ',expand = True)


# Assuming 'df' is your pandas DataFrame
header = list(summ.columns)
""" 
sum_area = []
for key in april:
       #for time in sumarea_data:
           # Sum the data values along the time dimension
    summed_values = april['exposure'].groupby('time').sum(dim=['time'])
    new_data_array = xr.DataArray(summed_values, dims=['time'], coords={'time':june['time']})
    sum_area[key]= new_data_array
summed_values = june.sum(dim=['lat', 'lon'])
"""
