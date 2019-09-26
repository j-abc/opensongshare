import numpy as np
import os 
import pickle

class Featurizer:
    def __init__(self, name = ''):
        self.audio_db_path        = '/home/ubuntu/insight/data/raw/spotify_audio/mp3/'
        self.features_db_path     = '/home/ubuntu/insight/data/feature_sets/'
        self.name                 = name
        self.features_path        = os.path.join(self.features_db_path, self.name)
        if not os.path.exists(self.features_path):
            os.makedirs(self.features_path)
        self.feature_keys         = ['']

    def get_features_for_track(self, track_id, recalculate = False):
        track_feature_path = os.path.join(self.features_path, track_id + '.pkl')
        if os.path.exists(track_feature_path) and not recalculate:
            # load the track features
            with open(track_feature_path, 'rb') as handle: 
                features = pickle.load(handle)
        else: 
            # calculate and save the track features 
            features = self.calculate_features_for_track(track_id)
            with open(track_feature_path, 'wb') as handle:
                pickle.dump(features, handle)
        return features

    def get_features_for_tracks(self, track_ids, recalculate = False):
        return [self.get_features_for_track(track_id, recalculate = recalculate) for track_id in track_ids]

    def calculate_features_for_track(self, track_id):
        return {'id': track_id}

    def get_track_mp3_path(self, track_id):
        return os.path.join(self.audio_db_path, track_id + '.mp3')