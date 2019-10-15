import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import KMeans
from .FeaturizerMusicnn import *
from .FeaturizerSpotify import *
from .Featurizer import * 

class Recommender:
    def __init__(self, model_type, which_layer = '', distance_type = 'euclidean', pl_centroid_type = 'None', rank_type = 'mean', report_streamlit = False):
        # set our recommender parameters
        self.model_type       = model_type
        self.which_layer      = which_layer
        self.distance_type    = distance_type
        self.rank_type        = rank_type
        self.pl_centroid_type = pl_centroid_type

        # will we report streamlit?
        self.report_streamlit = report_streamlit

        # load our featurizer 
        if self.model_type == 'spotify_audio':
            self.featurizer   = FeaturizerSpotify()
        else:
            self.featurizer   = FeaturizerMusicnn(self.model_type)

    def predict_rank(self, playlist_track_ids, database_track_ids, limit_n = None):
        ranks = [i + 1 for i in range(len(database_track_ids))]
        if self.model_type == 'randomized':
            rand_db_ids = np.copy(database_track_ids)
            np.random.shuffle(rand_db_ids)
            rank_id_df = pd.DataFrame.from_dict({'id' : rand_db_ids, 'rank' : ranks})
            if limit_n:
                rank_id_df = rank_id_df.iloc[:limit_n]
            return rank_id_df

        # featurize
        pl_raw_feats = pd.DataFrame.from_records(self.featurizer.get_features_for_tracks(playlist_track_ids))
        db_raw_feats = pd.DataFrame.from_records(self.featurizer.get_features_for_tracks(database_track_ids))

        # extract and shape features
        if self.which_layer:
            pl_feat_array = np.vstack(pl_raw_feats[self.which_layer].values)
            db_feat_array = np.vstack(db_raw_feats[self.which_layer].values)
        else: # if not musicnn, assume we use all 
            pl_feat_array = np.vstack(pl_raw_feats.values)
            db_feat_array = np.vstack(db_raw_feats.values)

        # do we want to reduce the playlist to centroids? 
        if not(self.pl_centroid_type == 'None'):
            pl_feat_array = self._get_playlist_centroids(pl_feat_array, pl_centroid_type =self.pl_centroid_type)

        # alright! now lets rank it
        rank2dbidx = self._dist2rank(pl_feat_array, db_feat_array, distance_type = self.distance_type, rank_type = self.rank_type)

        # and let's get our database ranking back
        sorted_ids = database_track_ids[rank2dbidx]        

        # gather into dataframe and return
        rank_id_df = pd.DataFrame.from_dict({'id' : sorted_ids, 'rank' : ranks})

        if limit_n:
            rank_id_df = rank_id_df.iloc[:limit_n]

        return rank_id_df

    def _get_playlist_centroids(self, feat_array, pl_centroid_type):
        if pl_centroid_type == 'mean':
            return np.mean(feat_array, axis = 0)[:,np.newaxis]

        if pl_centroid_type == 'k2':
            if feat_array.shape[0] > 1:
                clustering = KMeans(n_clusters = 2, random_state = 0).fit(feat_array)
                return clustering.cluster_centers_
            else:
                raise Exception('need >= 2 data points in database.')

        if pl_centroid_type == 'k3':
            if feat_array.shape[0] > 2:
                clustering = KMeans(n_clusters = 3, random_state = 0).fit(feat_array)
                return clustering.cluster_centers_
            else:
                raise Exception('need >= 3 data points in database.')

    def _dist2rank(self, pl_feat_array, db_feat_array, distance_type, rank_type):
        dmat = pairwise_distances(X = db_feat_array, Y = pl_feat_array, metric = distance_type)

        # collapse the distance 
        collapse_dfun = {'mean': np.mean,
                        'max': np.max,
                        'min': np.min}
        collapse_dmat = collapse_dfun[rank_type](dmat, axis = 1)
        
        # sort and put out the ranking 
        sorted_db_idx = np.argsort(collapse_dmat)
        # if distance_type == 'euclidean':
        #     sorted_db_idx = sorted_db_idx[::-1]

        return sorted_db_idx