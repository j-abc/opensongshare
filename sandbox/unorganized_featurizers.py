#%%

#%%
import musicnn
import pandas as pd
#%%
class Featurizer:
    def __init__(self):
        pass

# for a given track, computes these features, and outputs as feature/dictionary
class FeatureSpotifyLow(Featurizer):
    def __init__(self):
        pass

class FeatureMelSpectrogram(Featurizer):
    def __init__(self):
        pass

class FeatureMusicnn(Featurizer):
    def __init__(self):
        pass
    # outputs...
        # mel spectrogram
        # tag grams
        # music nn features

class FeatureTags(Featurizer):
    def __init__(self):
        pass

class FeatureTagGrams(Featurizer):
    def __init__(self):
        pass

#%%


#%% 

import musicnn
import pandas as pd


#%%
connection2spotify = SpotifyConnector()
audio_features = connection2spotify.instance.audio_features('3oEHQmhvFLiE7ZYES0ulzv')

#%%
audio_features

#%%

# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
feature_keys = ['danceability', 'energy', 'key','loudness', 'mode','speechiness','acousticness','instrumentalness','liveliness','valence','temp']

#%%


#%%


#%%
import musicnn
from musicnn.extractor import extractor
import numpy as np

#%%
# we want to save the taggram and the penultimate layer out
# now.. we want to save the features as a dictionary.
#%%
my_user = SpotifyUserExplorer()
my_user.list_playlist_names()
test_id = my_user.get_playlist_id_from_name('nn')

#%%
my_list = TrackListSpotify()
# my_list.add_tracks_from_public_user_playlist(test_id)
my_list.add_all_tracks_from_public_user()
my_list.remove_tracks_with_missing_previews()
my_list.write_list_to_db(list_name = 'cocjin_all_v2')
my_list.populate_audio_database()

#%%


#%%
def get_features_for_track(track_id):
    mp3_path = get_track_mp3_path(track_id)
    taggram, tags, features = extractor(mp3_path, model = 'MTT_musicnn', extract_features = True)
    return {'penultimate':features['penultimate'], 'taggram': taggram}

#%% write the features to output files  
track_ids = my_list.dataframe['id'].values
features_of_tracks = {}
num_tracks = len(track_ids)
itrack = 0
for track_id in track_ids:
    itrack = itrack + 1
    print('%d out of %d'%(itrack, num_tracks))
    features_of_tracks[track_id] = get_features_for_track(track_id)
    track_path = os.path.join('/home/ubuntu/insight/data/feature_sets/musicnn_test/', track_id + '.pkl')
    with open(track_path, 'wb') as handle:
        pickle.dump(features_of_tracks[track_id], handle)

#%%
features  = [item for key, item in features_of_tracks.items()]
track_ids = [key for key, item in features_of_tracks.items()]
test_df = pd.DataFrame.from_records(features)
test_df['track_id'] = track_ids

#%% now we should try to do this... 

#%%
#%%

#%% now we have our user...
# check out our user's playlists
test_user = SpotifyUserExplorer()
test_user.list_playlist_names()

# get the playlist id of our playlist of interest
test_id = my_user.get_playlist_id_from_name('nn')

# and create a playlist from it
test_list = TrackListSpotify()
test_list.add_tracks_from_public_user_playlist(test_id)
test_list.remove_tracks_with_missing_previews()
test_features = test_list.load_features(set_name = 'musicnn_test')
#%%
# now... what we want to do is... compute the adjacency matrix for our database and our tracks
# with that playlist

#%%
my_list = TrackListSpotify()
my_list.load_list_from_db(list_name = 'cocjin_all_v2')
my_list.remove_tracks_with_missing_previews()
db_features = my_list.load_features(set_name = 'musicnn_test')

#%%
db_features   = collapse_time_in_features(db_features, ['taggram', 'penultimate'])
test_features = collapse_time_in_features(test_features, ['taggram', 'penultimate'])
#%%
X = np.vstack(db_features['mean_penultimate'].values)
Y = np.vstack(test_features['mean_penultimate'].values)

from sklearn.metrics.pairwise import pairwise_distances
metric = 'euclidean'
dmat = pairwise_distances(X = X, Y = Y, metric = 'euclidean')
# dmat = cosine_similarity(X = X, Y = Y)

# see if we can identify ourselves for each track
which_min = np.argmin(dmat, axis = 0)
print(db_features.loc[which_min, 'track_id'])
print(test_features['track_id'])

#%%
# see if we can identify ourselves given the mean of the similarity..
collapse_d = np.mean(dmat, axis = 1)
#%%
which_db_songs = np.argsort(collapse_d)[:10]
print(db_features.loc[which_db_songs,'track_id'])

#%%
print(test_features['track_id'])

#%%
pd.merge(db_features.loc[which_db_songs,'track_id'], my_list.dataframe, left_on = 'track_id', right_on = 'id')

#%%
pd.merge(db_features.loc[which_min,'track_id'], my_list.dataframe, left_on = 'track_id', right_on = 'id')

#%%
import seaborn as sns
sns.heatmap(dmat)

#%%
# more things to do!
# parallelize the feature computations

#%%
# how to do this... and what to do about this...
# let's see exactly what to do!

#%%


import multiprocessing
num_cores = multiprocessing.cpu_count()

#%%
print(num_cores)

#%%




#%%
