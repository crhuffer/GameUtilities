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
import numpy as np
import math 
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


# %% Main loop
# Load player data and extract features related to each play session.

# lists to store the features
list_session_durations = []      
list_session_kills = []
list_session_exp = []

# Walk through the player files
for (dirpath, dirnames, filenames) in os.walk('./'):
    for filename in filenames:
        if filename.endswith('.dat'):
#            print(filename)
            with open(filename, 'r') as f:
                login = 0
                counter_kills = 0
#                exp_per_death = 0
                exp_per_session = 0
            
                # Parse the player files
                for line in f.readlines():
                    
                    # Catch unexpected cases, blank files for example
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
                        print('Value Error on filename: ', filename)
                        continue
                    
# %% Conversions and adding features to df_session
                        
df_session = pd.DataFrame(list_session_durations, columns=['Duration'])
df_session/=3600.
df_session['Kills'] = list_session_kills
df_session['SessionExp'] = list_session_exp

# %% Apply normalization

scaler = MinMaxScaler()
columns = df_session.columns
df_session_norm = pd.DataFrame(scaler.fit_transform(df_session), columns=columns)

# %% Apply PCA

pca = PCA(n_components=len(df_session_norm.columns)-1)
pca.fit(df_session_norm)
df_session_pca = pd.DataFrame(pca.transform(df_session_norm))

# %% Elbow plot for clustering on the normalized data

clusters = range(3,10)
kmeans = [KMeans(n_clusters=cluster) for cluster in clusters]
inertias = []
for kmean in kmeans:
    kmean.fit(df_session_norm)
    inertias.append(kmean.inertia_)
    
fig, ax = plt.subplots()
plt.plot(clusters, inertias, marker='.')
ax.set_xlabel('Num Clusters')
ax.set_ylabel('Inertia')

# %% Clustering on the normalized data

n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters).fit(df_session_norm)
labels = kmeans.predict(df_session_norm)
df_session['ClustersV1'] = labels

# %% Clustering on the pca data

n_clusters = 10
kmeans_pca = KMeans(n_clusters=n_clusters).fit(df_session_pca)
labels_pca = kmeans_pca.predict(df_session_pca)
df_session['ClustersPCAV1'] = labels_pca

# %% Histogram of session duration

df_session['Duration'].hist(bins=100)

# %% Histogram of session duration, zoomed in on low time peak
df_session['Duration'].apply(lambda x: x*3600.0).hist(bins=np.linspace(0, 60, 100))

# %% Histogram of the session kills

df_session['Kills'].hist(bins=100)

# %% Histogram of the session experience

df_session['SessionExp'].hist(bins=100)

# %% 2d histogram of the session duration and kills
fig, ax = plt.subplots()
plt.hist2d(x='Duration', y='Kills', data=df_session, bins=(100,100), norm=mpl.colors.LogNorm())
#ax.set_yscale('log')
#ax.set_xscale('log')
# %% Joint plot of the duration and kills

sns.jointplot(x='Duration', y='Kills', data=df_session, kind='scatter')

# %% Plot: clusters on the original data

fig, ax = plt.subplots()
plt.scatter(x='Duration', y='Kills', data=df_session, marker='.', c='Clusters3')
ax.set_xlabel('Duration [hrs]')
ax.set_ylabel('Kills')
fig.legend()

# %% Plot: cluster made in the pca transform but mapped to the original data
fig, ax = plt.subplots()
plt.scatter(x='Duration', y='Kills', data=df_session, marker='.', c='ClustersPCA')
ax.set_xlabel('Duration [hrs]')
ax.set_ylabel('Kills')
fig.legend()

# %% Plot: clusters in the primary components of the pca transformed data

fig, ax = plt.subplots()
plt.scatter(x=df_session_pca.iloc[:, 0], y=df_session_pca.iloc[:, 1], marker='.', c=labels_pca)
ax.set_xlabel('PCA Axis 0')
ax.set_ylabel('PCA Axis 1')

# %% Crosstab to compare different versions of clusters.

crosstab = pd.crosstab(df_session['ClustersV1'], df_session['ClustersPCAV1'])
crosstab = pd.crosstab(df_session['ClustersV1'], df_session['ClustersPCAV1']).apply(lambda x: x.apply(lambda y: math.log(y+1)))

