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


class DatabaseSpotifyAudio:
    # class for downloading raw audio previews

    def __init__(self):
        self.audio_db_path = '/home/ubuntu/insight/data/raw/spotify_audio/mp3/'
        self.connection2spotify = SpotifyConnector() 

    def insert_track_from_id(self, track_id):
        # insert track raw audio preview given our track id

        mp3_name = track_id + '.mp3'
        mp3_path = os.path.join(self.audio_db_path, mp3_name)
        track_info = self.connection2spotify.get_track_from_id_formatted(track_id)
        if not track_info['preview_url']:
            return False
        if not os.path.exists(mp3_path):
            wget.download(track_info['preview_url'], mp3_path)
        return True
