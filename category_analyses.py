#%%
from src import * 
import numpy as np
import os
import pandas as pd
import timeit

def get_metrics_at_k(relevant_ids, rank_to_all_ids, k):
    # relevant ids: numpy array of ids 
    # rank_to_all_ids: dataframe of ranking for ids

    which_rows_in_ranks  = (rank_to_all_ids['rank'].values) < (k)
    subset_ranks         = rank_to_all_ids.loc[which_rows_in_ranks, :]
    subset_ids           = subset_ranks['id'].values

    id_intersection      = np.intersect1d(relevant_ids, subset_ids)

    num_relevant_found    = len(id_intersection)
    num_relevant_possible = len(relevant_ids)
    num_recommended       = k

    recall_at_k           = num_relevant_found/num_relevant_possible
    precision_at_k        = num_relevant_found/k

    return {'recall_at_k': recall_at_k, 'precision_at_k': precision_at_k,  'k':k, 'num_relevant_found': num_relevant_found, 'num_relevant_possible':num_relevant_possible}

def aggregate_results(raw_results):
    calc_results = []
    k_list = [50, 100, 500]
    idx = 0 
    for iresult in raw_results:
        idx = idx + 1
        print('%d out of %d'%(idx, len(raw_results)))

        for k in k_list:
            metrics = get_metrics_at_k(iresult['target_track_ids'], iresult['rank_id_df'], k)
            metrics['playlist_name'] = iresult['playlist_name']
            calc_results.append(metrics)

    calc_results = pd.DataFrame(calc_results)
    return calc_results.groupby('k', as_index = False).median()

def load_meta_df():
    spot_data_path  = os.path.join('/home/ubuntu','insight','spot_datasets')
    benchmark_path = os.path.join(spot_data_path, 'category_benchmark_pivot.csv') 
    benchmark_df = pd.read_csv(benchmark_path)
    return benchmark_df

def rank_across_playlists(recommender, playlist_names, target_names, db_name = 'categories|||in_db'):
    raw_results = []
    iplay = 0
    for playlist_name, target_name in zip(playlist_names, target_names):
        iplay = iplay + 1
        print('%d out of %d'%(iplay, len(playlist_names)))

        # define the database
        db_list = TrackListSpotify()
        db_list.load_list_from_db(db_name)
        database_track_ids = db_list.dataframe['id'].values

        # define our tracklist
        pl_list = TrackListSpotify()
        pl_list.load_list_from_db(playlist_name)
        playlist_track_ids = pl_list.dataframe['id'].values

        target_list = TrackListSpotify()
        target_list.load_list_from_db(target_name)
        target_track_ids = target_list.dataframe['id'].values

        rank_id_df = recommender.predict_rank(playlist_track_ids, database_track_ids)

        raw_results.append({'playlist_name':playlist_name, 'rank_id_df': rank_id_df, 'target_track_ids':target_track_ids})
    return raw_results

def get_track_ids(playlist_id):
    new_list = TrackListSpotify()
    new_list.load_list_from_db(list_name=playlist_id)
    track_ids = new_list.dataframe['id'].values
    return track_ids

def get_features(playlist_ids):
    model_types  = ['MSD_musicnn', 'MTT_musicnn']
    imodel = 0
    iplaylist = 0
    for model_name in model_types:
        imodel = imodel + 1
        for playlist_id in playlist_ids:
            iplaylist = iplaylist + 1
            print('Model %d out of %d, Playlist %d out of %d\n'%(imodel, len(model_types),iplaylist, len(playlist_ids)))
            featurizer   = FeaturizerMusicnn(model_name)
            pl_track_ids = get_track_ids(playlist_id)
            pl_features  = featurizer.get_features_for_tracks(pl_track_ids, recalculate=True)

def run_analyses_for_recommender(rec_params, playlist_names, target_names, db_name = 'categories|||in_db'):
    recommender  = Recommender(**rec_params, rank_type = 'mean', pl_centroid_type = 'None')
    print(recommender.model_type)
    print(recommender.rank_type)
    raw_results  = rank_across_playlists(recommender, playlist_names, target_names, db_name = db_name)
    results_df   = aggregate_results(raw_results)
    for key, item in rec_params.items():
        results_df[key] = [item for i in range(results_df.shape[0])]
    return results_df

#%% network parameters
# define training playlists and recommender database
meta_df = load_meta_df()
train_pl_df = meta_df#.loc[(meta_df['split'] == 'train')]
playlist_names = train_pl_df['in_playlist'].values
target_names   = train_pl_df['in_db'].values
db_name = 'categories|||in_db'

#%%
# get_features(playlist_names)
# get_features(target_names)

#%%
# define parameters for our recommenders
model_types   = ['MSD_musicnn', 'MTT_musicnn',  'MSD_vgg', 'MTT_vgg']
which_layers   = ['taggram', 'penultimate']
distance_types = ['euclidean',  'manhattan', 'cosine']

params_list = [{'model_type':model_type, 'which_layer':which_layer, 'distance_type':distance_type} for model_type in model_types for which_layer in which_layers for distance_type in distance_types]
spot_params_list = [{'model_type': 'spotify_audio','which_layer': '', 'distance_type':distance_type} for distance_type in distance_types]
rand_params_list = [{'model_type': 'randomized','which_layer': '', 'distance_type':'cosine'}]
all_params_list = params_list + spot_params_list + rand_params_list
all_params_df = pd.DataFrame(all_params_list)

#%% 
results_list = []
for i in range(all_params_df.shape[0]): # [0, all_params_df.shape[0]-1]:
    print('RECOMMENDER %d out of %d'%(i, all_params_df.shape[0]-1))
    print(all_params_df.iloc[i].to_dict())
    results_df = run_analyses_for_recommender(all_params_df.iloc[i].to_dict(), playlist_names, target_names, db_name)
    results_list.append(results_df)

all_results_df = pd.concat(results_list, ignore_index = True)
spot_data_path  = os.path.join('/home/ubuntu','insight','spot_datasets')
results_path = os.path.join(spot_data_path, 'results_cats.csv') 
all_results_df.sort_values(by = ['k','model_type'], inplace= True)
all_results_df.to_csv(results_path, index = False)

print(all_results_df)

#%%
# recommender = Recommender(model_type = 'MSD_musicnn', which_layer = 'taggram', distance_type = 'euclidean', pl_centroid_type = 'None', rank_type = 'mean')
# raw_results = rank_across_playlists(recommender, playlist_names[:5], target_names[:5])
# results_df = aggregate_results(results_df)
# print(results_df)

#%%
