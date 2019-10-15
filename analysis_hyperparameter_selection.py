#%% Create the playlists database


#%%
from src import * 

import os
spot_data_path  = os.path.join('/home/ubuntu','insight','spot_datasets')
categories_path = os.path.join(spot_data_path, 'custom_dataset_categories.txt')
metadata_path   = os.path.join(spot_data_path, 'custom_dataset_info.json')
categories = [line.rstrip('\n') for line in open(categories_path)]

# load up my user
user_id = '6fvjc6dmcplc3d3lkaaa59k9v'
user_explorer = SpotifyUserExplorer(user_id)
playlist_names = user_explorer.list_playlist_names().tolist()
playlist_ids = [user_explorer.get_playlist_id_from_name(playlist_name) for playlist_name in playlist_names]

format_categories = []
for i in categories:
    format_categories = format_categories + [i]
    format_categories = format_categories + [i]
print(format_categories)
format_categories = format_categories[::-1]

# load our playlists
benchmark_df = pd.DataFrame.from_dict({'name':playlist_names, 'id':playlist_ids, 'category':format_categories})

#%%

benchmark_path = os.path.join(spot_data_path, 'benchmark.csv') 
benchmark_df.to_csv(benchmark_path, index = False)

#%%
import os
import pandas as pd
spot_data_path  = os.path.join('/home/ubuntu','insight','spot_datasets')
benchmark_path = os.path.join(spot_data_path, 'benchmark.csv') 
benchmark_df = pd.read_csv(benchmark_path)
from src import * 

def get_playlist_len(playlist_id):
    my_list = TrackListSpotify()
    my_list.load_list_from_db(list_name = playlist_id)
    return my_list.dataframe.shape[0]

# print(get_playlist_len(benchmark_df.loc[0,'id']))
benchmark_df['num_usable_songs'] = benchmark_df['id'].apply(get_playlist_len)
benchmark_df = benchmark_df.loc[benchmark_df['num_usable_songs'] >= 20]
benchmark_df.to_csv(os.path.join(spot_data_path, 'benchmark_v2.csv'), index = False)

#%%
import os
import pandas as pd
spot_data_path  = os.path.join('/home/ubuntu','insight','spot_datasets')
benchmark_path = os.path.join(spot_data_path, 'benchmark.csv') 
benchmark_df = pd.read_csv(benchmark_path)
from src import * 

#%%
def get_playlist_len(playlist_id):
    my_list = TrackListSpotify()
    my_list.load_list_from_db(list_name = playlist_id)
    return my_list.dataframe.shape[0]

# print(get_playlist_len(benchmark_df.loc[0,'id']))
benchmark_df['num_usable_songs'] = benchmark_df['id'].apply(get_playlist_len)

benchmark_df.loc[benchmark_df['num_usable_songs'] < 20]
#%%
#%%
user_id = '6fvjc6dmcplc3d3lkaaa59k9v'
# playlist_id = '37i9dQZF1DX9hWdQ46pHPo'
# playlist_id = '37i9dQZF1DWXcOHfWefCtg'
playlist_id = '37i9dQZF1DX3Xgp6iJAFjW'
test_list = TrackListSpotify()
test_list.add_tracks_from_public_user_playlist(playlist_id = playlist_id, user = user_id)
test_list.remove_tracks_with_missing_previews()
test_list.remove_duplicate_tracks()
#%%
test_list.set_list_name(playlist_id)
test_list.write_list_to_db()
test_list.populate_audio_database()
#%%
test_list.dataframe = test_list.dataframe.iloc[:25]
#%%
test_list.write_list_to_db()
#%%
new_list = TrackListSpotify()
new_list.load_list_from_db(list_name=playlist_id)
new_list.dataframe
#%%
#%%
def get_track_ids(playlist_id):
    new_list = TrackListSpotify()
    new_list.load_list_from_db(list_name=playlist_id)
    track_ids = new_list.dataframe['id'].values
    return track_ids
    
playlist_ids = ['37i9dQZF1DX3Xgp6iJAFjW','37i9dQZF1DX9hWdQ46pHPo']
model_types  = ['MTT_musicnn', 'MTT_vgg', 'MSD_musicnn', 'MSD_vgg']
imodel = 0
iplaylist = 0
for model_name in model_types:
    imodel = imodel + 1
    for playlist_id in playlist_ids:
        iplaylist = iplaylist + 1
        print('Model %d out of %d, Playlist %d out of %d\n'%(imodel, len(model_types),iplaylist, len(playlist_ids)))
        featurizer   = FeaturizerMusicnn(model_name)
        pl_track_ids = get_track_ids(playlist_id)
        pl_features  = featurizer.get_features_for_tracks(pl_track_ids)

#%%




#%%
import numpy as np
import pandas as pd

#%%

#%%
from src import *

#%%

user_explorer = SpotifyUserExplorer(user_id)
playlist_names = user_explorer.list_playlist_names().tolist()
playlist_ids = [user_explorer.get_playlist_id_from_name(playlist_name) for playlist_name in playlist_names]

pl2tl = {}
ip = 0
for playlist_id in playlist_ids:
    ip = ip + 1
    print('PLAYLIST %d out of %d'%(ip, len(playlist_ids)))
    pl2tl[playlist_id] = TrackListSpotify(user = user_id)
    pl2tl[playlist_id].add_tracks_from_public_user_playlist(playlist_id)
    pl2tl[playlist_id].remove_tracks_with_missing_previews()
    pl2tl[playlist_id].remove_duplicate_tracks()
    pl2tl[playlist_id].write_list_to_db(list_name = playlist_id)
    pl2tl[playlist_id].populate_audio_database()

#%%
# pl2lengths = [tl.dataframe.shape[0] for tl, keys in pl2tl.items()]
#%%
pl2lengths = [pl2tl[key].dataframe.shape[0] for key in pl2tl.keys()]
np.sum(pl2lengths)
#%%
#%%
model_types  = ['MTT_musicnn', 'MTT_vgg', 'MSD_musicnn', 'MSD_vgg']
imodel = 0
iplaylist = 0
for model_name in model_types:
    imodel = imodel + 1
    for playlist_id in playlist_ids:
        iplaylist = iplaylist + 1
        print('Model %d out of %d, Playlist %d out of %d\n'%(imodel, len(model_types),iplaylist, len(playlist_ids)))
        featurizer   = FeaturizerMusicnn(model_name)
        pl_track_ids = pl2tl[playlist_id].dataframe['id'].values
        pl_features  = featurizer.get_features_for_tracks(pl_track_ids)

#%%
# okay... so we should probably... featurizer all this stuff!

#%%
# 50 playlists available now! 

#%%
# what are we going to do with the playlists? 
# check how mnay songs are in each playlist


#%%


