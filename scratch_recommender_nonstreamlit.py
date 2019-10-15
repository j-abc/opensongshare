#%%
from src import * 
import pandas as pd

my_user_id = '1240204888'

my_user_explorer = SpotifyUserExplorer(my_user_id)
my_playlists = my_user_explorer.list_playlist_names().tolist()
my_playlist_idx = 2
my_playlist_id  = my_user_explorer.get_playlist_id_from_name(my_playlists[my_playlist_idx])

# let's get our track list and add it to our audio database
my_playlist = TrackListSpotify() # initialize track list
my_playlist.add_tracks_from_public_user_playlist(my_playlist_id) # add tracks from this playlist
my_playlist.remove_tracks_with_missing_previews() # remove tracks that are missing
my_playlist.populate_audio_database() # and populate the audio database

# let's figure out how to do the taggrams for this stuff...
feat_musicnn   = FeaturizerMusicnn()
track_features = feat_musicnn.get_features_for_tracks(my_playlist.dataframe['id'])

#%% feat_musicnn.tags
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

# see if we can identify ourselves given the mean of the similarity...
collapse_d = np.mean(dmat, axis = 1)

which_db_songs = np.argsort(collapse_d)[:10]
print(db_features.loc[which_db_songs,'track_id'])
print(test_features['track_id'])

pd.merge(db_features.loc[which_db_songs,'track_id'], my_list.dataframe, left_on = 'track_id', right_on = 'id')
pd.merge(db_features.loc[which_min,'track_id'], my_list.dataframe, left_on = 'track_id', right_on = 'id')

#%%
# choose the top n tags
# show all of the song tags that we are interested in. 
# figure out how to do this...

#%%
# how would we actually label our songs? 
# can we show it in taggram space? 

#%%
db_list = TrackListSpotify()
db_list.load_list_from_db['cocjin_all_v2']

#%%