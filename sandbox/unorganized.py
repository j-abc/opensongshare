import pandas as pd
import numpy as np
import os.path as path
import spotipy.util as su
import argparse
import librosa
import itertools
import logging
import os
import pickle
import random
import spotipy
import sys
import time
import wget
import json

#%% For connecting to spotify instance; mainly composed of convenience methods
class SpotifyConnector:
    # intialize the connector
    def __init__(self, client_id = None, client_secret = None, user = None):
        keys_json_path = '/home/ubuntu/insight/keys.json'
        with open(keys_json_path) as json_file:
            self.keys = json.load(json_file)

        self.instance = self.__get_instance(self.keys['client_id'], self.keys['client_secret'])

        if user == None:
            self.user     = self.keys['default_user'] # set default user
        else: 
            self.user = user

    # change which user we are looking at
    def set_current_user(self, user):
        self.user = user

    ### PLAYLISTS FROM USER
    def get_public_user_playlists(self, user = None):
        # get playlists from a user, if user not provided, user the default
        if user == None:
            user = self.user
        return self.instance.user_playlists(user)['items']
    def get_public_user_playlist_ids(self, user = None):
        playlists = self.get_public_user_playlists(user = user)
        return [iplaylist['id'] for iplaylist in playlists]  
    def get_public_user_playlists_formatted(self, user = None):
        playlists = self.get_public_user_playlists(user = user)
        return [self._format_playlist_info(iplaylist) for iplaylist in playlists]
    def get_public_user_tracks_formatted(self, user = None):
        playlist_ids = self.get_public_user_playlist_ids(user = user)
        tracks = []
        for iid in playlist_ids:
            tracks = tracks + self.get_tracks_from_playlist_formatted(iid, user = user)
        return tracks

    ### TRACKS FROM PLAYLIST
    def get_tracks_from_playlist(self, playlist_id, user = None):
        if user == None:
            user = self.user
        playlist = self.instance.user_playlist(user, playlist_id)
        return [item['track'] for item in playlist['tracks']['items']]
    def get_tracks_from_playlist_formatted(self, playlist_id, user = None):
        if user == None:
            user = self.user
        tracks = self.get_tracks_from_playlist(playlist_id, user = user)
        return [self._format_track_info(itrack) for itrack in tracks]
    def get_track_ids_from_playlist(self, playlist_id, user = None):
        if user == None:
            user = self.user
        tracks = self.get_tracks_from_playlist(playlist_id = playlist_id, user = user)
        return [itrack['id'] for itrack in tracks]

    ### TRACKS FROM IDS
    def get_track_from_id(self, track_id):
        return self.instance.track(track_id)
    def get_track_from_id_formatted(self, track_id):
        track = self.get_track_from_id(track_id)
        return self._format_track_info(track)
    def get_tracks_from_ids(self, track_ids):
        return self.instances.tracks(track_ids)
    def get_tracks_from_ids_formatted(self, track_ids):
        tracks = get_tracks_from_ids(track_ids)
        return [self._format_track_info(track) for track in tracks]

    ### FORMAT INFO
    def _format_track_info(self, track):
        track_info = {}
        track_info['artist_names']  = [iartist['name'] for iartist in track['artists']]
        track_info['artist_ids']    = [iartist['id'] for iartist in track['artists']]
        track_info['name']          = track['name']
        track_info['id']            = track['id']
        track_info['preview_url']   = track['preview_url']
        track_info['uri']           = track['uri']
        return track_info

    def _format_playlist_info(self, playlist):
        playlist_info       = playlist
        # ['id']
        # ['name']
        # ['tracks']['total']
        return playlist_info

    # hidden helper methods
    def __get_instance(self, client_id, client_secret):
        """Get a Spotify instance that can pull information from the Spotify API.

        Args:
            client_id (str): Client ID for accessing Spotify API.
            client_secret (str): Secret client ID (key) for accessing Spotify API.

        Returns:
            S: A Spotify instance that can be used to query the Spotify API.
        """
        token = su.oauth2.SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        cache_token = token.get_access_token()
        try:
            S = spotipy.Spotify(cache_token)
        except SpotifyOauthError:
            logging.exception('Make sure you are using the right Spotify \
                            credentials.')
        return S

#%% For connecting to spotify audio database on local computer
class DatabaseSpotifyAudio:
    # update the dataframe with this information
            # dataframe has what fields? 
                # track_id
                # track_name
                # artist_names
                # artist_ids
                # preview_url
                # preview_mp3_path
    def __init__(self):
        self.audio_db_path = '/home/ubuntu/insight/data/raw/spotify_audio/mp3/'
        self.connection2spotify = SpotifyConnector() 
    def insert_track_from_id(self, track_id):
        mp3_name = track_id + '.mp3'
        mp3_path = os.path.join(self.audio_db_path, mp3_name)
        track_info = self.connection2spotify.get_track_from_id_formatted(track_id)
        if not track_info['preview_url']:
            return False
        if not os.path.exists(mp3_path):
            wget.download(track_info['preview_url'], mp3_path)
        return True

#%% For exploring a spotify user - don't really care about this one right now

#%%


#%%
 #%%   
    # def write_to_df(self, list_db, list_name):
    #     # pd.to_pickle()
    #     pass
    # def load_from_df(self, list_db, list_name):
    #     # pd.read_pickle
    #     pass
    # def combine_track_lists(self, lists):
    #     pass

