# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 11:02:55 2018

@author: crhuffer

Process the data from the streaming API after it has been saved to .csv files
based on the type of event.
"""

# %% library imports

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import PlayerActivity

# %% Setup path and filename variables

path_CSVData = "../Machine/Data/"
path_Resources = "../GameUtilitiesResources/"
filename_GainedExp = path_CSVData + 'GainedExp.dat'
filename_FacilityDefends = path_CSVData + 'FacilityDefends.dat'


filename_OutfitID = path_Resources + 'OutfitID.txt'

# %% Loading outfit information

OutfitID = PlayerActivity.get_outfit_id()

# %% Load the experience data

#df_GainedExp = pd.read_csv(filename_GainedExp, sep = '\t')
list_Columns = ['Code', 'zone_id', 'outfit_id', 'character_id', 'timestamp',
                'facility_id', 'world_id']
df_FacilityDefends = pd.read_csv(filename_FacilityDefends, sep = '\t',
                                 names=list_Columns)

# %%

df_FacilityDefends.describe()

# %% Top players for defending zones

df_FacilityDefends['character_id'].value_counts().head(10)


# %%
