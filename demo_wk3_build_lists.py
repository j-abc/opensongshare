#%% grab all of our public tracks with me as user 
from src import * 

def define_database(database_name, user):
    db_list = TrackListSpotify()
    db_list.add_all_tracks_from_public_user(user=user)
    #%% annnnd remove tracks with missing previews...
    db_list.remove_tracks_with_missing_previews()
    db_list.remove_duplicate_tracks()
    #%% save it out for our personal use!
    db_list.write_list_to_db('demo_week_3')
    #%% how many songs do we have? 
    db_list.dataframe.shape
    #%% let's add our songs to the database
    db_list.populate_audio_database()
    return db_list

db_list = define_database('justin_db', user = '12125883155')

# norf norf

#%% and featurize them!

track_ids = db_list.dataframe['id'].values
print(track_ids)
#%%
model_types = ['MTT_musicnn']#, 'MTT_vgg', 'MSD_musicnn', 'MSD_vgg']
imodel = 0

for model_name in model_types:
    ifeat = FeaturizerMusicnn(model_name)
    imodel = imodel + 1
    itrack = 0 
    for track_id in track_ids:
        itrack = itrack + 1
        print('%d out of %d; %d out %d\n'%(itrack, len(track_ids),imodel, len(model_types)))
        ifeat.get_features_for_track(track_id)
 
#%%
from src import * 
playlist = TrackListSpotify(user = '12125883155')
user     = SpotifyUserExplorer(user = '12125883155')
playlist_id = user.get_playlist_id_from_name('Get Mad')
playlist.add_tracks_from_public_user_playlist(playlist_id)
playlist.remove_tracks_with_missing_previews()
playlist.remove_duplicate_tracks()
playlist.populate_audio_database()
playlist.write_list_to_db('justin_go')
#%% save it out for our personal use!
# playlist = TrackListSpotify()
# user     = SpotifyUserExplorer()
# playlist_id = user.get_playlist_id_from_name('demo')
# playlist.add_tracks_from_public_user_playlist(playlist_id)
# playlist.remove_tracks_with_missing_previews()
# playlist.remove_duplicate_tracks()
# playlist.populate_audio_database()

#%% how many songs do we have? 
playlist.dataframe.shape
#%% let's add our songs to the database
model_types  = ['MTT_musicnn', 'MTT_vgg', 'MSD_musicnn', 'MSD_vgg']
model_name   = model_types[0]
featurizer   = FeaturizerMusicnn(model_name)

pl_track_ids = playlist.dataframe['id'].values
db_track_ids = db_list.dataframe['id'].values

pl_features  = featurizer.get_features_for_tracks(pl_track_ids)
db_features  = featurizer.get_features_for_tracks(db_track_ids)

#%%
import pandas as pd
pl_feat_df   = pd.DataFrame.from_records(pl_features)
db_feat_df   = pd.DataFrame.from_records(db_features)

#%% 
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np

def rank_db_from_playlist(pl_feat_df, db_feat_df, db_list_df, feature_name = 'taggram', metric = 'euclidean', num_songs = 20): 
        pl_feat_array = np.vstack(pl_feat_df[feature_name].values)
        db_feat_array = np.vstack(db_feat_df[feature_name].values)

        dmat = pairwise_distances(X = db_feat_array, Y = pl_feat_array, metric = metric)

        collapse_dmat = np.mean(dmat, axis = 1)
        print(collapse_dmat.shape)

        sorted_db_idx = np.argsort(collapse_dmat)
        # sorted_db_idx = sorted_db_idx[::-1] # turn on for euclidean to get worst songs
        # top 5 and bottom 5 - and user assessment
        which_db_songs = sorted_db_idx[:num_songs]

        return pd.merge(db_feat_df.loc[which_db_songs, 'id'], db_list_df, on = 'id')

test = rank_db_from_playlist(pl_feat_df, db_feat_df, db_list.dataframe)

print(test.loc[:,'name'].values)
print(playlist.dataframe.loc[:,'name'].values)


#%% 
# db_feats, playlist_feats = extract_features(db_track_ids, playlist_track_ids, featurizer)
# sim_mat                  = compose_similarity_matrix(db_feats, playlist_feats, similarity_measure)
# db_rankings              = rank_from_similarity_matrix(sim_mat)

#%%
pd.merge(db_features.loc[which_db_songs,'track_id'], my_list.dataframe, left_on = 'track_id', right_on = 'id')

#%%
pd.merge(db_features.loc[which_min,'track_id'], my_list.dataframe, left_on = 'track_id', right_on = 'id')
