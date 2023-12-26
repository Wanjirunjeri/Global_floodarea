# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 14:37:54 2023

@author: Njesh
"""

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import xarray as xr

airtemps = xr.tutorial.open_dataset("air_temperature")

airtemps

air = airtemps.air - 273.15

air.attrs = airtemps.air.attrs

air.attrs["units"] = "deg C"

air1d = air.isel(lat=10, lon=10)

air1d.plot()

air2d = air.isel(time=500)

air2d.plot()