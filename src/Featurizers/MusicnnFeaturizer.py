import os
import musicnn
from musicnn.extractor import extractor
from .Featurizer import Featurizer

class MusicnnFeaturizer(Featurizer):
    def __init__(self, model = 'MTT_musicnn'):
        Featurizer.__init__(self, name = model)
        self.feature_keys  = ['penultimate_over_time', 'taggram_over_time', 'penultimate', 'taggram']
        if 'MTT' in self.name:
            self.tags = musicnn.configuration.MTT_LABELS
        elif 'MSD' in name:
            self.tags = musicnn.configuration.MSD_LABELS
        
    def calculate_features_for_track(self, track_id):
        mp3_path = self.get_track_mp3_path(track_id)
        taggram, tags, features = extractor(mp3_path, model = 'MTT_musicnn', extract_features = True)
        out_features = {'penultimate_over_time':features['penultimate'], 'taggram_over_time': taggram}
        out_features['taggram']     = np.mean(out_features['taggram_over_time'], axis = 0)
        out_features['penultimate'] = np.mean(out_features['penultimate_over_time'], axis = 0)
        out_features['id'] = track_id
        return out_features