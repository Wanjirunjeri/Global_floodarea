# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:06:08 2023

@author: Njesh
"""

import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import supporting_scriptmodified as sp
import os

march = sp.nc_read('orchidee_ipsl_rcp26_floodedarea_2006_2099.nc4', 2006, 94)

april = sp.nc_read('orchidee_ipsl_rcp85_floodedarea_2006_2099.nc4', 2006, 94)

may = sp.nc_read2('ipcc_regions_1_44.nc',2006)

june = sp.nc_read3('globe_grid_cell_areas.nc',2010)