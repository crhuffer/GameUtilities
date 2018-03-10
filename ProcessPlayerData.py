# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 13:31:36 2018

@author: crhuffer

Loads the datafiles produced by the machine. It moves through each of the file
line by line, determines the type of the line, and then saves it to a file for
events of that type.
"""

import pandas as pd
import json
import os
#import theMachineV0_5 as mc

# %% Global variable declarations

Test = False

path_JSONData = '../Machine/'
path_CSVData = '../Machine/Data/'



# %%

class PS2Message():

    def __init__(self, message):
#        print( message, type(message), message.split()[0],
#              type(message.split()[0]))
        messageDict = json.loads(message)
#        print(messageDict)
#        print(message)
        self.newID = 0
        self.messageType = "unknown"
        self.determineType(messageDict)
        self.operateOnMessage(messageDict)

    def determineType(self, message):

#        open("PS2.json","a").write(str(message)+"\n")
        if "payload" in message.keys():
            if "event_name" in message["payload"].keys():
                self.messageType = message["payload"]["event_name"]
#                print self.messageType
                return 0
        if "type" in message.keys() and "service" in message.keys():
            if (message["type"] == "serviceStateChanged" and
                    message["service"] == "event"):
                self.messageType = message["detail"]
#                print self.messageType
                return 0

#        {"attacker_character_id":"5428351605419291633","attacker_fire_mode_id":"0","attacker_loadout_id":"1","attacker_vehicle_id":"8","attacker_weapon_id":"0","character_id":"5428351605419291633","character_loadout_id":"1","event_name":"Death","is_headshot":"0","timestamp":"1455676546","world_id":"1","zone_id":"4"},"service":"event","type":"serviceMessage"}
        if "payload" in message.keys():
            if "event_name" in message["payload"].keys():
                if message["payload"]["event_name"] == "Death":
                    self.messageType = "Death"
#                    print "Death Event 1:",message
                    return 0
                if message["payload"]["event_name"] == 'PlayerFacilityDefend':
                    self.messageType = 'PlayerFacilityDefend'
                    return 0
                if message["payload"]["event_name"] == 'GainExperience':
                    self.messageType = 'GainExperience'
                    return 0
                if message["payload"]["event_name"] == 'VehicleDestroy':
                    self.messageType = 'VehicleDestroy'
                    return 0
                if message["payload"]["event_name"] == 'AchievementEarned':
                    self.messageType = 'AchievementEarned'
                    return 0
                if message["payload"]["event_name"] == 'ItemAdded':
                    self.messageType = 'ItemAdded'
                    return 0
#                if message["payload"]["event_name"] == :
#                    self.messageType =
#                    return 0

        if 1:
            self.messageType = 0
            self.saveValue("PS2.json", str(message) + "\n")

    def saveValue(self, filename, outputMessage):
        if os.path.isfile(filename):
            open(filename, "a").write(outputMessage)
        else:
            open(filename, "w").write(outputMessage)

    def operateOnMessage(self, message):
        self.checkMessageType(message)

        if self.messageType == "PlayerLogin":
            character_id = message["payload"]["character_id"]
            timestamp = message["payload"]["timestamp"]
#            self.checkPlayerID(character_id)
#            filename = path_CSVData + "Player"+character_id+".dat"
            filename = path_CSVData + "PlayerLogin.dat"
#            open(filename,"a").write(character_id+"\t"+timestamp+"\n")
            self.saveValue(filename, "10\t" + timestamp + "\n")

        if self.messageType == "PlayerLogout":
            character_id = message["payload"]["character_id"]
            timestamp = message["payload"]["timestamp"]
#            self.checkPlayerID(character_id)
#            filename = path_CSVData + "Player"+character_id+".dat"
            filename = path_CSVData + "PlayerLogout.dat"
#            open(filename,"a").write(character_id+"\t"+timestamp+"\n")
            self.saveValue(filename, "11\t" + timestamp + "\n")

        if self.messageType == "Death":
            # print("Death Event 2:", message)
            character_id = message["payload"]["character_id"]
#            "character_loadout_id":"1","event_name":"Death","is_headshot":"0","timestamp":"1455676546","world_id":"1","zone_id":"4"},"service":"event","type":"serviceMessage"}
            attacker_character_id = message["payload"]["attacker_character_id"]
            a_fire_mode_id = message["payload"]["attacker_fire_mode_id"]
            a_loadout_id = message["payload"]["attacker_loadout_id"]
            a_vehicle_id = message["payload"]["attacker_vehicle_id"]
            a_weapon_id = message["payload"]["attacker_weapon_id"]
            event_name = message["payload"]["event_name"]
            is_headshot = message["payload"]["is_headshot"]
            timestamp = message["payload"]["timestamp"]
            world_id = message["payload"]["world_id"]
            zone_id = message["payload"]["zone_id"]

#            self.checkPlayerID(attacker_character_id)

            # character_id =0 stores suicides
            Type = '1' # default to actual kill (not suicide)
            if attacker_character_id == 0 or character_id == 0:
                Type = '0'

            outputMessage = "\t".join([Type, attacker_character_id,
                                       a_fire_mode_id, a_loadout_id,
                                       a_vehicle_id, a_weapon_id, is_headshot,
                                       timestamp, world_id, zone_id,
                                       character_id]) + '\r'
            filename = path_CSVData + "PS2Deaths.dat"
            self.saveValue(filename, outputMessage)


        if self.messageType == 'PlayerFacilityDefend':
#            {u'outfit_id': u'37527449492099598', 
#             u'character_id':u' 5428064957370121713', u'zone_id': u'4',
#             u'event_name': u'PlayerFacilityDefend',
#             u'timestamp': u'1455947688', u'facility_id': u'293000',
#             u'world_id': u'1'}
            outfit_id = message["payload"]['outfit_id']
            character_id = message["payload"]['character_id']
            zone_id = message["payload"]['zone_id']
            timestamp = message["payload"]['timestamp']
            facility_id = message["payload"]['facility_id']
            world_id = message["payload"]["world_id"]
            outputMessage = "\t".join(['12', zone_id, outfit_id, character_id,
                                       timestamp, facility_id,
                                       world_id]) + '\r'
#            outputMessage = ("12\t" + zone_id + "\t" + outfit_id + "\t" +
#                             character_id + "\t" + timestamp + "\t" +
#                             facility_id + "\t" + world_id + "\r")
#            filename = "FacilityDefends.dat"
            filename = path_CSVData + "FacilityDefends.dat"
            self.saveValue(filename, outputMessage)

        if self.messageType == 'GainExperience':
#            {u'character_id': u'7680926244008182529', u'zone_id': u'2',
#             u'event_name': u'GainExperience', u'timestamp': u'1455947688',
#             u'loadout_id': u'20', u'amount': u'100', u'world_id': u'25',
#             u'other_id': u'0', u'experience_id': u'557'}
            loadout_id = message['payload']['loadout_id']
            character_id = message['payload']['character_id']
            world_id = message['payload']['world_id']
            zone_id = message['payload']['zone_id']
            other_id = message['payload']['other_id']
            experience_id = message['payload']['experience_id']
            event_name = message['payload']['event_name']
            timestamp = message['payload']['timestamp']
            amount = message['payload']['amount']
            outputMessage = "\t".join(['4', experience_id, amount, timestamp,
                                       loadout_id, world_id, zone_id,
                                       other_id, character_id]) + '\r'
#            outputMessage = ("4\t" + experience_id + "\t" + amount + "\t" +
#                             timestamp + "\t" + loadout_id + "\t" + world_id +
#                             "\t" + zone_id + "\t" + other_id + "\r")
#            filename = path_CSVData + "Player"+character_id+".dat"
            filename = path_CSVData + "GainedExp.dat"
            self.saveValue(filename, outputMessage)

        if self.messageType == 'VehicleDestroy':
#            {u'vehicle_id': u'3', u'character_id': u'5428011263390564993',
#             u'zone_id': u'8', u'event_name': u'VehicleDestroy',
#             u'timestamp': u'1455947688', u'faction_id': u'2',
#             u'facility_id': u'0', u'world_id': u'1',
#             u'attacker_character_id': u'5428010618015275809',
#             u'attacker_weapon_id': u'802875', u'attacker_loadout_id': u'12',
#             u'attacker_vehicle_id': u'12'}
            character_id = message['payload']['character_id']
            event_name = message['payload']['event_name']
            timestamp = message['payload']['timestamp']
            facility_id = message['payload']['facility_id']
            vehicle_id = message['payload']['vehicle_id']
            zone_id = message['payload']['zone_id']
            faction_id = message['payload']['faction_id']
            world_id = message['payload']['world_id']
            attacker_character_id = message['payload']['attacker_character_id']
            attacker_weapon_id = message['payload']['attacker_weapon_id']
            attacker_vehicle_id = message['payload']['attacker_vehicle_id']
            attacker_loadout_id = message['payload']['attacker_loadout_id']

#              self.checkPlayerID(attacker_character_id)
            Type = '6'
            if attacker_character_id == 0:  # character_id =0 stores suicides
                Type = '5'

            outputMessage = '\t'.join([Type, timestamp, facility_id,
                                       vehicle_id, zone_id, faction_id,
                                       world_id, attacker_character_id,
                                       attacker_weapon_id, attacker_vehicle_id,
                                       attacker_loadout_id,
                                       character_id]) + '\r'
#            filename = "Deaths/PS2"+self.messageType+ str(character_id)+".dat"
#            filename = path_CSVData + "Player"+character_id+".dat"
            filename = path_CSVData + "VehicleDestroyed.dat"
#            filename = "PS2Deaths.dat"
            self.saveValue(filename, outputMessage)


        if self.messageType == 'ItemAdded':
#            {u'character_id': u'5428285306548900689', u'zone_id': u'4',
#             u'event_name': u'ItemAdded', u'timestamp': u'1455947688',
#             u'item_count': u'1', u'world_id': u'1',
#             u'context': u'GiveRewardBundle:Ding', u'item_id': u'70463'}
            item_id = message['payload']['item_id']
            character_id = message['payload']['character_id']
            world_id = message['payload']['world_id']
            zone_id = message['payload']['zone_id']
            context = message['payload']['context']
            event_name = message['payload']['event_name']
            timestamp = message['payload']['timestamp']
            item_count = message['payload']['item_count']

            outputMessage = '\t'.join(['8', item_id, world_id, zone_id,
                                       context, timestamp, item_count,
                                       character_id]) + '\r'
#            filename = path_CSVData + "Player" + character_id + ".dat"
            filename = path_CSVData + 'ItemAdded.dat'
            self.saveValue(filename, outputMessage)

        if self.messageType == 'AchievementEarned':
#            {u'character_id': u'5428285306548900689', u'zone_id': u'4',
#             u'event_name': u'AchievementEarned', u'timestamp': u'1455947688',
#             u'achievement_id': u'3709', u'world_id': u'1'}

            character_id = message['payload']['character_id']
            zone_id = message['payload']['zone_id']
            event_name = message['payload']['event_name']
            timestamp = message['payload']['timestamp']
            achievement_id = message['payload']['achievement_id']
            world_id = message['payload']['world_id']

            outputMessage = '\t'.join(['9', zone_id, timestamp, achievement_id,
                                       world_id, character_id]) + '\r'
#            filename = path_CSVData + "Player" + character_id + ".dat"
            filename = path_CSVData + 'AchievementEarned.dat'
            self.saveValue(filename, outputMessage)
#        self.saveValue("PS2.json",str(message)+"\n")

    def checkMessageType(self, message):
        filename = path_JSONData + "PS2messageTypes.dat"
        messageTypes = open(filename, "r").readlines()
        messageTypes = [element.strip() for element in messageTypes]
#        print messageTypes,type(messageTypes)
        if self.messageType not in messageTypes:
            messageTypes.append(self.messageType)
            self.saveValue(filename, str(self.messageType) + "\n")
            filename = path_JSONData + "PS2messageExamples.dat"
            outputDict = {}
            outputDict[self.messageType] = message
            self.saveValue(filename, str(outputDict) + "\n")


# %%

if Test:
    filename = path_JSONData + "dataV2f00030.dat"

    with open(filename, 'r') as f:
        data = f.readlines()

# %% 

if Test:
    for line in data:
    #    message = mc.PS2Message(line)
        message = PS2Message(line)
        
# %% Testing loading the data in to a dataframe
#
#filename = path_CSVData + 'KilledPlayer.dat'
#Columns = ['type', 'character_id', 'a_fire_mode_id', 'a_loadout_id', 'a_vehicle_id', 'a_weapon_id', 'is_headshot', 'timestamp', 'world_id', 'zone_id', 'attacker_character_id']
#df_KilledPlayer = pd.read_csv(filename, sep='\t', names=Columns)

# %% Loading all files into a dataframe

list_FilesToProcess = []
#for (dirpath, dirnames, filenames) in os.walk('./Data2Test'):
for (dirpath, dirnames, filenames) in os.walk(path_JSONData):
    for filename in filenames:
        if filename.endswith('.dat') and filename.startswith('dataV2f'):
            print(filename)
            with open(path_JSONData + filename, 'r') as f:
                data = f.readlines()
                for line in data:
#    message = mc.PS2Message(line)
                    message = PS2Message(line)
            os.remove(path_JSONData + filename)