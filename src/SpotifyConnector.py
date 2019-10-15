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

class SpotifyConnector:
    # intialize the connector
    def __init__(self, client_id = None, client_secret = None, user = None):
        # Class for connecting to spotify through spotipy 
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
        return playlist_info

    # hidden helper methods
    def __get_instance(self, client_id, client_secret):
        # Get a Spotify instance that can pull information from the Spotify API.
        
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
