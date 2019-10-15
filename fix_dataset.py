#%%
import os
import pandas as pd
from src import * 
def load_benchmark_df():
    spot_data_path  = os.path.join('/home/ubuntu','insight','spot_datasets')
    benchmark_path = os.path.join(spot_data_path, 'benchmark_v2.csv') 
    benchmark_df = pd.read_csv(benchmark_path)
    return benchmark_df

def load_meta_df():
    spot_data_path  = os.path.join('/home/ubuntu','insight','spot_datasets')
    benchmark_path = os.path.join(spot_data_path, 'benchmark_final.csv') 
    benchmark_df = pd.read_csv(benchmark_path)
    return benchmark_df

def combine_track_lists(playlist_names, suffix = ''):
    df_list = []
    for playlist_name in playlist_names:
        my_list = TrackListSpotify()
        my_list.load_list_from_db(list_name=playlist_name + suffix)
        my_list.dataframe['original_list'] = playlist_name + suffix
        df_list.append(my_list.dataframe)
    return pd.concat(df_list)

def combine_playlists(playlist_names, new_playlist_name):
        cat_df = combine_track_lists(playlist_names)
        db_list = TrackListSpotify()
        db_list.set_list_name(new_playlist_name)
        db_list.dataframe = cat_df
        db_list.write_list_to_db()    

#%%
meta_df = load_meta_df()
print(meta_df.head())

#%% create single playlists from single genres
out_names  = []
categories = []
functions  = []
splits     = []

for idf in meta_df.groupby(['category', 'function', 'split']):
    print('|||'.join(idf[0]))
    name_list = list(idf[0])
    name_list[0] = name_list[0].replace('/', '-')
    out_name = '|||'.join(name_list)
    combine_playlists(idf[1].name.values, out_name)

    out_names.append(out_name)
    categories.append(idf[0][0])
    functions.append(idf[0][1])
    splits.append(idf[0][2])

category_meta_df = pd.DataFrame.from_dict({'name': out_names, 'category': categories, 'function': functions, 'split':splits})
spot_data_path  = os.path.join('/home/ubuntu','insight','spot_datasets')
category_meta_df.to_csv(os.path.join(spot_data_path, 'category_benchmark_final.csv'), index = False)

#%% create databases
for idf in category_meta_df.groupby(['function']):
    print(idf[0])
    combine_playlists(idf[1].name.values, 'categories|||' + idf[0])

#%%
pivot_category_df = category_meta_df.pivot(index = 'category',columns = 'function', values = ['name', 'split'])
pivot_category_df.reset_index(inplace = True)
pivot_category_df.columns = ['category','full','in_db','in_playlist','split','split1','split2']
pivot_category_df.drop(columns = ['split1','split2'], inplace = True)
pivot_category_df.to_csv(os.path.join(spot_data_path, 'category_benchmark_pivot.csv'), index = False)
#%%

