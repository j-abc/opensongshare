#%%
import pandas as pd
import numpy as np
from src import *


#%%





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
