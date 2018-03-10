# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:12:54 2018

@author: crhuffer

Loads data from the daybreak API about an outfit and saves the data into
a dataframe.
"""

# %% imports

import pandas as pd
import json
import requests
import datetime
import math

# %% Path and filename definitions

path_UserInformation = "../GameUtilitiesResources/"

filename_UserID = path_UserInformation + "APIUserName.txt"
filename_OutfitName = path_UserInformation + "OutfitName.txt"

filename_OutfitID = path_UserInformation + "OutfitID.txt"

# Storage location for final data
filename_OutfitData = path_UserInformation + "OutfitData.csv"

# %% Load the user specific data

def get_user_id(filename_UserID = filename_UserID):
    with open(filename_UserID) as f:
        UserName = f.read()
        return UserName

UserName = get_user_id()

def get_outfit_name(filename_OutfitID = filename_OutfitID):
    with open(filename_OutfitName) as f:
        OutfitName = f.read()
        return OutfitName

OutfitName = get_outfit_name()


# # %% A test of the API functionality
#
# request = requests.get("https://census.daybreakgames.com/s:" + UserName +
#                       "/get/ps2:v2/event/?type=DEATH&c:limit=1")
# print(request.text)

# %% Searching for the ID of the outfit and saving on the local machine
# url_Request = ("http://census.daybreakgames.com/s:" + UserName +
#                       "/get/ps2:v2/outfit/?name="+OutfitName)
# request = requests.get("http://census.daybreakgames.com/s:" + UserName +
#                       "/get/ps2:v2/outfit/?name="+OutfitName)
# print(request.text)
#
# OutfitInformation = json.loads(request.text)
# OutfitID = OutfitInformation['outfit_list'][0]['outfit_id']
#
# with open(filename_OutfitID, 'w') as f:
#    f.write(OutfitID)
#
# %% Load the outfit ID if this doesn't work run commented previous cell

def get_outfit_id(filename_OutfitID = filename_OutfitID):
    with open(filename_OutfitID) as f:
        OutfitID = f.read()
        return OutfitID

OutfitID = get_outfit_id()

# %% Get a list of the outfit members

def get_outfit_member_list(OutfitID, UserName, verbose=False):
    """
    Retrieves a list of outfit members from the API and returns them in 
    a pandas dataframe.
    
    Arguments:
        OutfitID (str): numeric ID for the outfit.
        
        UserName (str): account name for the user pulling from the API.

    Returns:
        df_OutfitMembers (pandas.DataFrame): API data dropped in pd.
    """
    request = requests.get("http://census.daybreakgames.com/s:" + UserName +
                           "/get/ps2:v2/outfit/?outfit_id=" + OutfitID +
                           "&c:resolve=member")
    # based off of the example in the documentation:
    # http://census.daybreakgames.com/
    # https://census.daybreakgames.com/get/ps2:v2/outfit/?outfit_id=37509488620601345&c:resolve=member

    if verbose == True:
        print(request.text)
    # df_OutfitMembers = pd.read_json(json.loads(request.text))
    # df_OutfitMembers = pd.read_json(json.loads(request.text)[
    #     'outfit_list'][0]['members'])
    # df_OutfitMembers = json.loads(request.text)['outfit_list'][0]['members'][0]
    df_OutfitMembers = pd.DataFrame(json.loads(request.text
                                               )['outfit_list'][0]['members'])
    return df_OutfitMembers

df_OutfitMembers = get_outfit_member_list(OutfitID, UserName)

# %% Testing the retrieval of the first outfit member

def test_member_apirequest(Username, CharacterID, verbose=False):
    #CharacterID = df_OutfitMembers['character_id'][0]
    request = requests.get("http://census.daybreakgames.com/s:" + UserName +
                           "/get/ps2:v2/character/?character_id=" +
                           CharacterID)

    if verbose:
        print(request.text)

    LastSaveDate = json.loads(request.text
                              )['character_list'][0]['times']['last_save_date']
    return LastSaveDate

test_member_apirequest(UserName, df_OutfitMembers['character_id'][0])


# %% Load the player status of each member in the outfit

def get_members_last_login(df_OutfitMembers):
    df_OutfitMembers['last_login_date'] = ''
    df_OutfitMembers['name'] = ''
    
    for index in df_OutfitMembers['character_id'].index:
        CharacterID = df_OutfitMembers.loc[index, 'character_id']
    
        request = requests.get("http://census.daybreakgames.com/s:" + UserName +
                               "/get/ps2:v2/character/?character_id=" +
                               CharacterID)
        try:
            last_login_date = json.loads(request.text)['character_list'][0][
                    'times']['last_login_date']
            CurrentUserName = json.loads(request.text)['character_list'][0][
                    'name']['first']
            df_OutfitMembers.loc[index, 'last_login_date'] = last_login_date
            df_OutfitMembers.loc[index, 'name'] = CurrentUserName
        except KeyError:
            print(request.text)
            break
    return df_OutfitMembers

df_OutfitMembers = get_members_last_login(df_OutfitMembers)

# %% Make a datetime version of the last save date

df_OutfitMembers['last_save_date_datetime'] = pd.to_datetime(df_OutfitMembers['last_login_date'])

# %% Add number of days feature

Today = datetime.datetime.today()
df_OutfitMembers['days_since_last_login'] = df_OutfitMembers['last_save_date_datetime'
                ].apply(lambda x: math.floor((Today - x).total_seconds()/(3600.*24)))

# %% reorder the columns and index

df_OutfitMembers = df_OutfitMembers.loc[:, ['name', 'rank',
                                            'days_since_last_login',
                                            'member_since_date',
                                            'rank_ordinal', 'character_id',
                                            'last_login_date']]

### TODO: sort dataframe based on last login date

df_OutfitMembers.sort_values(by=['days_since_last_login',
                                 'rank_ordinal', 'member_since_date', 'name'],
                             inplace=True,
                             ascending=False)


# %% Save dataframe as a .csv

df_OutfitMembers.to_csv(filename_OutfitData)

# # %% Making a concatenated string containing all of the user IDs separated
# by commas for use in the URL request
#
# str_CharacterIDs = ""
# for CharacterID in df_OutfitMembers['character_id']:
#    str_CharacterIDs += CharacterID + ','
# str_CharacterIDs = str_CharacterIDs[:-1]
#
# # %% Requesting all of the user IDs in a single request
# # This failed because the URL was too long.
#
# #for CharacterID in df_OutfitMembers['character_id']:
#    # print(CharacterID)
# request = requests.get("http://census.daybreakgames.com/s:" + UserName +
#                           "/get/ps2:v2/character/?character_id=" +
#                           str_CharacterIDs)
# print(request.text)
# #    TempJSON = json.loads(request.text)['character_list'][0]
# #    PlayerName = TempJSON['name']['first']
# #    PlayerName = CharacterID
# #    LastSaveDate = TempJSON['times']['last_save_date']
#
# #    print(PlayerName, LastSaveDate)
# #
