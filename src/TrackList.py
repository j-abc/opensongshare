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
from .SpotifyConnector import SpotifyConnector
from .DatabaseSpotifyAudio import DatabaseSpotifyAudio

class TrackList:
    def __init__(self):
        self.dataframe = []

    def add_to_audio_db(self):
        pass

    # def spotify_id_from_names(self, song_names, artist_names):
    #     pass
    def remove_tracks_with_missing_previews(self):
        isnull = self.dataframe['preview_url'].isnull()
        self.dataframe = self.dataframe[~isnull]

    def _load_features_for_track(self, track_id, set_name):
        track_path = os.path.join('/home/ubuntu/insight/data/feature_sets/', set_name, track_id + '.pkl')
        with open(track_path, 'rb') as handle:
            features = pickle.load(handle)  
        return features      

    # load or calculate the features? 
    def load_features(self, set_name):
        track_ids = self.dataframe['id'].values
        features = [self._load_features_for_track(track_id, set_name) for track_id in track_ids]
        features_df = pd.DataFrame.from_records(features)
        features_df['track_id'] = track_ids
        return features_df

class TrackListSpotify(TrackList):
    def __init__(self, user = None):
        super(TrackList, self).__init__()
        self.connection2spotify = SpotifyConnector(user = user)
        self.dataframe          = pd.DataFrame(columns = ['artist_names', 'artist_ids', 'name','id','preview_url','uri', 'playlist_id'])
        self.list_db_path       = '/home/ubuntu/insight/data/raw/lists_spotify/'
        self.list_name          = None

    def add_all_tracks_from_public_user(self, user = None):
        sublist_df = pd.DataFrame.from_records(self.connection2spotify.get_public_user_tracks_formatted(user = user))
        if user == None:
            user = self.connection2spotify.user
        sublist_df['playlist_id'] = sublist_df.shape[0]*['[all][' + user + ']']
        self.dataframe = self.dataframe.append(sublist_df)

    def add_tracks_from_public_user_playlist(self, playlist_id, user = None):
        sublist_df = pd.DataFrame.from_records(self.connection2spotify.get_tracks_from_playlist_formatted(playlist_id = playlist_id, user = user))
        if user == None:
            user = self.connection2spotify.user
        sublist_df['playlist_id'] = sublist_df.shape[0]*['[' + playlist_id + ']' + '[' + user + ']']
        self.dataframe = self.dataframe.append(sublist_df)

    def load_list_from_db(self, list_name = None):
        if list_name == None:
            list_name = self.list_name
        else:
            self.list_name = list_name
        self.dataframe = pd.read_pickle(os.path.join(self.list_db_path, self.list_name + '.pkl'))

    def set_list_name(self, list_name = None):
        self.list_name = list_name

    def write_list_to_db(self, list_name = None):
        if list_name == None:
            list_name = self.list_name
        else:
            self.list_name = list_name
        self.dataframe.to_pickle(os.path.join(self.list_db_path, self.list_name + '.pkl'))

    def populate_audio_database(self):
        db_audio = DatabaseSpotifyAudio()
        track_id_list = self.dataframe.loc[:,'id'].values
        num_tracks = len(track_id_list)
        itrack = 0
        for track_id in track_id_list:
            db_audio.insert_track_from_id(track_id) 
            itrack = itrack  + 1
            print('%d out of %d\n'%(itrack, num_tracks))

    # def combine_lists(self, all_lists):
    #     pass

    # # add songs from different spotify sources
    # def add_from_public_user_playlist(self, playlist_id, user = None):
    #     # adds songs from this user playlist
    #     return 1

    # save information out to a dataframe!
        # what do we want to call this one? 
