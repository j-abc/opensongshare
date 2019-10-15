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

class SpotifyUserExplorer:
    def __init__(self, user = None):
        # Class for looking at public playlist tracks from a spotify user
        self.connection2spotify = SpotifyConnector(user = user)
        self.playlist_df   = pd.DataFrame.from_records(self.connection2spotify.get_public_user_playlists_formatted())
    def list_playlist_names(self):
        return self.playlist_df.loc[:, 'name'].values
    def get_playlist_id_from_name(self, name):
        playlist_id = self.playlist_df.loc[self.playlist_df['name'].str.match(name),'id'].values
        if len(playlist_id) > 1:
            print('more than one playlist matches this name')
            return False
        else: 
            return playlist_id[0]
