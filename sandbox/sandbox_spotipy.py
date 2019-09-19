# NOTE TO SELF: this was run at the top level insight directory

#%% 
import spotipy
import os
import pkgs.autoencoda.autoencoda as ae
import pandas as pd

#%%
keys_path = os.path.join('~','insight','keys.csv')
keys_df   = pd.read_csv(keys_path)
spotify = ae.ingest.get_spotify_instance(keys_df.loc[0,'CLII'], keys_df.loc[0,'CLIS'])
track_URI, artist_URI = ae.ingest.get_spotify_from_billboard('Honey', 'Kehlani', spotify)

#%%
client_id =     keys_df.loc[0, 'CLII']
client_secret = keys_df.loc[0, 'CLIS']

print(client_id)
print(client_secret)

client_id = 'f4da1be5057a4796ac743a3250d44499'
client_secret = 'fce65c0cf3204ba8932fd66e36e6b607'
#%%
dir(spotify)
#%%
def build_track(track_URI, artist_URI, spotify, dir_mp3):
  track_info_from_spotify = spotify.track(track_URI)
  track = {
      'track_id': track_URI,
      'artist_id': artist_URI,
      'info': track_info_from_spotify
  }
  return track


#%%


#%%
help(spotify)

#%%
keys_df

#%%
dir(spotify)
# tracks = spotify.current_user_saved_tracks(limit = 50)

#%%
spotify.artist_top_tracks('Lenka')
#%%
# token = util.prompt_for_user_token(username, scope)

#%%
spotify = ae.ingest.get_spotify_instance(keys_df.loc[0,'CLII'], keys_df.loc[0,'CLIS'])

#%%
dir(spotify)
username = [input here]
spotify.user(user = username)
#%%
playlists = spotify.user_playlists(username)
#%%
# how to get spotify playlist id
test_playlist_meta = playlists['items'][0]
test_playlist = spotify.user_playlist(username, test_playlist_meta['id'])
#%%
test_song = test_playlist['tracks']['items'][0]
test_song_id = test_song['track']['id']
print(test_song_id)

#%%
spotify.track(test_song_id)['preview_url']
#%%
test_song_track = spotify.track(test_song_id)
test_song_track.keys()
#%%
import spotipy
client_id = 'f4da1be5057a4796ac743a3250d44499'
client_secret = 'fce65c0cf3204ba8932fd66e36e6b607'
username = '1240204888'
redirect_uri = 'localhost'
redirect_uri = 'http://localhost:8888/callback/'
token = spotipy.util.prompt_for_user_token(username, client_id = client_id, client_secret = client_secret, scope = 'playlist-read-private', redirect_uri = redirect_uri)
sp = spotipy.Spotify(auth = token)

spotify = ae.ingest.get_spotify_instance(keys_df.loc[0,'CLII'], keys_df.loc[0,'CLIS'])
#%%
from spotipy.oauth2 import SpotifyClientCredentials


#%%
# how do I want to do this now?
# library_builder.py
# [1] define access token
# [2] define user of interest
# def get_user_playlists
# def get_tracks_from_playlists

#%% 