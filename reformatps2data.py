# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 10:33:09 2018

@author: crhuffer
"""

import pandas as pd
import numpy as np
import PlayerActivity as apiutilities

# %% Load dictionaries with the IDs

filename = '../MachineResources/LoadoutID.csv'
df_LoadoutID = pd.read_csv(filename, names=['loadout_id', 'code_name'])
df_LoadoutID = df_LoadoutID.append({'loadout_id': 0, 'code_name': 'None'},
                                   ignore_index=True)
df_LoadoutID.index = df_LoadoutID['loadout_id']
df_LoadoutID.dropna(inplace=True)

filename = '../MachineResources/VehicleID.csv'
df_VehicleID = pd.read_csv(filename, names=['vehicle_id', 'name'])
df_VehicleID = df_VehicleID.append({'vehicle_id': 0, 'name': 'None'},
                                   ignore_index=True)
df_VehicleID.index = df_VehicleID['vehicle_id']
df_VehicleID.dropna(inplace=True)

filename = '../MachineResources/ZoneID.csv'
df_ZoneID = pd.read_csv(filename, names=['zone_id', 'code'])
df_ZoneID.index = df_ZoneID['zone_id']
df_ZoneID.dropna(inplace=True)

filename = '../MachineResources/ExperienceID.csv'
df_ExperienceID = pd.read_csv(filename, names=['experience_id', 'description'])
df_ExperienceID.index = df_ExperienceID['experience_id']
df_ExperienceID.dropna(inplace=True)


# %% Testing loading the data in to a dataframe

filename = '../Machine/Data/KilledPlayer.dat'
Columns = ['type', 'character_id', 'a_fire_mode_id', 'a_loadout_id',
           'a_vehicle_id', 'a_weapon_id', 'is_headshot', 'timestamp',
           'world_id', 'zone_id', 'attacker_character_id']
df_KilledPlayer = pd.read_csv(filename, sep='\t', names=Columns)

df_KilledPlayer.astype(float, inplace=True, errors='ignore')

df_KilledPlayer['a_vehicle_id'] = df_KilledPlayer['a_vehicle_id'].apply(
        lambda x: df_VehicleID.loc[x, 'name'])
df_KilledPlayer['a_vehicle_id'].value_counts()

df_KilledPlayer['a_loadout_id'] = df_KilledPlayer['a_loadout_id'].apply(
        lambda x: df_LoadoutID.loc[x, 'code_name'])
df_KilledPlayer['a_loadout_id'].value_counts()


# %% Mapping the zoneIDs
# This didn't work there are a bunch of zones in the data that don't exist on
# the api.
# df_KilledPlayer['zone_id'] = df_KilledPlayer['zone_id'].apply(
#        lambda x: df_ZoneID.loc[x, 'code'])
# df_KilledPlayer['zone_id'].value_counts()

df_KilledPlayer['zone_id'].replace({98: 'VR training VS', 96: 'VR training NC',
                                    97: 'VR training TR', 2: 'Indar',
                                    4: 'Hossin', 6: 'Amerish',
                                    8: 'Esamir'}, inplace=True)

# df_KilledPlayer['a_vehicle_id'].isnull().sum()
# %%

filename = '../Machine/Data/GainedExp.dat'
Columns = ['type', 'experience_id', 'amount', 'timestamp', 'loadout_id',
           'world_id', 'zone_id', 'other_id']
df_GainedExp = pd.read_csv(filename, sep='\t', names=Columns)

df_GainedExp.astype(float, inplace=True, errors='ignore')

df_GainedExp['a_loadout_id'] = df_GainedExp['a_loadout_id'].apply(
        lambda x: df_LoadoutID.loc[x, 'code_name'])
df_GainedExp['a_loadout_id'].value_counts()

#df_GainedExp['experience_id'] = df_GainedExp['experience_id'].apply(
#        lambda x: df_ExperienceID.loc[x, 'description'])

## FIXME: improve logic using an indexer and the dataframe instead of todict
df_GainedExp['experience_id'].replace(df_ExperienceID['description'].to_dict(),
            inplace=True)
df_GainedExp['experience_id'].value_counts()
df_GainedExp['experience_id'].nunique()




df_GainedExp['zone_id'].replace({98: 'VR training VS', 96: 'VR training NC',
                                    97: 'VR training TR', 2: 'Indar',
                                    4: 'Hossin', 6: 'Amerish',
                                    8: 'Esamir'}, inplace=True)

# %%


df_KilledPlayer.dtypes

# %% Getting the outfit member names and IDs

OutfitID = apiutilities.get_outfit_id()
UserName = apiutilities.get_user_id()
df_OutfitMembers = apiutilities.get_outfit_member_list(OutfitID, UserName)
df_OutfitMembers = apiutilities.get_members_last_login(df_OutfitMembers)

# %% Cleanup the outfit members dataframe before merging

dict_ColumnTypes = {}

Columns = ['character_id', 'member_since', 'rank_ordinal']
Type = np.int64
for column in Columns:
    dict_ColumnTypes[column] = Type
#df_OutfitMembers[Columns].astype(np.int64)

Columns = ['rank', 'name']
Type = str
for column in Columns:
    dict_ColumnTypes[column] = Type
#df_OutfitMembers[Columns].astype(str)

Columns = ['member_since_date', 'last_login_date']
Type = pd.datetime
for column in Columns:
    dict_ColumnTypes[column] = Type
#df_OutfitMembers[Columns].astype(pd.datetime)

df_OutfitMembers = df_OutfitMembers.astype(dict_ColumnTypes)

# %% Merge on the outfit members

df_OutfitKilledPlayer = df_OutfitMembers.merge(df_KilledPlayer, how='right',
                                              on='character_id')

# %%

indexer = df_OutfitKilledPlayer['name'].notnull()


# %%

df_OutfitKilledPlayer_MembersOnly = df_OutfitKilledPlayer.loc[indexer, :]

# %%

df_OutfitMembers.dtypes

# %%

df_KilledPlayer.dtypes