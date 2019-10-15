#%%
#### DATA LOADING
# load the data set
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

def get_track_ids(playlist_id):
    new_list = TrackListSpotify()
    new_list.load_list_from_db(list_name=playlist_id)
    track_ids = new_list.dataframe['id'].values
    return track_ids

def subsample_to_20(playlist_id):
    my_list = TrackListSpotify()
    my_list.load_list_from_db(list_name = playlist_id)
    my_list.dataframe = my_list.dataframe.iloc[:20,:]
    my_list.dataframe.reset_index(inplace = True, drop = True)
    my_list.set_list_name(list_name = playlist_id + '_to20')
    my_list.write_list_to_db()

def split_to_first10(playlist_id):
    my_list = TrackListSpotify()
    my_list.load_list_from_db(list_name = playlist_id + '_to20')
    my_list.dataframe = my_list.dataframe.iloc[:10,:]
    my_list.dataframe.reset_index(inplace = True, drop = True)
    my_list.set_list_name(list_name = playlist_id + '_to20_first10')
    my_list.write_list_to_db()

def split_to_second10(playlist_id):
    my_list = TrackListSpotify()
    my_list.load_list_from_db(list_name = playlist_id + '_to20')
    my_list.dataframe = my_list.dataframe.iloc[10:20,:]
    my_list.dataframe.reset_index(inplace = True, drop = True)
    my_list.set_list_name(list_name = playlist_id + '_to20_second10')
    my_list.write_list_to_db()

split_lists = False

if split_lists:
    playlist_ids = benchmark_df['id'].values
    ipl = 0
    for playlist_id in playlist_ids:
        ipl = ipl + 1
        print('%d out of %d'%(ipl, len(playlist_ids)))
        subsample_to_20(playlist_id)
        split_to_first10(playlist_id)
        split_to_second10(playlist_id)

def combine_track_lists(playlist_names, suffix = '_to20_second10'):
    df_list = []
    for playlist_name in playlist_names:
        my_list = TrackListSpotify()
        my_list.load_list_from_db(list_name=playlist_name + suffix)
        my_list.dataframe['original_list'] = playlist_name + suffix
        df_list.append(my_list.dataframe)
    return pd.concat(df_list)

combine_lists = True
if combine_lists:
    for suffix in ['_to20', '_to20_second10', '_to20_first10']:
        benchmark_df = load_benchmark_df()
        cat_df = combine_track_lists(benchmark_df['id'].values, suffix)
        db_list = TrackListSpotify()
        db_list.set_list_name(suffix[1:])
        db_list.dataframe = cat_df
        db_list.write_list_to_db()
        print(suffix)
        print(cat_df.shape)
#%%

# okay cool! now we have all the tracks in our three data frames
# to20_second10 - database
# to20_first10  - playlist

# let's see benchmark_df

# now what do we need to do? 
# let's figure this out...

# so... now what do we need to do? 
# we need to figure out how to optimize the weightings of each of the things... 

# def combine_track_lists(playlist_names):
    # return 

#%%
#### DATA SPLITTING
# create the train set
    # train set - 25 playlists, 10 songs held out - single genre
    # database  - 50 playlists - both train and test set database


# database:  500 songs from left out set from train and test
# train set: 40 playlists - 400 songs 
# test set:  10 playlists - 100 songs 

# 20/80 split

#%%
# load benchmark_df

### DEFINING THE PLAYLIST LISTS
# sort by category
benchmark_df = load_benchmark_df()
benchmark_df.sort_values(by = 'category', inplace = True)
benchmark_df['split']       = ['test' for i in range(10)] + ['train' for i in range(40)]
benchmark_df['in_db']       = benchmark_df['id'].apply(lambda x: x + '_to20_second10')
benchmark_df['in_playlist'] = benchmark_df['id'].apply(lambda x: x + '_to20_first10')
benchmark_df['full']        = benchmark_df['id'].apply(lambda x: x + '_to20')
benchmark_df.drop(columns = 'num_usable_songs', inplace = True)

spot_data_path  = os.path.join('/home/ubuntu','insight','spot_datasets')
benchmark_df.to_csv(os.path.join(spot_data_path, 'benchmark_v3.csv'), index = False)

#%%
final_df = benchmark_df.melt(id_vars = ['name', 'id','category','split'], var_name = 'function', value_name = 'name')

final_df.to_csv(os.path.join(spot_data_path, 'benchmark_final.csv'), index = False)

#%%
# Start with this...
# (1) 
# (2) 

#%%
# now expand out id into...
# _to20first10
# _to20second10

#%% 


#%%
# okey doke...
# now... I have the metadata frame necessary
# now I need all of the tracks to make this useful 
# snap... now how do I formulate this problem. 

#%%

# let's think for a second


#%%

# define suffix as to20_first10
# choose the first 5 categories - 10 playlists - define as test 
    # save as test_metadata.pkl
    # save as test_tracklist.pkl

# choose next 20 categories     - 40 playlists - define as train
    # save as train_metadata.pkl
    # save as train_tracklist.pkl

### DEFINING THE DATABASE



# define suffix as to20_second10

# choose all to20_second10

# concatenate into a database
    # save as opt_db_metadata.pkl
    # save as opt_db_tracklist.pkl

# for each playlist, get a ranking of the database. 

# train database:
    # 40 playlists 
# test database:

# sort by genre
    # randomly choose the genre/category 





#%%

# create the test set 
    # test set  - 25 playlists, 10 songs held out - single genre
    # database  - 50 playlists - both train and test set database

#### FORMATTING THE PROBLEM
    # predicting the song co-occurence matrix
        # build song co-occurence matrix
    # or do the tensorflow backpropagation version 
        # predict whether it belongs or not...
        # double input: 

#### AND THEN DOING THE ACTUAL TEST
    # do a single thing for each of these...

#### VISUALIZING DIMENSION - tSNE, we can do this part last. 



#%%
