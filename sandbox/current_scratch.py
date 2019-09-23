#%%
# load our keys of interest
import json
keys_json_path = '/home/ubuntu/insight/keys.json'
with open(keys_json_path) as json_file:
    keys = json.load(json_file)

#%%
import sys
from os.path import dirname, realpath

file_path = realpath('/home/ubuntu/insight/songfinder/sandbox/')
dir_of_file = dirname(file_path)
# parent_dir_of_file = dirname(dir_of_file)
sys.path.insert(0, dir_of_file)

#%%
from songfinder.src import connect


#%% get instance
spotify = connect.get_spotify_instance(keys['client_id'], keys['client_secret'])

all_playlists  = []
all_songs      = []
for iplaylist in playlists['items']:
    my_playlist_dict = extract_playlist_info(iplaylist['id'])
    all_playlists.append(my_playlist_dict)
    print(my_playlist_dict['total'])
    idx = 0 
    for isong in my_playlist_dict['data']['tracks']['items']:
        all_songs.append(format_song_info(isong['track']))
        idx = idx + 1
        print('%d out of %d'%(idx, my_playlist_dict['total']))

#%%
spotify.recommendation_genre_seeds()

#%%
# do this...
import pandas as pd
songs_df = pd.DataFrame.from_dict(all_songs)
songs_df.head()

#%%
# drop duplicates
songs_df.drop_duplicates(subset='id', inplace = True)

#%%
# check the data shapes
print(songs_df[~songs_df['preview_url'].isnull()].shape)
print(songs_df.shape)

#%% 
# download the data

preview_songs_df = songs_df[~songs_df['preview_url'].isnull()]
for index, row in preview_songs_df.iterrows():
    print(row['preview_url'])
    try:
        mp3_name = '-'.join(row['artists'])+ '_' + row['name'] + '.mp3'
        mp3_path = os.path.join(songs_db_path, mp3_name)
        wget.download(row['preview_url'],mp3_path)
    except:
        print(mp3_name)

#%%

# https://en.wikipedia.org/wiki/Extract,_transform,_load
    # extracter - reading from spotify
        # extracter class - pulls from spotify
            # passes song object to the loader
            # file name of song...
    # loader writes into the database - writes to s3
        # passes it off

# user reading from database
    # don't want to combine the customer using the system

# PROGRAMMING STYLE to look into: active records


#%%

#%% 

def Songs


#%%
class song_list_def:    
    def __init__(self):
        self.list_path = ''
        # check if list_path exists already
        # if it exists, load the list

    def load_list(self, list_name): 
        return 1

    def add_song(song_title, song_id):
        # check if the song exists in spotify???
        self.song_list.append([song_title, song_id])

    def check_songs(self, song_list):
        return blah 

    def check_song_previews(self, song_list):
        return has_previews

    def clean_songs(self, song_list, inplace = False):
        clean_song_list = song_list
        if inplace:
            self.song_list = clean_song_list
        return clean_song_list

    def add_to_dataset(self, dataset_path):
        # will try to add songs that work or not 
#%%
# class song_list_maker
    # params:
        # list of songs
        # clean_song_list
    # methods:
        # __init__
        # check_songs
        # check_songs_previews
        # get_as_dataframe
        # interfaces with the spotify object

# class db_billboard_list_maker(song_list_maker)
# class db_spotify_list_maker(song_list_maker)
# class spotify_user_playlist_maker(song_list_maker)
# class input_user_playlist_maker(song_list_maker)

# class dataset_spotify_audio
    # params:
        # base_folder_path
        # num_songs
        # num_artists
        # has_loaded
        # dataset_name
    # public methods:
        # def insert_song
        # def list_songs_by_artist
        # def list_artists
        # def num_entries
        # def load_meta_dataframe
        # def get_meta_dataframe
        # def load_song
    # __init__(self, location)

# class file_manager_features
    # params:
        # base_features_path
        # feature_params
        # feature_name
        # feature_calculator_name
        # num_songs
        # num_artists
        # has_loaded
        # dataset_name
    # public methods:
        # def featurize_song
        # def load_song_features
        # def load_songs_features


# class recommender

#####
# 

#####
# 

#####

#####

#####

#####

#####

#####

######%%