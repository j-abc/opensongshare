import pandas as pd
import numpy as np
import os.path as path
import spotipy.util as su
import argparse
import librosa
import itertools
import logging
import os
import pickle
import random
import spotipy
import sys
import time
import wget
import json

#%%
# For connecting to spotify instance; mainly composed of convenience methods


# For exploring a spotify user - don't really care about this one right now

#
 #
    # def write_to_df(self, list_db, list_name):
    #     # pd.to_pickle()
    #     pass
    # def load_from_df(self, list_db, list_name):
    #     # pd.read_pickle
    #     pass
    # def combine_track_lists(self, lists):
    #     pass

#
# test_list = TrackList()

# For creating lists of data... basically.. track lists lol 


#%%
class TrackListBillboards:
    def __init__(self):
        pass

#%% Demonstration of utility 
# get a track 
spot_conn    = SpotifyConnector()
tracks       = spot_conn.get_public_user_tracks_formatted()
print(tracks[0]['id'])

# and put it into the database!
db_audio = DatabaseSpotifyAudio()
db_audio.insert_track_from_id(tracks[0]['id'])


#%% EXAMPLE OF HOW TO USE SPOTIFYCONNECTOR CLASS
# here, we instantiate our spotify connector... and get all the tracks of a given user as a set of records

# class DatasetSpotifyAudio
# params: 
    # base_folder_path: where the dataset is stored...
    # dataset_name 
    # num_songs
    # num_artists
    # has_loaded
    # df (dataframe of the audio)

# def __init__(self):
    # loads our dataset

# def list_tracks
# def list_artists
# def num_entries

#%%
# SpotifyTracksList...
# what does this do? 
# it... 
class SpotifyTracksList:

class SpotifySongsList:
    # operate by song uris
    def __init__(self):
        self._data = 
#%%
test_ssl = SpotifySongsList()

#%% 
# now... how to download and store audio... need to figure this out...

#%% 

#%%
# getting feature sets on mp3s
# featurizer

#%% 