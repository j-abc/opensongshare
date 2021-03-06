import os
from .Featurizer import Featurizer
from .SpotifyConnector import SpotifyConnector

class FeaturizerSpotify(Featurizer):
    def __init__(self):
        # class for extracting features that are provided by spotify. Here, we are extracting low level musicality features for each song
        Featurizer.__init__(self, name = 'SpotifyMusicality')
        self.feature_keys  = ['danceability', 'energy', 'loudness', 'mode','speechiness','acousticness','instrumentalness', 'liveness','valence']

        # all features on scale [0, 1], removed mode, key, and tempo
        self.connection2spotify = SpotifyConnector()
        
    def calculate_features_for_track(self, track_id):
        # extracts low level audio features from spotify
        out_features = self.connection2spotify.instance.audio_features(track_id)[0]
        return {key:item for key, item in out_features.items() if key in self.feature_keys}