# import src.Widgets

# user_exploration.py 

# specify our user
# define which playlist(s) to look at
# visualize the playlists in t-SNE space
# color t-SNE space

# let's start by defining our user
import streamlit as st 
from src import * 
import pandas as pd

class StreamlitInterface:
    def __init__(self, use_streamlit = True, display_instructions = True):
        self.use_streamlit = use_streamlit
        self.display_instructions = display_instructions

    def select_user(self):
        default_user = '1240204888'
        user_id = default_user
        if self.use_streamlit:
            user_id = st.text_input(label = 'Enter the user id that you are interested in.', value = default_user)
        return user_id

    def write(self, *inputs):
        if self.use_streamlit:
            st.write(*inputs)
        else: 
            print(*inputs)

    def select_single_playlist_from_user(self, user_id):
        user_explorer = SpotifyUserExplorer(user_id)
        playlists = user_explorer.list_playlist_names().tolist()
        if self.use_streamlit:
            index = st.selectbox('Select a playlist of interest', playlists)
            playlist_name = playlists[index]
            playlist_id   = user_explorer.get_playlist_id_from_name(playlist_name)
            st.text('Playlist name: ' + playlist_name  + '\nPlaylist id: ' + playlist_id)
            return playlist_id

    def display_tracks_in_tracklist(self, tracklist):
        st.write(tracklist.dataframe.loc[:,['name', 'artist_names']])

    # def select_multiple_playlists_from_user(self, user_id):
    #     user_explorer = SpotifyUserExplorer(user_id)
    #     playlists = my_user_explorer.list_playlist_names().tolist()
    #     default_idx = 0
    #     idx = default_idx
    #     if self.use_streamlit:
    #         playlist_name = st.selectbox('Select a playlist of interest', my_playlists, index = 0)
    #     return user_explorer.get_playlist_id_from_name(playlist_name)
    
test_interface = StreamlitInterface(use_streamlit = True)
user_id = test_interface.select_user()
user_explorer = SpotifyUserExplorer(user_id)
test_interface.write(user_id)

# now check out the user's playlists

st.header('Here, we will analyze what kinds of songs you listen to!')

which_track_set = st.radio('What would you like to analyze?', ['All public songs', 'A single playlist', 'A combo of playlists'])
playlist_id = test_interface.select_single_playlist_from_user(user_id)
st.write(playlist_id)

# now get all of the tracks from this playlist
tracklist = TrackListSpotify(user = user_id)
tracklist.add_tracks_from_public_user_playlist(playlist_id)
tracklist.remove_tracks_with_missing_previews()
tracklist.remove_duplicate_tracks()
track_ids = tracklist.dataframe['id'].values

test_interface.display_tracks_in_tracklist(tracklist)

# now let's featurize it
feat_musicnn   = FeaturizerMusicnn()
track_features = feat_musicnn.get_features_for_tracks(track_ids)
features_df    = pd.DataFrame.from_records(track_features)

# let's show the songs against the taggrams

# what features do we have? 
st.write(features_df.columns)

# we need to convert the features to taggram vs. song id
tagmat = np.vstack(features_df['taggram'].values)
st.write(tagmat.shape)

tag_df = pd.DataFrame(data = tagmat, columns = feat_musicnn.tags)
tag_df['id'] = features_df['id']

st.write(tag_df)

tag_df.set_index('id', inplace = True)
import seaborn as sns
f = sns.heatmap(tag_df)
# st.write(dir(f))
st.pyplot(f.get_figure())


# Clustering
from sklearn.manifold import TSNE
from sklearn import cluster

# Bokeh
from bokeh.io import output_notebook
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import HoverTool

# Basic
import numpy as np
import pandas as pd

X = 
tsne = TSNE(init='pca', perplexity=40, learning_rate=1000, 
            early_exaggeration=8.0, n_iter=1000, random_state=0, metric='l2')
tsne_representation = tsne.fit_transform(X)


# from bokeh.plotting import figure
# long_tag_df = tag_df.melt(id_vars = ['id'])
# st.write(long_tag_df)
# p = figure()
# hm = p.rect(source = long_tag_df, x='variable', y='id',fill_color={'field': 'value'}, width = 100, height = 100)
# st.bokeh_chart(hm)
# x = [1, 2, 3, 4, 5]
# y = [6, 7, 2, 4, 5]
# p = figure(title='simple line example',x_axis_label='x',y_axis_label='y')
# p.line(x, y, legend='Trend', line_width=2)
# st.bokeh_chart(p)

#%%
# import bokeh
# from bokeh.charts import HeatMap, bins, output_file, show, vplot
# hm = HeatMap(long_tag_df, x = bins('variable'), y = bins('id'), values = 'value')

#%%
# track_ids = tracklist.dataframe['id'].values

# how about we show attributes of the tracks? 

# okay! let's grab the playlist id
# test_interface.write(playlist_id)

# if which_track_set == 'All public songs':
#     pass    
# elif which_track_set == 'A single playlist':
# elif which_track_set == 'Several playlists':
#     pass