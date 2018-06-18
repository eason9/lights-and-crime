# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 13:25:12 2018

@author: Sade
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import urllib
import os

#%% Importing and Setting Up Fail Code Data

# Fail codes df and pulling out relevant light out codes:
fc = pd.read_excel('C:/Users/Sade/Desktop/Lights/Data/islims_failure_codes.xlsx')
important_lights_out_fcs = [2, 196, 201, 209]

# Work order df and filtered wo df by relevant fail codes:
wo = pd.read_excel('C:/Users/Sade/Desktop/Lights/Data/islims_workorders.xlsx')
wo_filteredby_fc = wo['finalresolutionID'].isin(important_lights_out_fcs)
wo[wo_filteredby_fc]['finalresolutionID'].value_counts()

# Filtering out data without an asset id, dates outside interest time, and fail codes that are not of immediate interest:
f1 = wo_filteredby_fc
f2 = wo['srchAssetID'] != '-???-'
f3 = (wo['resolveddatetime'] > '2007-12-31') & (wo['resolveddatetime'] < '2017-01-01') 
f4 = (wo['entereddate'] > '2007-12-31') & (wo['entereddate'] < '2017-01-01') 
fil = f1 & f2 & f3 & f4 
wo_fil = wo[fil]

# As Don stated we are losing approximately 15.6% of data due to missing asset ids:
1 - len(wo_fil)/len(wo[f1 & f3 & f4])

#%% Open Data Work Orders

inv = pd.read_excel('C:/Users/Sade/Desktop/Lights/Data/islims_inventory.xlsx')

if os.path.isfile('C:/Users/Sade/Desktop/Lights/Data/Cityworks_Workorders.geojson'):
    odwo = gpd.read_file('C:/Users/Sade/Desktop/Lights/Data/Cityworks_Workorders.geojson')
else:
    urllib.request.urlretrieve ('https://opendata.arcgis.com/datasets/a1dd480eb86445239c8129056ab05ade_0.geojson', 'C:/Users/Sade/Desktop/Lights/Data/Cityworks_Workorders.geojson')
    odwo = gpd.read_file('C:/Users/Sade/Desktop/Lights/Data/Cityworks_Workorders.geojson')

descriptions = pd.Series(odwo['DESCRIPTION'].unique())
dmask = descriptions.str.contains('LIGHT')
dlist = descriptions[dmask].tolist()

mask = odwo.DESCRIPTION.isin(dlist)
odwo[mask].DESCRIPTION.value_counts()

mask = odwo.DESCRIPTION.isin(['LIGHT MALFUNCTION', 'LIGHT POLE LIGHT OUT'])