#%%
test_list = TrackList()

#%% For creating lists of data... basically.. track lists lol 
class SpotifyUserExplorer:
    def __init__(self, user = None):
        self.connection2spotify = SpotifyConnector(user = user)
        self.playlist_df   = pd.DataFrame.from_records(self.connection2spotify.get_public_user_playlists_formatted())
    def list_playlist_names(self):
        return self.playlist_df.loc[:, 'name'].values
    def get_playlist_id_from_name(self, name):
        playlist_id = self.playlist_df.loc[self.playlist_df['name'].str.match(name),'id'].values
        if len(playlist_id) > 1:
            print('more than one playlist matches this name')
            return False
        else: 
            return playlist_id[0]

class TrackList:
    def __init__(self):
        self.dataframe = []

    def add_to_audio_db(self):
        pass
    # def spotify_id_from_names(self, song_names, artist_names):
    #     pass
    def remove_missing_previews(self, inplace = False):
        pass

class TrackListSpotify(TrackList):
    def __init__(self, user = None):
        super(TrackList, self).__init__()
        self.connection2spotify = SpotifyConnector(user = user)
        self.dataframe          = pd.DataFrame(columns = ['artist_names', 'artist_ids', 'name','id','preview_url','uri', 'playlist_id'])
        self.list_db_path       = '/home/ubuntu/insight/data/raw/lists_spotify/'
        self.list_name          = None

    def add_all_tracks_from_public_user(self, user = None):
        sublist_df = pd.DataFrame.from_records(self.connection2spotify.get_public_user_tracks_formatted(user = user))
        if user == None:
            user = self.connection2spotify.user
        sublist_df['playlist_id'] = sublist_df.shape[0]*['[all][' + user + ']']
        self.dataframe = self.dataframe.append(sublist_df)

    def add_tracks_from_public_user_playlist(self, playlist_id, user = None):
        sublist_df = pd.DataFrame.from_records(self.connection2spotify.get_tracks_from_playlist_formatted(playlist_id = playlist_id, user = user))
        if user == None:
            user = self.connection2spotify.user
        sublist_df['playlist_id'] = sublist_df.shape[0]*['[' + playlist_id + ']' + '[' + user + ']']
        self.dataframe = self.dataframe.append(sublist_df)

    def load_list_from_db(self, list_name = None):
        if list_name == None:
            list_name = self.list_name
        else:
            self.list_name = list_name
        self.dataframe = pd.read_pickle(os.path.join(self.list_db_path, self.list_name + '.pkl'))

    def set_list_name(self, list_name = None):
        self.list_name = list_name

    def write_list_to_db(self, list_name = None):
        if list_name == None:
            list_name = self.list_name
        else:
            self.list_name = list_name
        self.dataframe.to_pickle(os.path.join(self.list_db_path, self.list_name + '.pkl'))

    def populate_audio_database(self):
        db_audio = DatabaseSpotifyAudio()
        track_id_list = self.dataframe.loc[:,'id'].values
        num_tracks = len(track_id_list)
        itrack = 0
        for track_id in track_id_list:
            db_audio.insert_track_from_id(track_id) 
            itrack = itrack  + 1
            print('%d out of %d\n'%(itrack, num_tracks))

    # def combine_lists(self, all_lists):
    #     pass

    # # add songs from different spotify sources
    # def add_from_public_user_playlist(self, playlist_id, user = None):
    #     # adds songs from this user playlist
    #     return 1

    # save information out to a dataframe!
        # what do we want to call this one? 

#%%
class TrackListBillboards:
    def __init__(self):
        pass

#%% Demonstration of utility 
# get a track 
spot_conn    = SpotifyConnector()
tracks       = spot_conn.get_public_user_tracks_formatted()
print(tracks[0]['id'])

# and put it into the database!
db_audio = DatabaseSpotifyAudio()
db_audio.insert_track_from_id(tracks[0]['id'])


#%% EXAMPLE OF HOW TO USE SPOTIFYCONNECTOR CLASS
# here, we instantiate our spotify connector... and get all the tracks of a given user as a set of records

# class DatasetSpotifyAudio
# params: 
    # base_folder_path: where the dataset is stored...
    # dataset_name 
    # num_songs
    # num_artists
    # has_loaded
    # df (dataframe of the audio)

# def __init__(self):
    # loads our dataset

# def list_tracks
# def list_artists
# def num_entries

#%%
# SpotifyTracksList...
# what does this do? 
# it... 
class SpotifyTracksList:

class SpotifySongsList:
    # operate by song uris
    def __init__(self):
        self._data = 
#%%
test_ssl = SpotifySongsList()

#%% 
# now... how to download and store audio... need to figure this out...

#%% 

#%%
# getting feature sets on mp3s
# featurizer


#%%
class Featurizer:
    def __init__(self):
        pass

class FeatureSpotifyLow(Featurizer):
    def __init__(self):
        pass

class FeatureMelSpectrogram(Featurizer):
    def __init__(self):
        pass

class FeatureMusicnn(Featurizer):
    def __init__(self):
        pass
    # outputs...
        # mel spectrogram
        # tag grams
        # music nn features

class FeatureTags(Featurizer):
    def __init__(self):
        pass

class FeatureTagGrams(Featurizer):
    def __init__(self):
        pass