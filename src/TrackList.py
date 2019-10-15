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
        # Class for defining and manipulating a list of tracks

        self.dataframe = []

    def remove_tracks_with_missing_previews(self):
        # remove tracks without previews from the list
        isnull = self.dataframe['preview_url'].isnull()
        self.dataframe = self.dataframe[~isnull]

    def remove_duplicate_tracks(self):
        self.dataframe.drop_duplicates(subset = 'id', inplace = True)

    def _load_features_for_track(self, track_id, set_name):
        # load the features for a track in the list
        track_path = os.path.join('/home/ubuntu/insight/data/feature_sets/', set_name, track_id + '.pkl')
        with open(track_path, 'rb') as handle:
            features = pickle.load(handle)  
        return features      

    def load_features(self, set_name):
        # load the features across all of our tracks
        track_ids = self.dataframe['id'].values
        features = [self._load_features_for_track(track_id, set_name) for track_id in track_ids]
        features_df = pd.DataFrame.from_records(features)
        features_df['track_id'] = track_ids
        return features_df