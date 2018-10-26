# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 18:48:42 2018

@author: crhuffer
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# %%

#df_raw = pd.read_csv('Player8266105775633161185.dat')
#
## %%
#
#login = 0
#logout = 0
#
#columns = ['Duration']
#df_session = pd.DataFrame(columns=columns)
#list_session_durations = []
#for line in df_raw.values:
#    line = line[0]
#    split = line.split('\t')
##    print(line)
##    print(split)
#    if int(split[0]) == 10:
#        print('login', split)
#        login = 1
#        login_datetime = int(split[1])
#        session = {}
#    elif int(split[0]) == 11:
#        print('logout', split)
#        logout_datetime = int(split[1])
##        session['Duration'] = logout_datetime - login_datetime
#        list_session_durations.append(logout_datetime - login_datetime)
##        df_session[login_datetime] = session['Duration']
##    break
#        
# %%

list_session_durations = []      
list_session_kills = []
list_session_exp = []
for (dirpath, dirnames, filenames) in os.walk('./'):
    for filename in filenames:
        if filename.endswith('.dat'):
#            print(filename)
            with open(filename, 'r') as f:
                login = 0
                counter_kills = 0
#                exp_per_death = 0
                exp_per_session = 0
                for line in f.readlines():
                    
                    try:
                        split = line[:-1].split('\t')
                        
                        # character login
                        if int(split[0]) == 10:
#                            print('login', split)
                            login = 1
                            login_datetime = int(split[1])
                            
                            exp_per_session = 0
                            
                        # character logout
                        elif int(split[0]) == 11:
#                            print('logout', split)
                            logout_datetime = int(split[1])
                            
                            # only record the value if the player has logged in
                            # in our records.
                            if login == 1:
                                list_session_durations.append(logout_datetime - login_datetime)
                                
                                list_session_kills.append(counter_kills)
                                counter_kills = 0
                                
                                list_session_exp.append(exp_per_session)
                                experience_per_kill = 0
                                
                        # character kill
                        elif int(split[0]) == 1:
                            counter_kills += 1
                            
                        # gain experience
                        elif int(split[0]) == 4:
                            exp = int(split[2])
#                            exp_per_death += exp
                            exp_per_session += exp
                            
                        
                    except ValueError:
                        continue
                    
# %%
                        
df_session = pd.DataFrame(list_session_durations, columns=['Duration'])
df_session/=3600.
df_session['Kills'] = list_session_kills
df_session['SessionExp'] = list_session_exp
# %%

df_session['Duration'].hist(bins=100)

# %%

df_session['Kills'].hist(bins=100)

# %%

df_session['SessionExp'].hist(bins=100)

# %%
fig, ax = plt.subplots()
plt.hist2d(x='Duration', y='Kills', data=df_session, bins=(100,100), norm=mpl.colors.LogNorm())
#ax.set_yscale('log')
#ax.set_xscale('log')
# %%

sns.jointplot(x='Duration', y='Kills', data=df_session, kind='scatter', markersize=0.7)

# %%

sns.jointplot(x='Duration', y='Kills', data=df_session, kind='scatter', markersize=0.7)
