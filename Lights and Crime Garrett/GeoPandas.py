#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 17:55:50 2018

@author: Garrett
"""

#%% Packages

#%matplotlib inline #used for notebook

from __future__ import (absolute_import, division, print_function)
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('bmh')

from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from geopandas import GeoSeries, GeoDataFrame

#%% Data
Windows = 'C:/Users/Sade/Documents/GitHub/lights-and-crime/Lights and Crime Garrett/Data'
Linux = '/home/sade/Desktop/Git Cloned Repos/lights-and-crime/Lights and Crime Garrett/Data'

choice = Linux

Lights = pd.read_excel(choice + '/Lights.xlsx')
NCR = pd.read_excel(choice + '/NCR.xlsx')

geometry = [Point(xy) for xy in zip(Lights['gpsX'], Lights['gpsY'])]
gLights = GeoDataFrame(Lights, geometry=geometry)
geometry = [Point(xy) for xy in zip(NCR['gpsX'], NCR['gpsY'])]
gNCR = GeoDataFrame(NCR, geometry=geometry)

BUFFER = .00125 # Approximately half a city block in Maryland coordinates

gLights_Buff = gLights.assign(geometry = lambda x: x.geometry.buffer(BUFFER)) 
# Overwrites geometry variable with a buffer centered at the point of interest. A.k.a. applies the function geometry(x) to gNCR.

Matched_Lights = gpd.sjoin(gLights_Buff, gNCR, 'left')

Matched_Lights.to_excel(choice + '/Matched_Lights.xlsx')

#%% Plotting circles

x = []
y = []
for i in range(len(gLights_Buff['geometry'])):
    xc, yc = glights_Buff.loc[i, 'geometry'].exterior.coords.xy
    x.append(xc)
    y.append(yc)

plt.figure(1)
plt.scatter(x, y)

plt.figure(2)
plt.scatter(Lights['gpsX'], Lights['gpsY'])