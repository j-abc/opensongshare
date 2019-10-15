#%%
import numpy as np
import pandas as pd

#%%
import os
spot_data_path  = os.path.join('/home/ubuntu','insight','spot_datasets')
categories_path = os.path.join(spot_data_path, 'custom_dataset_categories.txt')
metadata_path   = os.path.join(spot_data_path, 'custom_dataset_info.json')

categories = [line.rstrip('\n') for line in open(categories_path)]

#%%
from src import *

#%%
user_id = '6fvjc6dmcplc3d3lkaaa59k9v'
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


