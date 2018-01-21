# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:12:54 2018

@author: crhuffer
"""

# %% imports

import pandas as pd
#import numpy as np
import json
import requests

# %% Path and filename definitions

path_UserInformation = "../../../Code/TheMachine/Inputs/"

filename_UserID = path_UserInformation + "APIUserName.txt"
filename_OutfitName = path_UserInformation + "OutfitName.txt"

filename_OutfitID = path_UserInformation + "OutfitID.txt"

# %% Load the user specific data

#OutfitName = pd.read_csv(filename_outfitname)
#UserName = pd.read_csv(filename_userid)

with open(filename_UserID) as f:
    UserName = f.read()
    
with open(filename_OutfitName) as f:
    OutfitName = f.read()


## %%
#
#request = requests.get("https://census.daybreakgames.com/s:" + UserName +
#                       "/get/ps2:v2/event/?type=DEATH&c:limit=1")
#print(request.text)

# %%

request = requests.get("http://census.daybreakgames.com/s:" + UserName +
                       "get/ps2:v2/outfit/?name="+OutfitName)
print(request.text)

OutfitInformation = json.loads(request.text)
OutfitID = OutfitInformation['outfit_list'][0]['outfit_id']

with open(filename_OutfitID, 'w') as f:
    f.write(OutfitID)
    
# %% Load the outfit ID if this doesn't work run commented previous cell

with open(filename_OutfitID) as f:
    OutfitID =f.read()
    
# %% Get a list of the outfit members

request = requests.get("http://census.daybreakgames.com/s:" + UserName +
                       "get/ps2:v2/outfit/?outfit_id=" + OutfitID +
                       "&c:resolve=member")
# based off of the example in the documentation:
# http://census.daybreakgames.com/
# https://census.daybreakgames.com/get/ps2:v2/outfit/?outfit_id=37509488620601345&c:resolve=member

print(request.text)
#df_OutfitMembers = pd.read_json(json.loads(request.text))
#df_OutfitMembers = pd.read_json(json.loads(request.text)['outfit_list'][0]['members'])
#df_OutfitMembers = json.loads(request.text)['outfit_list'][0]['members'][0]
df_OutfitMembers = pd.DataFrame(json.loads(request.text)['outfit_list'][0]['members'])

## %%
#
#CharacterID = df_OutfitMembers['character_id'][0]
#request = requests.get("http://census.daybreakgames.com/s:" + UserName +
#                       "get/ps2:v2/character/?character_id=" + CharacterID)
#
#print(request.text)

# %%

str_CharacterIDs = ""
for CharacterID in df_OutfitMembers['character_id']:
    str_CharacterIDs += CharacterID + ','
str_CharacterIDs = str_CharacterIDs[:-1]

# %%

    

#for CharacterID in df_OutfitMembers['character_id']:
    # print(CharacterID)
request = requests.get("http://census.daybreakgames.com/s:" + UserName +
                           "get/ps2:v2/character/?character_id=" + str_CharacterIDs)
print(request.text)
#    TempJSON = json.loads(request.text)['character_list'][0]
#    PlayerName = TempJSON['name']['first']
#    PlayerName = CharacterID
#    LastSaveDate = TempJSON['times']['last_save_date']
    
#    print(PlayerName, LastSaveDate)
#    