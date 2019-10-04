#%%
import pandas as pd
import numpy as np
from src import *

#%%
import tensorflow as tf

#%%
labels = [0, 1, 2, 3, 4]
predictions_idx = [[1,0,0,0,0], [0,1,0,0,0],[0,0,1,0,0], [0,0,0,0,1,0], [0,0,0,0,0,1]]
tf.metrics.precision_at_top_k(labels, predictions_idx)

#%%
import numpy as np

#%%
relevant_ids    = np.array(['0','1','2','3','4'])
ranks           = [0,1,2,3,4,5,6,7,8,9]
db_ids          = [str(i) for i in ranks]
rank_to_all_ids = pd.DataFrame.from_dict({'rank':ranks, 'id': db_ids})
k = 10

#%%

#%%
# some other things to check: sparsity of the genre labels

# another way to see it is...

# HELD OUT SET, PLAYLISTS INPUT:
# tracklist_name, track_id

# DATABASE:
# track_id

# PREDICTIONS TO RUN:
# for each tracklist, get ranked order of the database

# PREDICTIONS OUTPUT:
# track_id, tracklist_id (taken from), ranking

# PER TRACKLIST RESULTS
# tracklist_name, db_name, recall_at_k, precision_at_k, k, num_relevant_found, num_relevant_possible

# OVERALL AGGREGATED RESULTS
# average precision at k over tracklists
# average recall at k over tracklists

def get_tracklist_with_tracks_df(tracklist_names):
    # loads all the track_ids from tracklist_names
    return out_df
    

def get_metrics_at_k(relevant_ids, rank_to_all_ids, k):
    # relevant ids: numpy array of ids 
    # rank_to_all_ids: dataframe of ranking for ids

    which_rows_in_ranks  = rank_to_all_ids['rank'].values < (k- 1)
    subset_ranks         = rank_to_all_ids.loc[which_rows_in_ranks, :]
    subset_ids           = subset_ranks['id'].values

    id_intersection      = np.intersect1d(relevant_ids, subset_ids)

    num_relevant_found    = len(id_intersection)
    num_relevant_possible = len(relevant_ids)
    num_recommended       = k

    recall_at_k           = num_relevant_found/num_relevant_possible
    precision_at_k        = num_relevant_found/k

    return {'recall_at_k': recall_at_k, 'precision_at_k': precision_at_k,  'k':k, 'num_relevant_found': num_relevant_found, 'num_relevant_possible':num_relevant_possible}

get_metrics_at_k(relevant_ids, rank_to_all_ids, k)
 

#%%
def metrics_at_k(relevant_ids, rank_to_all_ids, k):
    # inputs: 
    #   held out track ids 
    #   rank-to-track_id list 
    #   k = how many rankings to consider

    # outputs:
    #   precision at k: 
    #   recall at k: 
    #   RMSE: 
    
    # filter rank-to-track-id by rank
    # choose the top k out of database

    # calculate precision 
    # number of recommended items @k that are relevant
    # div
    # number of recommended items

    # calculate recall
    # recommended items at k 
    # div
    # total relevant items
    


    return {'precision': 0, 'recall': 0}

def precision:
    pass

def recall:
    pass

#%%
user = SpotifyUserExplorer()
playlist_id = user.get_playlist_id_from_name('nn')

tracklist = TrackListSpotify()
tracklist.add_tracks_from_public_user_playlist(playlist_id)
tracklist.remove_tracks_with_missing_previews()
tracklist.remove_duplicate_tracks()

track_id = tracklist.dataframe['id'].values[0]
featurizer = FeaturizerSpotify()
featurizer.get_features_for_track(track_id, recalculate = True)


#%%

#%%
# https://github.com/ocelma/python-recsys

#%%
#%%
recommender = Recommender(**params)
recommender.predict_rank(playlist_track_ids, database_track_ids)

#%%
def predict_rank(playlist_track_ids, database_track_ids):
    
# extract playlist and database features 

# cluster the database if desired
if not(db_centroid_type == 'None'):
    db_feat_array = get_database_centroids(db_feat_array, db_centroid_type = db_centroid_type)

# get the ranking from distances
rank2dbidx = dist2rank(pl_feat_array, db_feat_array, distance_type = distance_type, ranking_type = ranking_type)

sorted_ids = database_track_ids[rank2dbidx]
ranks      = [i+1 for i in range(len(sorted_id))]
# database_track_ids  = np.array([50,55,58,59,53])
# rank2dbidx = np.array([0,3,4,1,2])
sorted_ids = database_track_ids[rank2dbidx]
ranks      = [i + 1 for i in range(len(sorted_ids))]

rank_with_ids_df = pd.DataFrame.from_dict({'id' : sorted_ids, 'rank' : ranks})
return rank_with_ids_df

#%%
def get_database_centroids(db_feat_array, db_centroid_type):
    if db_centroid_type == 'mean':
        return np.mean(db_feat_array, axis = 0)[:,np.newaxis]
    if db_centroid_type == 'k2':
        if db_feat_arary.shape[0] > 1:
            clustering = KMeans(n_cluster = 2, random_state = 0).fit(db_feat_array)
            return clustering.cluster_centers_
        else:
            raise Exception('need >= 2 data points in database.')
    if db_centroid_type == 'k3':
        if db_feat_arary.shape[0] > 2:
            clustering = KMeans(n_cluster = 3, random_state = 0).fit(db_feat_array)
            return clustering.cluster_centers_
        else:
            raise Exception('need >= 3 data points in database.')
    return reduced_db_feat_array

def dist2rank(pl_feat_array, db_feat_array, distance_type, ranking_type):
    dmat = pairwise_distances(X = db_feat_array, y = pl_feat_array, metric = distance_type)
    
    # collapse the distance 
    collapse_dfun = {'mean': np.mean,
                     'single': np.max,
                     'complete': np.min}
    collapse_dmat = collapse_dfun[ranking_type](dmat, axis = 1)
    
    # sort and put out the ranking 
    sorted_db_idx = np.argsort(collapse_dmat)

    if distance_type == 'euclidean':
        sorted_db_idx = sorted_db_idx[::-1]

    return sorted_db_idx

# get distance matrix
# get the minimum
# get the mean
# get the max
