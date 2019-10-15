from src import * 
#%%
audio_db        = DatabaseSpotifyAudio()
test_connector  = SpotifyConnector()
test_user       = SpotifyUserExplorer()

test_user.list_playlist_names()
playlist_id = test_user.get_playlist_id_from_name('nn')

test_list       = TrackListSpotify()
test_list.add_tracks_from_public_user_playlist(playlist_id)
test_list.remove_tracks_with_missing_previews()

musicnn_featurizer = FeaturizerMusicnn()
test_feat = musicnn_featurizer.get_features_for_track('2XMTqoHHSH0lvuXrvIEdco')

#%%
test_connector  = SpotifyConnector()

#%%
spot_featurizer    = FeaturizerSpotify()
test_feature = spot_featurizer.get_features_for_track('2XMTqoHHSH0lvuXrvIEdco')

#%%
features_records = featurizer.get_features_for_tracks(['0ac2BxpvOntMSC5zfLzU2i', '0ac2BxpvOntMSC5zfLzU2i'], recalculate = False)
import pandas as pd
features_df      = pd.DataFrame.from_records(features_records)
#%%
from songfinder.src import *

#%%
db_list = TrackListSpotify()

#%%


#%%
# now... to build the recommender

#%%
# which recommender will we use? 
# class Recommender
#   def load_similarity 
#   def recommend_songs(input_data, output_data, number_songs)

# to build our recommender system

#### INPUTS
# define database
# define target playlist


# recommender sweep
    # 
    # 
    # 

#### FEATURES
# input: database, target playlists, featurizer
    # define features of interest
        # feature - data type - similarity metric of interest
    # calculate features of database
    # calculate features of targets
# output: features of database and playlists

#### SIMILARITY CHECKER
# input: features of database and playlists
    # define similarity measure of interest (per feature?)
        # cosine similarity
        # euclidean
        # combination? 
# output: similarity matrix 

#### RECOMMENDATIONS
# input: similarity matrix
    # define how to operate on similarity matrix
        # mean
        # k-means clustering
        # PCA + clustering? 
        # t-SNE + clustering? 
# output: ranked list of recommendations

#%% Definitions of interest
def extract_features(db_track_ids, playlist_track_ids, featurizer):
    return db_feats, playlist_feats

# key2measure (and then normalize?)
def compose_similarity_matrix(db_feats, playlist_feats, similarity_measure):
    return sim_mat
def rank_from_similarity_matrix(sim_mat):
    return db_rankings

#%% Running a single recommendation run

#%% things to test for the recommendation 

# spotify musicality --> 