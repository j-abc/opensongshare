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
from ..SpotifyConnector import SpotifyConnector
from ..DatabaseSpotifyAudio import DatabaseSpotifyAudio

class TrackList:
    def __init__(self):
        self.dataframe = []

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

    # def combine_lists(self, all_lists):
    #     pass

    # # add songs from different spotify sources
    # def add_from_public_user_playlist(self, playlist_id, user = None):
    #     # adds songs from this user playlist
    #     return 1

    # save information out to a dataframe!
        # what do we want to call this one? 