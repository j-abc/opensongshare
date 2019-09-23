#%%
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
    keys_json_path = '/home/ubuntu/insight/keys.json'
    with open(keys_json_path) as json_file:
        keys = json.load(json_file)

    # intialize the connector
    def __init__(self, client_id = None, client_secret = None, user = None):
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
        return self.instance.user_playlists(user)
    def get_public_user_playlist_ids(self, user = None):
        playlists = self.get_public_user_playlists(user = user)
        return [iplaylist['id'] for iplaylist in playlists['items']]  
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
        return [self._format_track_info(itrack )for itrack in tracks]
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
class SpotifyUserExplorer:
    def __init__(self):
        pass

#%% For creating lists of data... basically.. track lists lol 
class TrackList:
    def __init__(self):
        self.dataframe = []
        pass
    def add_to_audio_db(self):
        pass
    # def spotify_id_from_names(self, song_names, artist_names):
    #     pass
    def remove_missing_previews(self, inplace = False):
        pass
    def write_to_df(self, list_db, list_name):
        # pd.to_pickle()
        pass
    def load_from_df(self, list_db, list_name):
        # pd.read_pickle
        pass
    def combine_track_lists(self, lists):
        pass

#%%
test_list = TrackList()
#%%
class TrackListSpotify(TrackList):
    def __init__(self):
        # dataframe contains
            # track_id, artist_id, playlist_id, user_id, track_name, playlist_name, etc. 
        pass

    # add songs from different spotify sources
    def add_from_public_user_playlist(self, playlist_id, user = None):
        # adds songs from this user playlist
        return 1

    def add_from_public_user_playlists(self, playlist_ids, user = None):
        # add songs from multiple playlists
        return 1

    def add_from_public_user_all(self, user = None):
        return 1
    
    def combine_lists(self, all_lists)

    # save information out to a dataframe!
        # what do we want to call this one? 


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