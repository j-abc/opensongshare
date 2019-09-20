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

#%% from a single user, grab a single playlist's information
def extract_playlist_info(playlist_id):
    my_playlist_dict = {}
    my_playlist_dict['id']   = playlist_id
    my_playlist_dict['data'] = spotify.user_playlist(keys['username'], my_playlist_dict['id'])
    my_playlist_dict['name'] = my_playlist_dict['data']['name']
    my_playlist_dict['total'] = my_playlist_dict['data']['tracks']['total']
    return my_playlist_dict

#%% from a single playlist, grab a single song's information
def format_song_info(track):
    my_song_dict = {}
    my_song_dict['data']          = track
    my_song_dict['artists']       = [iel['name'] for iel in my_song_dict['data']['artists']]
    my_song_dict['name']          = my_song_dict['data']['name']
    my_song_dict['id']            = my_song_dict['data']['id']
    my_song_dict['preview_url']   = my_song_dict['data']['preview_url']
    my_song_dict['uri']           = my_song_dict['data']['uri']
    del my_song_dict['data']
    return my_song_dict

#%% get instance
spotify = connect.get_spotify_instance(keys['client_id'], keys['client_secret'])
playlists = spotify.user_playlists(keys['username'])

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
import pandas as pd
songs_df = pd.DataFrame.from_dict(all_songs)
songs_df.head()

#%%
print(songs_df[~songs_df['preview_url'].isnull()].shape)
print(songs_df.shape)

#%% 
import os
import wget
songs_db_path = '/home/ubuntu/insight/data/raw/spotify_audio/mp3/'
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
#####
#####
#####
#####
#####
#####
#####
#####
#####

#%%
