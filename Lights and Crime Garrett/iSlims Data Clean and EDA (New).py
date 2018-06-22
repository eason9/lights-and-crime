# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 10:53:03 2018

@author: Garrett
"""

#%% Merging and Cleaning iSLims data

# Packages
import pandas as pd
import matplotlib.pyplot as plt

#%% Data

wo = pd.read_excel('C:/Users/Sade/Documents/GitHub/lights-and-crime/Lights and Crime Garrett/Data/islims_workorders.xlsx')
de = pd.read_excel('C:/Users/Sade/Documents/GitHub/lights-and-crime/Lights and Crime Garrett/Data/islims_workorders_detail.xlsx')
iv = pd.read_excel('C:/Users/Sade/Documents/GitHub/lights-and-crime/Lights and Crime Garrett/Data/islims_inventory.xlsx')
fc = pd.read_excel('C:/Users/Sade/Documents/GitHub/lights-and-crime/Lights and Crime Garrett/Data/islims_failure_codes.xlsx')

#%% Merging and Cleaning Data

# Merging work order and details sets on woID
wode = pd.merge(wo, de, on='woID')

# Merging wode and inventory sets on inventoryID
iSlimsa = pd.merge(wode, iv, on='inventoryID')

# Merging the GPS coordinates to fill in as many NaN gaps as possible
gpsX = iSlimsa['gpscoordinateX_x'].combine_first(iSlimsa['gpscoordinateX_y'])
gpsX = gpsX.combine_first(iSlimsa['gpscoordinateX_x'])
gpsY = iSlimsa['gpscoordinateY_x'].combine_first(iSlimsa['gpscoordinateY_y'])
gpsY = gpsY.combine_first(iSlimsa['gpscoordinateY_x'])

# Removing irrelevant variables
iSlimsb = iSlimsa.iloc[:,0:18]
iSlimsb['gpsX'] = gpsX
iSlimsb['gpsY'] = gpsY

# final merged dataset
iSlimsc = iSlimsb.drop(['gpscoordinateX_x', 'gpscoordinateY_x'], axis = 1)

# Throwing out observations without GPS coordinate
iSlimsd = iSlimsc.dropna(subset = ['gpsX', 'gpsY'])

# Will use codes: 2, 196, 201, 209
fc[fc['description'].str.contains('ight')].head()

# Filtering by observations with the desired failure codes
iSlimse = iSlimsd[iSlimsd['finalresolutionID'].isin([2, 196, 201, 209])]

# Filtering by times of interest
resolv_t = (iSlimse['resolveddatetime'] > '2007-12-31') & (iSlimse['resolveddatetime'] < '2017-01-01') 
enter_t = (iSlimse['entereddate_x'] > '2007-12-31') & (iSlimse['entereddate_x'] < '2017-01-01')
iSlimsf = iSlimse[resolv_t & enter_t]

# Filtering out observations with excessively long completion / late completion times
iSlimsg = iSlimsf[(iSlimsf['daysToComplete'] <= 23)]
iSlimsg['finalresolutionID'].value_counts()

# Dropping duplicate woID's
iSlimsh = iSlimsg.drop_duplicates(subset = ['woID'])

# Throwing out observations with a GPS coordinate that is too large in magnitude to be possible
iSlimsh[['gpsX', 'gpsY']] = iSlimsh[['gpsX', 'gpsY']].apply(pd.to_numeric)
iSlims = iSlimsh[iSlimsh['gpsX'] <= 20000 ]
iSlims = iSlims[iSlims['gpsY']<= 20000]

# Removing 2 observations whos GPS coordinates were entered incorrectly and limiting bounds of GPS coordinates to realistic numbers in the bounds of DC
iSlims = iSlims.drop([465076, 144970])
iSlims = iSlims[(iSlims['gpsX'] >= 38.7) & (iSlims['gpsX'] <= 39) ]
iSlims = iSlims[(iSlims['gpsY'] >= -77.15) & (iSlims['gpsY'] <= -76.90)]
# Cutting out close outliers
iSlims = iSlims[~((iSlims['gpsX'] >= 38.828) & (iSlims['gpsX'] <= 38.8395) & (iSlims['gpsY'] <= -76.9632) & (iSlims['gpsY'] >= -76.9777))]
iSlims = iSlims[~((iSlims['gpsX'] >= 38.955) & (iSlims['gpsX'] <= 38.96) & (iSlims['gpsY'] >= -76.98) & (iSlims['gpsY'] <= -76.97))]


#%% To Excel

iSlims.to_excel('C:/Users/Sade/Documents/GitHub/lights-and-crime/Lights and Crime Garrett/Data/iSlims_final.xlsx')

#%% EDA

# Summary Statistics and histogram on completion days
iSlims[['daysToComplete', 'daysLate']].describe()
# on average it takes 2 days to complete a task and the completion tasks are rarely late (excluding completion tasks beyond 14 days).
plt.hist(iSlims['daysToComplete'], bins = 23)
# Something to note: this data closely resembels a Poisson distribution for count data.  Could do a GLM to predict what contributes to repair time.
# Also Interesting jump at 14ish days and predictible drop after 5ish days.

# Scatter of GPS coordinates
plt.scatter(iSlims['gpsX'], iSlims['gpsY'])
# No obvious problem areas
# Could also filter by Completion time and Late time, no obvious problem areas there either

#%% Play


