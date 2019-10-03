import streamlit as st 
from src import * 
import pandas as pd

class StreamlitInterface:
    def __init__(self, use_streamlit = True, display_instructions = True):
        self.use_streamlit = use_streamlit
        self.display_instructions = display_instructions

    def select_user(self, instructions = ''):
        default_user = ''
        user_id = default_user
        if self.use_streamlit:
            user_id = st.text_input(label = instructions, value = default_user)
        return user_id

    def write(self, *inputs):
        if self.use_streamlit:
            st.write(*inputs)
        else: 
            print(*inputs)

    def select_single_playlist_from_user(self, user_id, instructions = 'Select a playlist of interest'):
        user_explorer = SpotifyUserExplorer(user_id)
        playlists = user_explorer.list_playlist_names().tolist()
        if self.use_streamlit:
            index = st.selectbox(instructions, ['', 'all playlists'] + playlists)
            if index == 0:
                playlist_name = ''
                playlist_id   = ''
            elif index == 1:
                playlist_name = 'all playlists'
                playlist_id = 'all'
            else:
                playlist_name = playlists[index-2]
                playlist_id   = user_explorer.get_playlist_id_from_name(playlist_name)
            return playlist_id, playlist_name

    def display_tracks_in_tracklist(self, tracklist):
        st.write(tracklist.dataframe.loc[:,['name', 'artist_names']])
    def display_tracks_in_rank_df(self, df):
        st.write(df.loc[:,['rank', 'name', 'artist_names']])


while True: 
    my_interface = StreamlitInterface(use_streamlit = True)

    ##### DEFINING OUR USERS
    users = {}
    users['1'] = {}
    users['2'] = {}

    st.header('OpenSongShare')
    st.subheader('Helping friends share music')

    st.markdown('***')
    st.subheader('First, enter your and your friend\'s Spotify user ids.')
    users['1']['id'] = my_interface.select_user('Enter your Spotify user id:')
    try:
        users['1']['explorer'] = SpotifyUserExplorer(users['1']['id'])    
        users['1']['valid_user'] = True
    except: 
        users['1']['valid_user'] = False
        if users['1']['id']:
            st.write('Your specified spotify id does not exist, please enter another.')

    users['2']['id'] = my_interface.select_user('Enter your friend\'s Spotify user id:')
    try:
        users['2']['explorer'] = SpotifyUserExplorer(users['2']['id'])    
        users['2']['valid_user'] = True
    except: 
        users['2']['valid_user'] = False
        if users['2']['id']:
            st.write('Your friend\'s specified spotify id does not exist, please enter another.')
    
    if not users['1']['valid_user'] or not users['2']['valid_user']:
        break

    ##### DEFINING SEED AND DATABASE
    
    st.subheader('Who is recommending songs to whom?')
    sel_idx = st.selectbox('', ['---','I am recommending songs to my friend.', 'My friend is recommending songs to me.'], value = 0)

    if sel_idx == 0:
        break

    st.markdown('***')
    st.subheader('Which playlists would you like to compare?')
    st.write("Or, if you want, you can compare against all recent playlists by selecting the ''all recent playlists'' option")


    users['1']['sel_play_id'], users['2']['sel_play_name'] = my_interface.select_single_playlist_from_user(users['1']['id'], 
    'Select one of your playlists')

    users['2']['sel_play_id'], users['2']['sel_play_name'] = my_interface.select_single_playlist_from_user(users['2']['id'], 
    "Select one of your friend's playlists")

    if not users['1']['sel_play_id'] or not users['2']['sel_play_id']:
        break
    
    # now get all of the tracks from this playlist
    for idx in ['1', '2']:
        users[idx]['tracklist'] = TrackListSpotify(user = users[idx]['id'])
        if users[idx]['sel_play_id'] == 'all':
            users[idx]['tracklist'].add_all_tracks_from_public_user()
        else:
            users[idx]['tracklist'].add_tracks_from_public_user_playlist(users[idx]['sel_play_id'])
        users[idx]['tracklist'].remove_tracks_with_missing_previews()
        users[idx]['tracklist'].remove_duplicate_tracks()

    st.write('Here are the songs in your playlist!')
    my_interface.display_tracks_in_tracklist(users['1']['tracklist'])

    st.write("And in your friend's playlist!")
    my_interface.display_tracks_in_tracklist(users['2']['tracklist'])

    if sel_idx == 1:
        pl_id = '2'
        db_id = '1'
    else:
        pl_id = '1'
        db_id = '2'

    # get track ids
    pl_ids = users[pl_id]['tracklist'].dataframe['id'].values
    db_ids = users[db_id]['tracklist'].dataframe['id'].values

    # get recommendation 
    st.markdown('***')
    st.subheader("Let's get our recommendations...")
    which_prompt = ['Here are the songs that you should give to your friend!', "Here are songs that you may like in your friend's playlist!"]

    recommender  = Recommender(model_type = 'MTT_musicnn', which_layer = 'taggram', 
    distance_type = 'euclidean', pl_centroid_type = 'k2', rank_type = 'min')
    rank_id_df   = recommender.predict_rank(pl_ids, db_ids)
    rank_df = pd.merge(rank_id_df,  users[db_id]['tracklist'].dataframe)

    st.subheader(which_prompt[sel_idx-1])
    my_interface.display_tracks_in_rank_df(rank_df)

    st.markdown('***')
    st.subheader("Let's explore what they look like!...")

    # # Clustering
    # from sklearn.manifold import TSNE
    # from sklearn import cluster

    # # Basic
    # import numpy as np
    # import pandas as pd
    # import seaborn as sns
    # from matplotlib import pyplot as plt

    # # How does this look in latent dimensional space?? 
    # full_tag_df = pd.concat([users['1']['tag_df'], users['2']['tag_df']])
    # full_tag_df.drop(columns = ['id'], inplace = True)

    # tsne = TSNE(n_components = 2, verbose = 1, perplexity = 40, n_iter = 2000)
    # tsne_results = tsne.fit_transform(full_tag_df.values)

    # plt.figure(figsize = (16, 11))
    # plt.scatter(tsne_results[:,0], tsne_results[:,1])
    # st.pyplot()



    
    break

# how can we recommend songs that go into a shared playlist
# tool - recommend songs for friends

# which of your music you're going to like... 

# only that person likes...

# overlapping songs that you enjoy
# yes or no to each other...

# well, my tool 
# you can recommend songs to each other
# and even create a playlist out of it..

# would you like to make a playlist from these playlists?
# how many songs from yours
# how many songs from theirs

# download both as csvs

# interpretability - here's what you like
# overlapping space and tastes
