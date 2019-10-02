import os
from .Featurizer import Featurizer
from .SpotifyConnector import SpotifyConnector

class FeaturizerSpotify(Featurizer):
    def __init__(self):
        Featurizer.__init__(self, name = 'SpotifyMusicality')
        self.feature_keys  = []
        self.connection2spotify = SpotifyConnector()
        
    def calculate_features_for_track(self, track_id):
        out_features = self.connection2spotify.instance.audio_features(track_id)[0]
        return out_features
