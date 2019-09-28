import streamlit as st
from src import *
import pandas as pd
# mock up! 

# let's start by looking at some user data!

# define user
st.subheader('Let us try this out! Start by entering your user id')

my_user_id = st.text_input('Input spotify user id:', value = '')
my_user_explorer = SpotifyUserExplorer(my_user_id)

# define and show playlists 
st.subheader('Here are your playlists!')
my_playlists = my_user_explorer.list_playlist_names().tolist()

st.write(type(my_playlists))
st.write(my_playlists)
st.subheader('Now, choose a playlist.')
my_playlist_idx = st.selectbox('test', my_playlists)
st.write(my_playlist_idx)
my_playlist_id  = my_user_explorer.get_playlist_id_from_name(my_playlists[my_playlist_idx])
# my_playlist_id = 
st.write(my_playlist_id)

# what songs do you have on this playlist? 
# tracks = my_user_explorer.connection2spotify.get_tracks_from_playlist_formatted(my_playlist_id)
# tracks_df = pd.DataFrame.from_records(tracks)
# st.write(tracks_df)

# let's get our track list and add it to our audio database
my_playlist = TrackListSpotify() # initialize track list
my_playlist.add_tracks_from_public_user_playlist(my_playlist_id) # add tracks from this playlist
my_playlist.remove_tracks_with_missing_previews() # remove tracks that are missing
my_playlist.populate_audio_database() # and populate the audio database
st.write(my_playlist.dataframe)
    # add a waitbar for adding it to the database here...

st.subheader('Now we can featurize our data!')
feat_musicnn   = FeaturizerMusicnn()
track_features = feat_musicnn.get_features_for_tracks(my_playlist.dataframe['id'])
# feat_musicnn.extract_top_n_tags
# show the top n tags that are of interest to peoples. 
features_df    = pd.DataFrame.from_records(track_features)

st.write(features_df)

st.subheader('But we want to do something more useful with our data...')

# specify our song database 
# let us see what databases we have available...
db_list = TrackListSpotify()
db_list.load_list_from_db('cocjin_all_v2')
st.write(db_list.dataframe.head())

# show tags 
#### featurize button!
#### choose your featurizer
#### and label them!

#### look at the data set's most common tags

# if it's a tagged featurizer, display it
# if it's not a tagged featurizer, then don't display it
