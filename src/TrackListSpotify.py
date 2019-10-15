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
from .TrackList import *

class TrackListSpotify(TrackList):
    def __init__(self, user = None):
        super(TrackList, self).__init__()
        self.connection2spotify = SpotifyConnector(user = user)
        self.dataframe          = pd.DataFrame(columns = ['artist_names', 'artist_ids', 'name','id','preview_url','uri', 'playlist_id', 'original_playlist'])
        self.list_db_path       = '/home/ubuntu/insight/data/raw/lists_spotify/'
        self.list_name          = None

    def add_tracks_from_track_ids(self, track_ids):
        sublist_df = pd.DataFrame.from_records(self.connection2spotify.get_tracks_from_ids_formatted(track_ids))
        if user == None:
            user = self.connection2spotify.user

    def add_all_tracks_from_public_user(self, user = None):
        sublist_df = pd.DataFrame.from_records(self.connection2spotify.get_public_user_tracks_formatted(user = user))
        if user == None:
            user = self.connection2spotify.user
        sublist_df['playlist_id'] = sublist_df.shape[0]*['[all][' + user + ']']
        sublist_df['original_list'] = sublist_df.shape[0]*[self.list_name]
        self.dataframe = self.dataframe.append(sublist_df)

    def add_tracks_from_public_user_playlist(self, playlist_id, user = None):
        sublist_df = pd.DataFrame.from_records(self.connection2spotify.get_tracks_from_playlist_formatted(playlist_id = playlist_id, user = user))
        if user == None:
            user = self.connection2spotify.user
        sublist_df['playlist_id'] = sublist_df.shape[0]*['[' + playlist_id + ']' + '[' + user + ']']
        sublist_df['original_list'] = sublist_df.shape[0]*[self.list_name]
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